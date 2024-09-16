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
        -- inserindo atributos faltantes
        alter table staging_area add column banco text;
        

        -- atualizando banco
        update staging_area
        set banco = '{bank}'; -- ajuste o banco, para string que a tabela staging_area esta retornando
        
        -- atualizando convenio/tipo_operacao
        update staging_area set tipo_operacao = CASE
        WHEN tipo_operacao IN ('NOVO') THEN 'MARGEM LIVRE (NOVO)'
        WHEN tipo_operacao IN ('REFIN') THEN 'REFINANCIAMENTO DA PORTABILIDADE'
        WHEN tipo_operacao IN ('PORTABILIDADE') THEN 'PORTABILIDADE'
        else tipo_operacao
        end;
        

        -- atualizando orgao/conveniada
        update staging_area set conveniada = CASE
        WHEN conveniada IN ('SIAPE') THEN 'FEDERAL'
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
        
   