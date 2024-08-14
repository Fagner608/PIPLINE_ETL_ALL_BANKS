# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginAreaUsuario():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        pass

    def conciliation_user(self, proposta: int, contaCorrente: pd.DataFrame):

                contaCorrente = contaCorrente
                proposta = proposta
                retorno = contaCorrente[(contaCorrente['Código'].astype(int) == int(proposta))]['Login'].values
                if len(retorno) > 0:
                    
                    return retorno[0]
                else:
                     return
            
    def propostasUnicas(self):
         
        '''
         Retornar propostas da staging_area
        '''

        con, cur = inputsDB().conDatabase() 

        query = '''
            select distinct 
                proposta
            from 
                staging_area
           '''
        
        propostas = cur.execute(query).fetchall()
        cur.close()
        con.close()

        return [proposta[0] for proposta in propostas]

    def upDatating(self, contaCorrente: pd.DataFrame):
        
        '''
         Atualiza dados do staging_area
        '''
        propostas = self.propostasUnicas()
        propostas = [int(proposta) if proposta is not None else proposta for proposta in propostas]
        
        # print(propostas != None)
        for proposta in propostas:
            if proposta is not None:
                con, cur = inputsDB().conDatabase()
                ############ Digite aqui suas querys ############
                # exemlo
                query = f'''
            
                -- Atualizando usuario
                UPDATE staging_area
                set codigo_usuario_digitador = '{self.conciliation_user(proposta=proposta, contaCorrente=contaCorrente)}'
                where proposta == {proposta};

                '''
                try:
                    cur.executescript(query)
                except sqlite3.OperationalError:
                    raise
                con.commit()
                cur.close()
                con.close()
        
   