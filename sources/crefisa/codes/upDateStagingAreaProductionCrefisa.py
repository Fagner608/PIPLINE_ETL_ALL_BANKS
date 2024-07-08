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

        -- atualizando banco
        update staging_area
        set banco = '{bank}'
        where banco = 'crefisa'; -- ajuste o banco, para string que a tabela staging_area esta retornando
        
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

        -- Atualizando cliente id
        alter table staging_area add column cliente_id text;
        update staging_area
        set cliente_id = cliente.cliente_id
        from cliente
        where staging_area.cpf == cliente.cpf_cliente


        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            pass
        con.commit()
        cur.close()
        con.close()
        
   