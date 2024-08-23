# imports
import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime
from upDateStagingAreaUsuario import updateStaginAreaUsuario
from upDateStagingAreaUsuario_delete import updateStaginAreaUsuarioDelete
# Funcao para executar limpeza, tratamento e transformacao
def CleaningUser(date: datetime.date):

    '''
        Funcao para executar limpeza, tratamento e transformacao no relatorio extra
        ### date: argumnento setado no modulo main.py, quando chama o modulo main_transformLoad.py

        Execute a funcao uma primeira vez para pegar os novos labels, e informar nos argumentos que seguem.

    '''

    ## Carga da tabela de comissão
    production = read_downaload().read_data(
                        bank='facta', # informe o nome do banco conforme esta no diretorio criado
                        date = date,
                        type_transference = ['production'],
                        engine = ['html'], # informe o engine para leitura: csv, excel, html
                        decimal = '.',
                        thousands = '.',
                        parse_dates=[],
                        format_parse_dates='%d/%m/%Y'
                    )

    ## Codigo segue o fluxo se o arquivo for lido com sucesso
    if production is not None:
        production.columns = production.iloc[production.shape[0]-1, ].to_list()
        production = production.drop(production.shape[0]-1)
        final_production = production[['Código', 'Login']]
        updateStaginAreaUsuario().upDatating(contaCorrente = final_production)
        updateStaginAreaUsuarioDelete().upDatating()


# Debug
# CleaningUser(date = datetime.date(2024, 8, 23))
