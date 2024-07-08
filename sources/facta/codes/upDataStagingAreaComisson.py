# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class upDataStagingAreaComisson():

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

        -- Atualizando cliente id
        alter table staging_area add column banco text;
        update staging_area
        set banco = '{bank}'
        
        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            pass
        con.commit()
        cur.close()
        con.close()
        
   