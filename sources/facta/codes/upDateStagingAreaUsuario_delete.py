# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginAreaUsuarioDelete():

    '''
    Método para localizar e deletar propostas que ainda não encontram usuário.
    
    '''

    def __init__(self):
        pass
 
    def upDatating(self):
        
        '''
         Atualiza dados do staging_area
        '''
        # print(propostas != None)
        con, cur = inputsDB().conDatabase()
                ############ Digite aqui suas querys ############
                # exemlo
        query = f'''

                --Deletando usuários que não tenha código
                DELETE from staging_area
                WHERE codigo_usuario_digitador = ''
                OR codigo_usuario_digitador IS NULL
                OR codigo_usuario_digitador in ('none', 'NONE', 'None');
                '''
        try:
                    cur.executescript(query)
        except sqlite3.OperationalError:
                    # raise
                    pass
        con.commit()
        cur.close()
        con.close()
        
   