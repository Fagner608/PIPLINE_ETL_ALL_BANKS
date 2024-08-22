# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginAreaCrefisa():

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
        con, cur = inputsDB().conDatabase()
        
        ############ Digite aqui suas querys ############
        # exemlo
        query = f'''

        -- inserindo nome_operacao
        alter table staging_area add column nome_operacao text;
        

        -- atualizando banco
        update staging_area
        set descr_promotora = '{bank}'
        where descr_promotora = 'v8bank'; -- ajuste o banco, para string que a tabela staging_area esta retornando
        
        
        -- atualizando tipo de contrato/opercao
        update staging_area
        set nome_operacao = 'CARTÃO C/ SAQUE';
        
        
        -- atualizando convenio
        update staging_area set descr_tabela = CASE
        WHEN descr_tabela in ('inssrmcbank', 'inss_cbrep_legalbank', 'inssrmc_rep_legalbank') then 'INSS'
        WHEN descr_tabela in ('inss_cartao_beneficiobank') then 'INSS Cartão Benefício'
        else descr_tabela
        end;

        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            raise
            # pass
        con.commit()
        cur.close()
        con.close()
        
   