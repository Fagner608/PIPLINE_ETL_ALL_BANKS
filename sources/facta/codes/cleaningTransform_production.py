# imports
import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime
from upDateStagingAreaProduction import updateStaginAreaFacta
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF8')

# Funcao para executar limpeza, tratamento e transformacao
def CleaningProduction(date: datetime.date):

    '''
        Funcao para executar limpeza, tratamento e transformacao no relatorio de comissao
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
        
        
        # metodo para limpeza de valores monetarios
        result = cleaningData().cleaning(dataFrame = production,
                                                typeData = ['monetary'],
                                                columns_convert = ['valor'] # informe variaveis com valores monetarios, conforme exemplo
                                                )

        # metodo para limpeza de strings
        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                            columns_convert =['cpf', 'averbador', 'banco', 'tipo_operação', 'status', 'análise_crivo', 'atendente/vendedor', 
                                                              'tabela_digitada', 'consulta_srcc', 'aceita_pela_ctc'
                                                        ] # informe variaveis que contenham as strings que deseja limpar (Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original)
                                                )
        
        # metodo para transforacao dos valores monetarios
        final_production = transformationData().convert_monetary(dataFrame = result,
                                        columns_convert = ['valor'])


        # Se necessario faca as demais alteracoes aqui
            #exemplo:
            ## Spiit no tipo_contrato (001 - Novo Contrato)
        # final_production['tipo_contrato'] = final_production['tipo_contrato'].str.split("__", expand = True)[1]
        final_production['codigo_tabela'] = final_production['tabela_digitada'].str.split("__", expand = True)[0]
        final_production['nome_tabela'] = final_production['tabela_digitada'].str.split("__", expand = True)[1]
        
        # metodo par enviar os dados para staging_area no banco de dados
        saveStageArea().inputTable(table = final_production)



def load_production(date: datetime.date):
    
    '''
        Funcao que prepara os dados carregados na staging_area para carga definitiva no banco de dados

        ## FACA A SEGUINTE CONFIGURACAO:

        - atribua ao lado direito da chave,o label da variavel que sera setada no banco de dados, conforme exemplo abaixo. USe os labels tratados.

    '''

    # Atualizando valores na tabela staging_area
    updateStaginAreaFacta().upDatating(bank='FACTA FINANCEIRA')
    
    #lista para consultar os atributos das tabelas
    list_tables = [
            'tipo_contrato',
            'tipo_operacao',
            'cliente',
            'vendedor',
            'usuario_substabelecido',
            'convenio',
            'usuario_digitador_banco',
            'banco',
            'tabela'
            ]


    # metodo que retornar os atributos que atualizaremos, na tabela em producao
    total_dict = inputsDB().totalAttributes(list_tables = list_tables)

    # preencher os atributos com o correspondente da tabela carregada no staging_area
    #Tabela tipo_contrato (ex: novo, margem_livre, etc - como vier na fonte)
    total_dict[0]['tipo'] = 'tipo_operação'

    # tabela tipo_operacao (ex: )
    total_dict[1]['nome_operacao'] = 'averbador'

    # Tabela cliente
    total_dict[2]['nome_cliente'] = 'nome'
    total_dict[2]['cpf_cliente'] = 'cpf'

    # Tabela vendedor (exemplo: The One - como vier na fonte)
        # total_dict[3]['nome_vendedor'] = ''
        # total_dict[3]['codigo_vendedor'] = ''

    # Tabela usuario_substabelecido
        # total_dict[4]['nome_usuario_substabelecido'] = ''
        # total_dict[4]['codigo_usuario_substabelecido'] = ''

    # Tabela convenio (exemplo: Baixa Renda - como vier na fonte)
        # total_dict[5]['nome_convenio'] = ''
        # total_dict[5]['codigo_convenio'] = ''

    # Tabela usuario_digitador_banco
        # total_dict[6]['nome_usuario_digitador'] = ''
        # total_dict[6]['codigo_usuario_digitador'] = ''

    # Tabela banco
    total_dict[7]['nome_banco'] = 'banco'

    # Tabela tabela
    total_dict[8]['nome_tabela'] = 'nome_tabela'
    total_dict[8]['codigo_tabela'] = 'codigo_tabela'


    # metodo que fara o input dos dados
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict)
    

# Debug
CleaningProduction(date = datetime.date(2024, 7, 23))
# load_production(date = datetime.date(2024, 7, 23))