import sys

sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea_BMS
from inputDataTransformed import inputsDB
import datetime
import sqlite3
import re


def cleaningImportation(bank: str, date = datetime.datetime):

    # Trabalhando na tabela de produção
    production = read_downaload().read_data(
                    bank='v8_bms',
                    date = date.date(),
                    type_transference = ['importation'],
                    engine = ['csv'],
                    decimal = ',',
                    thousands = '.',
                    header = 0,
                    encoding = 'latin-1'
                )
    if production is not None:
        result = production
        # result['ADE'] = result['ADE'].apply(lambda x: str(x)[:12])
        result = result[['Banco', 'Nome Arquivo', 'ADE']]
        
        
        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                            columns_convert =['banco'])

        
        # Spiit no tipo_contrato (001 - Novo Contrato)
        # OBS: ainda não estou usando a data da importação
        # result['data_importacao'] = result['nome_arquivo'].map(lambda x: (re.findall('\d{1,2}-\d{1,2}-\d{4}', x) or re.findall('\d{1,2}-\d{1,2}', x))[0])
        # result.drop(['nome_arquivo'], axis = 1, inplace=True)
        # result['data_importacao'] = result['data_importacao'].apply(lambda x: x + f"-{date.year}" if len(x) < 8 else x)
        # result['data_importacao'] = result['data_importacao'].apply(lambda x: datetime.datetime.strptime(x, '%d-%m-%Y'))
        saveStageArea_BMS().inputTable(table = result)
        






def statusManager(bank:str, date: datetime.datetime):
    
    con, cur = con, cur = inputsDB().conDatabaseBMS()

    # Gerenciamento de status - ainda vou incluir aqui a data da importacao
    try:
        cur.execute("""
            update contratos_bms -- retorna ade
            set status_importacao = 'importado' -- da tabela contratos_bms
            WHERE (status_importacao != 'importada' OR status_importacao IS NULL OR status_importacao != 'importado') -- se o status nao for importado
            AND "NUMERO PROPOSTA" IN (SELECT ade FROM temp_table) --e a ade esteja no staging area
        """)
    except sqlite3.OperationalError:
        raise
        # pass
    con.commit()
    cur.close()
    con.close()

#Debug
# cleaningImportation('v8_bms', date=datetime.datetime.today())
# statusManager('v8_bms', date=datetime.datetime.today())
