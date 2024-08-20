# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginAreaExtra():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        pass

    def conciliation_flat(self, proposta: int, contaCorrente: pd.DataFrame, flat = False):

                contaCorrente = contaCorrente
                proposta = proposta
                retorno = contaCorrente[(contaCorrente.codigoaf == proposta) & (contaCorrente.tipocontacorretor == 54)]['credito'].values
                if flat:
                    retorno = contaCorrente[(contaCorrente.codigoaf == proposta) & (contaCorrente.tipocontacorretor == 1)]['credito'].values
                if len(retorno) > 1:
                    teste = float()
                    for item in retorno:
                        item = float(item.replace(".", "").replace(",", "."))
                        teste = teste + item
                        retorno = '{0:.2f}'.format(teste)
                else:
                    try:
                        retorno  = retorno[0]
                        retorno = retorno.replace(".", "").replace(",", ".")
                    except IndexError:
                        retorno = 0.00
                return retorno
            
    def propostasUnicas(self):
         
        '''
         Retornar propostas da staging_area
        '''

        con, cur = inputsDB().conDatabase() 

        query = '''
            select distinct 
                codigo
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
            
                -- Atualizando flat
                UPDATE staging_area
                set vl_comiss = {self.conciliation_flat(proposta=proposta, contaCorrente=contaCorrente, flat=True)}
                where codigo == {proposta};
                
                -- Atualizando bonus
                UPDATE staging_area
                set bonus = {self.conciliation_flat(proposta=proposta, contaCorrente=contaCorrente)}
                where codigo == {proposta};
                
                '''
                
                
                try:
                    cur.executescript(query)
                except sqlite3.OperationalError:
                    raise
                con.commit()
                cur.close()
                con.close()
        
   