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

        -- inserindo atributos faltantes
        alter table staging_area add column banco text;
        alter table staging_area add column sit_pagamento_cliente text;
        alter table staging_area add column vendedor text;

        -- Atualizando vendedor
        update staging_area
        set vendedor = 'the_one_prestacao_de_servicos_ltda';
        

        -- Atualizando sit_pagamento_cliente
        update staging_area
        set sit_pagamento_cliente = 'PAGO';

        -- atualizando banco
        update staging_area
        set banco = '{bank}'; -- ajuste o banco, para string que a tabela staging_area esta retornando
        
        -- atualizando convenio/tipo_operacao
        update staging_area set tipo_operacao = CASE
        WHEN tipo_operacao IN ('NOVO') THEN 'MARGEM LIVRE (NOVO)'
        WHEN tipo_operacao IN ('REFIN', 'REFIN PORTABILIDADE ESPECIAL') THEN 'REFINANCIAMENTO DA PORTABILIDADE'
        WHEN tipo_operacao IN ('PORTABILIDADE', 'PORTABILIDADE ESPECIAL') THEN 'PORTABILIDADE'
        else tipo_operacao
        end;
        

        -- atualizando orgao/conveniada
        update staging_area set conveniada = CASE
        WHEN conveniada IN ('SIAPE') THEN 'FEDERAL'
        WHEN conveniada IN ('INSS DATAPREV') THEN 'INSS'
        else conveniada
        end;


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
            # raise
            pass
        con.commit()
        cur.close()
        con.close()
        
   