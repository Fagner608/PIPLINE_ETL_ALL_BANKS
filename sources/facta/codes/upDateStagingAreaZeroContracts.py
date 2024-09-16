# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginAreaZero():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        pass

    
    def upDatating(self):
        
        '''
         Atualiza dados do contrato que tenha comissão e bonus zerados
        '''
        # propostas = self.propostasUnicas()
        # propostas = [int(proposta) if proposta is not None else proposta for proposta in propostas]
        
        # print(propostas != None)
        con, cur = inputsDB().conDatabase()
        ############ Digite aqui suas querys ############
        # exemlo
        query = f'''
            
                -- Atualizando usuario
                DELETE from contrato
                where 
                    valor_cms_repasse == '0,00' or valor_cms_repasse == '0' or valor_cms_repasse == '0.00' 
                and 
                    valor_bonus_repasse == '0,00' or valor_bonus_repasse == '0' or valor_bonus_repasse == '0.00'
                and 
                    nome_banco == 'FACTA FINANCEIRA'

        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            raise
            # pass
        con.commit()
        cur.close()
        con.close()
        
#debug
# updateStaginAreaZero().upDatating()