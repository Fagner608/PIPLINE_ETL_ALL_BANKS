# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginAreaContracts():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        pass

    def upDatating(self, bank = str):
        
        '''
         Retorna propostas com status de importacao 'nao_importadas'
        '''
        #### substituir esta conexão com a do DB postgre
        con, cur = inputsDB().conDatabaseBMS()
        
        ############ Digite aqui suas querys ############
        # exemlo

        query = f'''
        alter table temp_table add column BANCO text;
        alter table temp_table add column PROVEDOR text;
        alter table temp_table add column ORGAO text;
        alter table temp_table add column TIPO_DE_OPERACAO text;
        alter table temp_table add column SITUACAO text;
        alter table temp_table add column FORMALIZACAO_DIGITAL text;
        alter table temp_table add column status_importacao text;
        

        --Atualizando
        update temp_table
        set status_importacao = 'nao_importado';

        --Atualizando
        update temp_table
        set SITUACAO = 'PAGO';

        -- atualizando banco
        update temp_table
        set BANCO = '{bank}';
        
        -- atualizando provedor
        update temp_table
        set PROVEDOR = 'BMS';

        -- atualizando orgao
        update temp_table
        set ORGAO = 'FGTS';
        

        -- atualizando orgao
        update temp_table
        set TIPO_DE_OPERACAO = 'MARGEM LIVRE (NOVO)';

        -- atualizando orgao
        update temp_table
        set FORMALIZACAO_DIGITAL = 'SIM';

        
        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            pass
        con.commit()
        cur.close()
        con.close()
        
   