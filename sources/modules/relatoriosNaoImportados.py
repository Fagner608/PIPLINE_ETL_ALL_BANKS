# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
from inputDataTransformed import inputsDB
import pandas as pd
class relatoriosNaoImportados():

    '''
        Retornar propostas que ainda não foram importadas para o storm.

    '''

    def __init__(self):
        pass

    def naoImportados(self, bank = str):
        '''
        Retorna propostas com status de importacao 'nao_importadas'

        ### Argumentos
            bank: defina o banco conforme lista  na tabela bancos.
        '''
        con, cur = inputsDB().conDatabase()
        # dados_nao_importado = pd.read_sql(f'''
        #                                   select * 
        #                                   from 
        #                                     contrato
        #                                   where 
        #                                     nome_banco = '{bank}'
        #                                   and 
        #                                     status_importacao = 'nao_importado'
        #                                   ''', con)
        dados_nao_importado = pd.read_sql(f'''
                                          select 
                                            contrato.*,
                                            cliente.nome_cliente,
                                            cliente.cpf_cliente
                                          from 
                                            contrato
                                          join cliente on contrato.cliente_id = cliente.cliente_id 
                                          where 
                                            nome_banco = '{bank}'
                                          and 
                                            status_importacao = 'nao_importado'
                                          ''', con)
        


        cur.close()
        con.close()
        return dados_nao_importado
    
   
class relatoriosNaoImportados_v8_bms():

    '''
        Retornar propostas que ainda não foram importadas para o storm.

    '''

    def __init__(self):
        pass

    def naoImportados(self, bank = str):
        '''
        Retorna propostas com status de importacao 'nao_importadas'

        ### Argumentos
            bank: defina o banco conforme lista  na tabela bancos.
        '''
        con, cur = inputsDB().conDatabaseBMS()
        # dados_nao_importado = pd.read_sql(f'''
        #                                   select * 
        #                                   from 
        #                                     contrato
        #                                   where 
        #                                     nome_banco = '{bank}'
        #                                   and 
        #                                     status_importacao = 'nao_importado'
        #                                   ''', con)
        dados_nao_importado = pd.read_sql(f'''
                                          select 
                                            *
                                          from 
                                            contratos_bms
                                          where 
                                            status_importacao = 'nao_importado'
                                          ''', con)
        


        cur.close()
        con.close()
        return dados_nao_importado
    
   