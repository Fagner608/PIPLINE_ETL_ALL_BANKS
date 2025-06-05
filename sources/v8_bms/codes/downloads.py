# imports 
from os import makedirs, path, remove, listdir
import sys

    # modulos base
sys.path.append("../../modules")
from login_code import login
from sendActions import move_file

    # webscraping
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import psycopg2
import sqlalchemy

    # manipulacao dedados
import datetime
import pandas as pd
from time import strptime

    # barra de progressao
from tqdm import tqdm


# Classe para baixar tabelas
class download():

    def __init__(self):
        self.credentials = dotenv_values("../data/.env") 
        self.engine = sqlalchemy.create_engine(f"postgresql://{self.credentials['USER']}:{self.credentials['PASSWORD']}@{self.credentials['HOST']}:{self.credentials['PORT']}/{self.credentials['DBNAME']}?sslmode=require")
        
    

    def __query(self, date_work: datetime.date):
        date_from = date_work
        date_to = date_from - datetime.timedelta(days = 30)

        query = f'''
        SELECT 
            payload->'ccb'->>'id' AS numero_proposta,
            payload->>'legacy_status' AS status,
            payload->'client'->>'name' AS nome,
            payload->'client'->>'email' AS email,
            payload->'client'->>'cell_phone' AS telefone,
            payload->'client'->>'document_number' AS cpf,
            (payload->'simulation'->'disbursement_options'->0->'issue_amount')::numeric AS valor_de_emissao,
            (payload->'simulation'->'disbursement_options'->0->'disbursed_issue_amount')::numeric AS valor_de_desembolso,
            jsonb_array_length(payload->'simulation'->'disbursement_options'->0->'installments') as prazo,
            TO_TIMESTAMP((payload->>'paid_at')::bigint) AS data_de_pagamento,
            TO_TIMESTAMP((payload->>'created_at')::bigint) AS data_de_criacao,
            (payload->'simulation'->'disbursement_options'->0->'iof_total')::numeric AS iof_total,
            (payload->'simulation'->'disbursement_options'->0->'tac'->>'Percentual') AS tac,
            (payload->'simulation'->'disbursement_options'->0->'tac_total')::numeric AS tac_total,
            payload->>'vendor_id' as id_vendedor,
            payload->'simulation'->'table'->'data'->>'id' as id_tabela
        FROM public.operations
        WHERE payload->>'legacy_status' = 'paid'
        AND TO_TIMESTAMP((payload->>'paid_at')::bigint) >= '{date_to.strftime("%Y-%m-%d")}'
        AND TO_TIMESTAMP((payload->>'paid_at')::bigint) <= '{date_from.strftime("%Y-%m-%d")}'
        '''
        return query
    

    def get_data(self, date_work: datetime.date):
            query = self.__query(date_work=date_work)
            dados = pd.read_sql(query, 
                                con = self.engine) ## informar a query
            if dados.empty:
               input(f"Sem dados para a data {date_work}. Pressione qualquer tecla para continuar!")  
            else:
                return dados


    def menagerTasks(self, date_work: datetime.date):
        '''

            Executa a classe self.__production() e faz a transferencia do download para a pasta download correta.

        '''
        path_to_save = f'../download/{date_work.year}/{date_work.month}/production/{date_work}.parquet'
        
        # Realiza dowenload somente se o download não existir
        # if not path.exists(path_to_save):
        if True:
            try:
                dados = self.get_data(date_work=date_work)            
            except TimeoutException:
                dados = self.get_data(date_work=date_work)

            # persiste .parquet
            dados.to_parquet(path_to_save)

    def tqdm_bar(self, date_work = datetime.date):
        '''
            Executa as classes anteriores, mostrando barra de progressao.

        '''
        processos = [("Obtendo propostas", self.menagerTasks)]
        
        with tqdm(total=len(processos), desc="Executando processos") as pbar_total:
            for processo_desc, processo_func in processos:
                
                pbar_total.set_description(processo_desc)
                try:
                    processo_func(date_work = date_work)
                except Exception as exc:
                    raise(exc)
                    
                pbar_total.update(1)

# Debug - exemplo de chamaa do modulo
# download().tqdm_bar(date_work = datetime.date.today())