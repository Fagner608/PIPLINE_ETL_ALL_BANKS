# imports
import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime
from upDateStagingAreaContracts import updateStaginAreaContracts

# Funcao para executar limpeza, tratamento e transformacao
def CleaningContracts(date: datetime.date):

    '''
        Funcao para executar limpeza, tratamento e transformacao nos contratos (podem ser do relatorio de producao ou de comissao)
        ### date: argumnento setado no modulo main.py, quando chama o modulo main_transformLoad.py

        Execute a funcao uma primeira vez para pegar os novos labels, e informar nos argumentos que seguem.

    '''
    ## Carga da tabela desejada
    contracts = read_downaload().read_data(
                                        bank='v8', # informe o nome do banco conforme esta no diretorio criado
                                        date = date,
                                        type_transference = ['production'],
                                        engine = ['excel'], # informe o engine para leitura
                                        decimal = '.',
                                        thousands = ',',
                                        sheet_name = 0,
                                        # parse_dates=['DATA_REGISTRO', 'DATA_PAGAMENTO_CLIENTE', 'DATAEFETIVACAO'],
                                        # format_parse_dates='%d/%m/%Y',
                                        skiprows = 9,
                                        header = 0

                    )
    ## Codigo segue o fluxo se o arquivo for lido com sucesso
    if contracts is not None:
        contracts = contracts[contracts.columns[~contracts.columns.str.contains('Unnamed')].to_list()]
        # Retorna instancias dos atributros listados transformados
        # preencher com os labels transformados
        result = cleaningData().cleaning(dataFrame = contracts,
                                                typeData = ['monetary'],
                                                columns_convert = ['vlr_final', 'vlriof', 'vlrtac', 'vlrda_parcela',
                                                                   'vlr_emprestimo', 'valor_liberacao_1'] # informe variaveis com valores monetarios, conforme exemplo
                                                )

        # metodo para limpeza de strings
        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                            columns_convert =['descr_promotora', 'descr_tabela', 'descr_banco', 'descr_empregador', 'descr_orgao'
                                                              
                                                        ] # informe variaveis que contenham as strings que deseja limpar (Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original)
                                                )

        final_contracts =  transformationData().convert_monetary(dataFrame = result,
                                        columns_convert = ['vlr_final', 'vlriof', 'vlrtac', 'vlrda_parcela',
                                                                   'vlr_emprestimo', 'valor_liberacao_1'])


        ## faca aqui as demais transformacoes
        # Spiit no tipo_contrato (001 - Novo Contrato)
        # final_contracts['codigo_usuario_digitador'] = final_contracts['usuário_dig_banco'].str.split('__', expand = True)[0]
        # final_contracts['nome_usuario_digitador'] = final_contracts['usuário_dig_banco'].str.split('__', expand = True)[1]

        final_contracts = contracts
        # Input na staging_aread do DB
        saveStageArea().inputTable(table = final_contracts)
  

def load_contracts(date: datetime.date):

    
    '''
        Funcao que prepara os dados carregados na staging_area para carga definitiva no banco de dados

        ## FACA A SEGUINTE CONFIGURACAO:

        - atribua ao lado direito da chave,o label da variavel que sera setada no banco de dados, conforme exemplo abaixo. USe os labels tratados.

    '''

    # Atualizando valores na tabela staging_area
    updateStaginAreaContracts().upDatating(bank='V8 DIGITAL')

    #lista para consultar os atributos das tabelas
    list_tables = ['contrato']

    # metodo que retornar os atributos que atualizaremos, na tabela em producao
    total_dict = inputsDB().totalAttributes(list_tables = list_tables)
    
    # preencher os atributos com o correspondente da tabela carregada no staging_area
    #Tabela tipo_contrato (ex: novo, margem_livre, etc - como vier na fonte)
    total_dict[0]['tipo_contrato'] = 'nome_operacao'
    
    # status_importacao (sera enviado com default de nao_importado) - nao preencher
    # total_dict[0]['status_importacao'] = ''

    # tipo_operacao (a informacao depende do tipo de contrato)
    total_dict[0]['tipo_operacao'] = 'nome_operacao'
    
    # numero
    total_dict[0]['numero_ade'] = 'proposta'
    
    #
    total_dict[0]['quantidade_parcela_prazo'] = 'qtd_parcelas'
    
    #
    total_dict[0]['valor_parcela'] = ''
    
    total_dict[0]['valor_bruto'] = ''
    
    total_dict[0]['valor_liquido'] = 'vlr_emprestimo'
    
    total_dict[0]['valor_base'] = 'vlr_final'
    
    total_dict[0]['percentual_cms_repasse'] = 'percentual_cms_a_vista'
    
    total_dict[0]['valor_cms_repasse'] = 'vlr_de_comissao'
    
    total_dict[0]['percentual_bonus_repasse'] = ''
    
    total_dict[0]['valor_bonus_repasse'] = ''
    
    total_dict[0]['data_pagamento_cliente'] = 'data_cadastro'
    
    total_dict[0]['percentual_cms_a_vista'] = ''
    
    total_dict[0]['valor_cms_a_vista'] = ''
    
    # tabela
    total_dict[0]['nome_tabela'] = 'tabela_utilizada'

    # banco
    total_dict[0]['nome_banco'] = 'descr_promotora'
    
    # usuario_digitador_banco
    total_dict[0]['codigo_usuario_digitador'] = 'nome_usu_cad_proposta'
    
    # convenio
    total_dict[0]['nome_convenio'] = 'descr_tabela'
    
    # usuario_substabelecido
    total_dict[0]['nome_usuario_substabelecido'] = ''
     
    #
    total_dict[0]['nome_vendedor'] = ''

    # situacao
    total_dict[0]['situacao'] = 'sit_pagamento_cliente'
    
    # situacao
    total_dict[0]['cliente_id'] = 'cliente_id'
    


    # metodo que fara o input dos dados
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict, contracts = True, staging_area_contato = 'proposta')
    

#Debug
# CleaningContracts(date=datetime.date(2024, 8, 21))
# load_contracts(date=datetime.date(2024, 8, 21))
