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

        -- incluindo sit_pagamento_cliente
        alter table staging_area add column sit_pagamento_cliente text;
        alter table staging_area add column nome_operacao text;
        
        update staging_area
        set sit_pagamento_cliente = 'PAGO';

        -- atualizando banco
        update staging_area
        set promotora = '{bank}'
        where promotora = 'V8BANK'; -- ajuste o banco, para string que a tabela staging_area esta retornando
        
        
        -- atualizando tipo de contrato/opercao
        update staging_area
        set nome_operacao = 'CARTÃO C/ SAQUE';


        -- atualizando convenio
        update staging_area set descricao = CASE
        WHEN descricao in ('inssrmc_bank', 'inssrmc_rep_legalbank') then 'INSS'
        WHEN descricao in ('inss_cartao_beneficiobank') then 'INSS Cartão Benefício'
        else descricao
        end;


        -- Atualizando cliente id
        alter table staging_area add column cliente_id text;
        update staging_area
        set cliente_id = cliente.cliente_id
        from cliente
        where staging_area.cpf == cliente.cpf_cliente;


        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            raise
            # pass
        con.commit()
        cur.close()
        con.close()
        
   