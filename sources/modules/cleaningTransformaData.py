import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import locale
from re import sub
from typing import Union
import sqlite3

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

# Classe que recebe o retorno do readDownloa e realiza limpeza dos dadados
class cleaningData():

    '''
        Classe para limpeza dos dados.

        Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original.

        Lembre-se de configurar os argumentos: 'decimal' e 'thousands' da classe readDownload.

    '''

    def __init__(self):
        pass





    def cleaning(self, dataFrame: pd.DataFrame, columns_convert: list, typeData: Union['monetary', 'string']) -> pd.DataFrame:
                '''
                    Método para tratar valores monetários, strings e labels das colunas. Não insira percentuais.
                    Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original.
                '''
            
                dataFrame.columns = [str(x).strip().replace(" ", "_").lower() for x in dataFrame.columns]
                dataFrame.columns = [sub(r"\%|\.", "", x) for x in dataFrame.columns]
                
                dataFrame.columns = [sub(r'[áàãâä]', 'a', x) for x in dataFrame.columns]
                dataFrame.columns = [sub(r'[éèêë]', 'e', x) for x in dataFrame.columns]
                dataFrame.columns = [sub(r'[íìîï]', 'i', x) for x in dataFrame.columns]
                dataFrame.columns = [sub(r'[óòõôö]', 'o', x) for x in dataFrame.columns]
                dataFrame.columns = [sub(r'[úùûü]', 'u', x) for x in dataFrame.columns]
                dataFrame.columns = [sub(r'[ç]', 'c', x) for x in dataFrame.columns]
                dataFrame.columns = [sub(r"['’]", '', x) for x in dataFrame.columns]
                

                if typeData[0] == 'monetary':
                    for column in columns_convert:
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r"[$R$\-]", "", str(x)).strip())

                elif typeData[0] == 'string':
                    for column in columns_convert:
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r"'|\*|`|'|'|\?|\$|$|\.|R\$|\%|\-|-|\_", "", str(x)).strip().replace(" ", "_"))
                        dataFrame[column] = dataFrame[column].apply(lambda x: str(x).lower())
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r'[áàãâä]', 'a', x))
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r'[éèêë]', 'e', x))
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r'[íìîï]', 'i', x))
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r'[óòõôö]', 'o', x))
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r'[úùûü]', 'u', x))
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r'[ç]', 'c', x))
                        dataFrame[column] = dataFrame[column].apply(lambda x: sub(r"['’]", '', x))
                   
                return dataFrame

    


# Classe que recebe o retorno do readDownloa e realiza limpeza dos dadados
class transformationData():

    '''
        Classe para tratamento dos dados.

        Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original.

    '''
    def __init__(self):
        pass


    def convert_monetary(self, dataFrame: pd.DataFrame, columns_convert: list) -> pd.DataFrame:
            '''
                    Método para tratar valores monetários, não insiera percentuais.
            '''
    
            
            for column in columns_convert:
                try:
                    dataFrame[column] = dataFrame[column].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                except ValueError:
                    dataFrame[column] = dataFrame[column].str.replace(".", "")
                    dataFrame[column] = dataFrame[column].str.replace(",", ".")
                    dataFrame[column] = dataFrame[column].map(lambda x: locale.currency(float(x), symbol=False, grouping=True) if len(x) > 0 else x)
                     
            return dataFrame


class saveStageArea():
    '''
        Classe para salvar o resultado na Stage Area.

    '''

    def __init__(self):
         pass
    

    def _conDatabase(self):
        con = sqlite3.connect("../../../ZZ/importacoes.db")
        cur = con.cursor()
        query = "create table if not exists staging_area(tabela BLOB)"
        cur.execute(query)
        con.commit()
        return con, cur

    def inputTable(self, table: pd.DataFrame):
        con, cur = self._conDatabase()
        
        table.to_sql('staging_area', 
                            con = con,
                            if_exists = 'replace',
                            index = False)
        cur.close()
        con.close()

    
         