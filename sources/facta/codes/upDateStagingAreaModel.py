# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd
class updateStaginAreaModel():

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
        query = '''

        -- atualizando banco
        update staging_area
        set banco = 'BANCO CREFISA'
        where banco = 'crefisa';
        
        
        -- atualizando convenio
        update staging_area
        set convenio = 'CRÉDITO PESSOAL'
        where convenio = 'baixa_renda';
        
        update staging_area
        set convenio = 'CRÉDITO PESSOAL'
        where convenio = 'inss';
        
        -- atualizando tipo de contrato/opercao
        update staging_area
        set tipo_contrato = 'MARGEM LIVRE (NOVO)'
        where tipo_contrato = 'novo_contrato';
        
        update staging_area
        set tipo_contrato = 'MARGEM LIVRE (NOVO)'
        where tipo_contrato = 'antecipacao_1_parcela';
        
        update staging_area
        set tipo_contrato = 'MARGEM LIVRE (NOVO)'
        where tipo_contrato = 'antecipacao_1_parcela';
        
        update staging_area
        set tipo_contrato = 'REFINANCIAMENTO'
        where tipo_contrato = 'refinanciamento';

        '''

        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            raise
            # pass
        con.commit()
        cur.close()
        con.close()
        
   