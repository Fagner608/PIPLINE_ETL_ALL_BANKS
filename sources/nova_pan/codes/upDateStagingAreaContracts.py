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
        con, cur = inputsDB().conDatabase()
        
        ############ Digite aqui suas querys ############
        # exemlo
        query = f'''

        -- inserindo colunas
        alter table staging_area add column sit_pagamento_cliente text;
        alter table staging_area add column cliente_id text;

        update staging_area
        set sit_pagamento_cliente = 'PAGO';

        -- Atualizando prazo
        UPDATE staging_area
        set qtd_parcela = 1
        where qtd_parcela == 0;
        

        -- Atualizando cliente id
        update staging_area
        set cliente_id = cliente.cliente_id
        from cliente
        where staging_area.cod_cpf_cliente == cliente.cpf_cliente;


        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            # raise
            pass
        con.commit()
        cur.close()
        con.close()
        
   