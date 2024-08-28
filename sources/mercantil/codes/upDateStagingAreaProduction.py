# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginArea():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        pass

    def upDatating(self, bank = str):
        
        '''
         Atualiza propostas no staging_area
        '''
        con, cur = inputsDB().conDatabase()
        
        ############ Digite aqui suas querys ############
        # exemlo
        query = f'''

        -- inserindo atributo banco
        alter table staging_area add column banco text;
        alter table staging_area add column nome_operacao text;
        

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
        WHEN codigoproduto in ('13728077', '13728076', '13728078') THEN 'MARGEM LIVRE (NOVO)'
        WHEN codigoproduto in ('13728071') THEN 'CARTÃO C/ SAQUE'
        else nome_operacao
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
        
   