# imports
import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime
from upDateStagingAreaExtra import updateStaginAreaExtra
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF8')

# Funcao para executar limpeza, tratamento e transformacao
def CleaningExtra(date: datetime.date):

    '''
        Funcao para executar limpeza, tratamento e transformacao no relatorio extra
        ### date: argumnento setado no modulo main.py, quando chama o modulo main_transformLoad.py

        Execute a funcao uma primeira vez para pegar os novos labels, e informar nos argumentos que seguem.

    '''

    ## Carga da tabela de comissão
    extra = read_downaload().read_data(
                                        bank='facta', # informe o nome do banco conforme esta no diretorio criado
                                        date = date,
                                        type_transference = ['extra'],
                                        engine = ['excel'], # informe o engine para leitura
                                        decimal = ',',
                                        thousands = '.',
                                        sheet_name = 'data',
                                        # parse_dates=['DATA_REGISTRO', 'DATA_PAGAMENTO_CLIENTE', 'DATAEFETIVACAO'],
                                        # format_parse_dates='%d/%m/%Y',
                                        header = 0
                            )

    
    
    ## Codigo segue o fluxo se o arquivo for lido com sucesso
    if extra is not None:
        
        # metodo para limpeza de valores monetarios
        result = cleaningData().cleaning(dataFrame = extra,
                                                typeData = ['monetary'],
                                                columns_convert = ['credito'] # informe variaveis com valores monetarios, conforme exemplo
                                                )

        
        # metodo para transforacao dos valores monetarios
        final_production = transformationData().convert_monetary(dataFrame = result,
                                        columns_convert = ['credito'])


        final_production = final_production[final_production['tipocontacorretor'].isin([1, 54])][['codigoaf', 'credito', 'tipocontacorretor']]
        
        updateStaginAreaExtra().upDatating(contaCorrente = final_production)
        


# Debug
# CleaningExtra(date = datetime.date(2024, 8, 16))
