import sys

sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime
import sqlite3
import re


def cleaningImportation(bank: str, date = datetime.date):

    # Trabalhando na tabela de produção
    production = read_downaload().read_data(
                    bank='crefisa',
                    date = date,
                    type_transference = ['importation'],
                    engine = ['csv'],
                    decimal = ',',
                    thousands = '.',
                    header = 0,
                    encoding = 'latin-1'
                )
    if production is not None:
        result = production
        result['ADE'] = result['ADE'].apply(lambda x: str(x)[:12])
        result = result[['Banco', 'Nome Arquivo', 'ADE']]
        
        
        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                            columns_convert =['banco', 'ade'])

        
        # Spiit no tipo_contrato (001 - Novo Contrato)
        result['data_importacao'] = result['nome_arquivo'].map(lambda x: (re.findall('\d{1,2}-\d{1,2}-\d{4}', x) or re.findall('\d{1,2}-\d{1,2}', x))[0])
        result.drop(['nome_arquivo'], axis = 1, inplace=True)
        result['data_importacao'] = result['data_importacao'].apply(lambda x: x + f"-{date.year}" if len(x) < 8 else x)
        result['data_importacao'] = result['data_importacao'].apply(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
        saveStageArea().inputTable(table = result)
        






def statusManager(bank:str, date: datetime.date):
    
    con, cur = inputsDB().conDatabase()

    # Gerenciamento de status - ainda vou incluir aqui a data da importacao
    
    try:
        cur.execute("""
            update contrato -- retorna ade
            set status_importacao = 'importado' -- da tabela contrato
            WHERE (status_importacao != 'importada' OR status_importacao IS NULL) -- se o status nao for importado
            AND numero_ade IN (SELECT ade FROM staging_area) --e a ade esteja no staging area
        """)


    except sqlite3.OperationalError:
        pass
    con.commit()
    cur.close()
    con.close()

#Debug
# cleaningImportation('crefisa', date=datetime.date(2024, 7, 23))
# statusManager('crefisa', date=datetime.date(2024, 6, 16))
