import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append("../../modules")
from readDownload_v8 import read_downaload
from cleaningTransformaData_v8 import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
from logger import loogerControls
from connectionDB import ConectionDB
from enumClasses import Connector, Database
logger = loogerControls().loggerFunction()
import datetime
import sqlite3
import re
import polars as pl

def cleaningImportation(provider: str, date = datetime.datetime):

    # Trabalhando na tabela de produção
    importation = read_downaload().read_data(
                        bank='v8_bms', # informe o nome do banco conforme esta no diretorio criado
                        date = date,
                        type_transference = ['importation']
                        # engine = ['parquet'], # informe o engine para leitura
                    )
    if importation is not None:
        result = importation
        # result['ADE'] = result['ADE'].apply(lambda x: str(x)[:12])

        try:
            
            result = result.with_columns(pl.col("Nome Arquivo").map_elements(
                lambda x: (re.findall('\\d{1,2}-\\d{1,2}-\\d{4}', x) or re.findall('\\d{4}-\\d{1,2}-\\d{1,2}', x) or re.findall('\\d{1,2}-\\d{1,2}', x))[0],
                return_dtype = pl.Utf8
            ).alias('data_importacao')
            )
            result = result.with_columns(pl.col("data_importacao").map_elements(
                lambda x: x + f"-{date.year}" if len(x) < 8 else x 
            ))
            result = result.drop(['Nome Arquivo'])
            result = result.with_columns(pl.coalesce([
                pl.col('data_importacao').str.to_date(format='%Y-%m-%d', strict = False),
                pl.col('data_importacao').str.to_date(format='%d-%m-%Y', strict=False)
            ]).alias('data_importacao'))
            # result = result.to_pandas()
            logger.info("Limpeza dos dados de importação finalizada.")
        except Exception as exc:
            logger.warning(f"Problema não esperado na limpeza dos dados de importacao: {exc}") 
        logger.info("Enviando dados de importacao para tabela temporaria")
        saveStageArea().inputTable(table = result)
        




def statusManager(provider:str, date: datetime.datetime, db_name: str = Database.BM_BMS.value):
    
    logger.info(f"Iniciando gerenciamento de status da tabela contrato do DB {db_name}")
    # instanciando engine
    con = ConectionDB().psycopgConnection(db_name)
    cur = con.cursor()

    # Gerenciamento de status - ainda vou incluir aqui a data da importacao
    query = """
            WITH tmp AS (
                SELECT * FROM temp_table
            )
            UPDATE contrato ct
            SET id_status_importacao = 1,
            data_importacao = tmp."data_importacao"
            FROM tmp
            WHERE ct.numero_proposta = tmp."ADE"
            AND ct.id_status_importacao != 1
            """
        
    try:
        cur.execute(query)
        affected_rows = cur.rowcount # <-- captura o numero de linhas afetadas
        con.commit()
        logger.info(f"Sucesso ao executar o gerenciamento de status do DB {db_name} - contrato. Update rows: {affected_rows} da tabela contrato.")
    except Exception as exc:
        logger.critical(f"Falha ao executar gerenciamento de status (DB: {db_name}) da tabela contrato: {exc}")
        con.rollback()
        logger.info("Rollback executado")
    cur.close()
    con.close()
        

#Debug
# cleaningImportation('v8_bms', date=datetime.datetime.today())
# statusManager('v8_bms', date=datetime.datetime.today())
