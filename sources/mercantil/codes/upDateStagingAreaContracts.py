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
        alter table staging_area add column valor_cms_repasse real;
        alter table staging_area add column percentual_cms_repasse real;
        
        

        -- atualzando comissoes
        UPDATE staging_area set percentual_cms_repasse = CASE
            -- regras com TCC
        WHEN
            valoremprestimo > 0 and valoremprestimo <= 600 and valortarifatcc > 0 and codigoproduto in (13728077, 13728127, 13728128) THEN 0.16
        WHEN
            valoremprestimo > 600 and valoremprestimo <= 1200 and valortarifatcc > 0 and codigoproduto in (13728077, 13728127, 13728128) THEN 0.15
        WHEN
            valoremprestimo > 1200 and valortarifatcc > 0 and codigoproduto in (13728077, 13728127, 13728128) THEN 0.13
            
            -- regras sem TCC
        WHEN
            valortarifatcc == 0 and codigoproduto in (13728077, 13728127, 13728128) THEN 0.13
        WHEN
            codigoproduto in (13728076, 13728078, 13728079) THEN 0.06



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
        WHEN codigoproduto in ('13728077', '13728076', '13728078', '13728127') THEN 'MARGEM LIVRE (NOVO)'
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
            raise
            # pass
        con.commit()
        cur.close()
        con.close()
        
   