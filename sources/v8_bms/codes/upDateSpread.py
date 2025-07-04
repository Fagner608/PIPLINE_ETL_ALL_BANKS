# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
from connectionDB import ConectionDB
from logger import loogerControls

import pandas as pd



class updateStaginAreaContracts():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        self.logger = loogerControls().loggerFunction()

    def upDatating(self, bank: str, db_name: str, provider: str):
        
        '''
         Retorna propostas com status de importacao 'nao_importadas'
        '''
        #### substituir esta conexão com a do DB postgre
        # instanciando engine
        con = ConectionDB().psycopgConnection(db_name)
        cur = con.cursor()
        
        ############ Digite aqui suas querys ############
        # exemlo

        query = f'''
        
        
                
        '''
        try:
            cur.execute(query)
            con.commit()
            self.logger.info(f"Sucesso ao executar query de atualizacao das tabelas do DB {db_name} - temp_table.")
        except Exception as exc:
            self.logger.critical(f"Falha ao executar query de atualizacao das tabelas da tamp_table: {exc}")
            con.rollback()
            self.logger.info("Rollback executado")
        cur.close()
        con.close()
        
   