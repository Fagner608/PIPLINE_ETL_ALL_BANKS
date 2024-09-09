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
        alter table staging_area add column percentual_cms_a_vista real;
        
        update staging_area
        set sit_pagamento_cliente = 'PAGO';

        -- atualizando banco
        update staging_area
        set descr_promotora = '{bank}'
        where descr_promotora = 'v8bank'; -- ajuste o banco, para string que a tabela staging_area esta retornando
        
        
        -- atualizando tipo de contrato/opercao
        update staging_area
        set nome_operacao = 'CARTÃO C/ SAQUE';


        -- atualizando convenio
        update staging_area set descr_tabela = CASE
        WHEN codigo_orgao in ('202290') then 'INSS'
        WHEN codigo_orgao in ('202284') then 'INSS - CARTÃO BENEFÍCIO'
        WHEN codigo_orgao in ('202329 ') then 'FEDERAL - CARTÃO BENEFÍCIO'
        WHEN codigo_orgao in ('000001 ') then 'FEDERAL'
        else descr_tabela
        end;


        -- Atualizando cliente id
        alter table staging_area add column cliente_id text;
        update staging_area
        set cliente_id = cliente.cliente_id
        from cliente
        where staging_area.cpf_cliente == cliente.cpf_cliente;

        
        
        -- Calculo percentual de comissao
        UPDATE staging_area
        SET percentual_cms_a_vista = CASE
            WHEN codigo_orgao IN ('202290', '202284') THEN 200.0
            WHEN codigo_orgao IN ('202329') THEN 320.0
            ELSE 0
        END;

        
        -- Calculo de comissao
        UPDATE staging_area
        SET vlr_de_comissao = CASE
            WHEN codigo_orgao IN ('202290', '202284') THEN vlr_emprestimo * percentual_cms_a_vista
            WHEN codigo_orgao IN ('202329') THEN vlr_emprestimo * percentual_cms_a_vista
            ELSE 0
        END;



        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            # raise
            pass
        con.commit()
        cur.close()
        con.close()
        
   