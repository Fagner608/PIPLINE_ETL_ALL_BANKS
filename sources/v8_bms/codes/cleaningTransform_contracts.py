# imports
import sys
# mudulos base
sys.path.append("../../modules")
from tempTableManager import CleaningTempTable
from readDownload_v8 import read_downaload
from cleaningTransformaData_v8 import cleaningData, transformationData, saveStageArea
import polars as pl
from inputDataTransformed import inputsDB

from connectionDB import ConectionDB
from enumClasses import Connector, Database
from logger import loogerControls
logger = loogerControls().loggerFunction()

import datetime
from upDateStagingAreaContracts import updateStaginAreaContracts

from updateClientTable import updateProdTables

EXECUTE_NEXT_STEP = False


# Funcao para executar limpeza, tratamento e transformacao
def CleaningContracts(date: datetime.date, provider: str):

    '''
        Funcao para executar limpeza, tratamento e transformacao nos contratos (podem ser do relatorio de producao ou de comissao)
        ### date: argumnento setado no modulo main.py, quando chama o modulo main_transformLoad.py

        Execute a funcao uma primeira vez para pegar os novos labels, e informar nos argumentos que seguem.

    '''
    global EXECUTE_NEXT_STEP
    EXECUTE_NEXT_STEP = False
    ## Carga da tabela desejada
    contracts = read_downaload().read_data(
                        bank='v8_bms', # informe o nome do banco conforme esta no diretorio criado
                        date = date,
                        type_transference = ['production']
                        # engine = ['parquet'], # informe o engine para leitura

                    )
    ## Codigo segue o fluxo se o arquivo for lido com sucesso
    if contracts is not None:
        EXECUTE_NEXT_STEP = True

        final_contracts = contracts
        final_contracts.columns = ["NUMERO PROPOSTA", "STATUS", "NOME", "USUARIO BANCO", "TELEFONE", "CPF", "VALOR OPERACAO", "VALOR LIBERADO", "NUMERO PARCELAS", "DATA DE PAGAMENTO", "DATA DE CRIACAO", "IOF TOTAL", "TAXA TAC", "TAX_INFORMADO", "ID VENDEDOR", "ID TABELA"]
        # final_contracts = final_contracts.to_pandas()
        cols_casting = ["VALOR OPERACAO", "VALOR LIBERADO", "IOF TOTAL", "TAXA TAC", "TAX_INFORMADO"]
        final_contracts = final_contracts.with_columns([pl.col(col).cast(pl.Float64) for col in cols_casting])
        saveStageArea().inputTable(table = final_contracts)
        



def load_contracts(date: datetime.date, provider: str, db_name: str = Database.BM_BMS.value):

    
    '''
        Funcao que prepara os dados carregados na staging_area para carga definitiva no banco de dados

        ## FACA A SEGUINTE CONFIGURACAO:

        - atribua ao lado direito da chave, o label da variavel que será setada no banco de dados, conforme exemplo abaixo. USe os labels tratados.

    '''

    if EXECUTE_NEXT_STEP:
    # if True:

        # Aqui a tabela será atualizada para incluir o que falta
        updateStaginAreaContracts().upDatating(bank='V8 DIGITAL', db_name = db_name, provider = provider)

        ## Buscando propostas incompletas
        CleaningTempTable().getProposals()


        # envia dados para tabela de produção
        updateProdTables()

        ## Atualizando propostas incompletas
        CleaningTempTable().update()

        ## propostas não processadas
        CleaningTempTable().count()



#Debug
# CleaningContracts(date=datetime.date.today(), provider = 'BMS')
# load_contracts(date=datetime.date.today(), provider = 'BMS')