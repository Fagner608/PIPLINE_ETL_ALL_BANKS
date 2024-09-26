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

        -- inserindo atributo banco
        alter table staging_area add column banco text;
        alter table staging_area add column nome_operacao text;
        alter table staging_area add column sit_pagamento_cliente text;
        alter table staging_area add column cliente_id text;
        alter table staging_area add column valor_cms_repasse float;
        alter table staging_area add column percentual_cms_repasse float;
        

        -- Atualizando percentual_cms_repasse
        UPDATE staging_area
        SET percentual_cms_repasse = CASE
            -- Regras com TCC
            WHEN valoremprestimo > 0 AND valoremprestimo <= 600 AND valortarifatcc > 0 AND codigoproduto IN (13728077, 13728127, 13728128) THEN 20
            WHEN valoremprestimo > 600 AND valoremprestimo <= 1200 AND valortarifatcc > 0 AND codigoproduto IN (13728077, 13728127, 13728128) THEN 16
            WHEN valoremprestimo > 1200 AND valortarifatcc > 0 AND codigoproduto IN (13728077, 13728127, 13728128) THEN 13
            
            -- Regras sem TCC
            WHEN valortarifatcc == 0 AND codigoproduto IN (13728077, 13728127, 13728128) THEN 8

            WHEN codigoproduto IN (13728076, 13728078, 13728079) THEN 6

            -- regra cartão
            WHEN codigoproduto IN (13728071) AND quantidadeparcelas between 1 and 17 THEN 0
            WHEN codigoproduto IN (13728071) AND quantidadeparcelas between 48 and 29 THEN 0.50
            WHEN codigoproduto IN (13728071) AND quantidadeparcelas between 60 and 71 THEN 2.20
            WHEN codigoproduto IN (13728071) AND quantidadeparcelas between 72 and 82 THEN 2.75
            WHEN codigoproduto IN (13728071) AND quantidadeparcelas == 83 THEN 3.58
            WHEN codigoproduto IN (13728071) AND quantidadeparcelas == 84 THEN 5.50

            -- regra empréstimo pessoal
            WHEN codigoproduto IN (500, 501) AND quantidadeparcelas == 6 THEN 6
            WHEN codigoproduto IN (500, 501) AND quantidadeparcelas == 12 THEN 6

            ELSE percentual_cms_repasse
        END;
            
        -- Atualizando valor_cms_repasse
        UPDATE staging_area 
        set valor_cms_repasse = round((valoremprestimo * percentual_cms_repasse) / 100, 2);

        -- atualizando sit_pagamento_cliente
        UPDATE staging_area set sit_pagamento_cliente = 'PAGO';
        
        -- atualizando banco
        update staging_area
        set banco = '{bank}'; -- ajuste o banco, para string que a tabela staging_area esta retornando
        
        -- atualizando convenio
        UPDATE staging_area set nomeconvenio = CASE
        WHEN codigoconvenio in ('161594') THEN 'FGTS'
        WHEN codigoconvenio in ('128525') THEN 'INSS'
        else nomeconvenio
        end;
        

        -- atualizando nome_operacao
        UPDATE staging_area set nome_operacao = CASE
        WHEN codigoproduto in ('13728077', '13728076', '13728078', '13728127', '500', '501') THEN 'MARGEM LIVRE (NOVO)'
        WHEN codigoproduto in ('13728071') THEN 'CARTÃO C/ SAQUE'
        else nome_operacao
        end;

        -- Atualizando cliente id
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
        
   