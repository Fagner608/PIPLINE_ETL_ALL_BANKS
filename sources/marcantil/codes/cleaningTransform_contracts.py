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
                        bank='crefisa', # informe o nome do banco conforme esta no diretorio criado
                        date = date,
                        type_transference = ['production'], # informe o relatorio em que estao as informacoes dos contratos
                        engine = ['html'],# informe o engine para leitura
                        decimal = ',',
                        thousands = '.',
                        parse_dates=['DATA_DIGIT_BANCO', 'DATA_PAGAMENTO_CLIENTE', 'DATA_PAGAMENTO_COMISSAO', 'DATA_FISICO_EMPRESA', 'DATA_SUB_STATUS'],
                        format_parse_dates='%d/%m/%Y',
                        header = 0
                    )
    ## Codigo segue o fluxo se o arquivo for lido com sucesso
    if contracts is not None:

        # metodo para limpeza de valores monetarios
        result = cleaningData().cleaning(dataFrame = contracts,
                                                typeData = ['monetary'],
                                                columns_convert = ['vlr_parc', 'valor_bruto', 'valor_liquido', 'valor_base', 'vlr_comissao_repasse', 'vlr_bonus_repasse'] # informe variaveis com valores monetarios, conforme exemplo
                                                )

        # metodo para limpeza de strings
        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                            columns_convert =['filial', 'grupo_vendedor', 'cod_vendedor', 'vendedor', 
                                                        'prazo',  'perc_comissao_repasse', 'cpf', 'sit_banco', 'sit_pagamento_cliente',
                                                        'banco', 'convenio', 'tabela', 'usuario_digit_banco',
                                                        'usuario_digit_banco_subestabelecido', 'sub_usuario',
                                                        'login_sub_usuario', 'situacao_pendencia', 'tipo_contrato',
                                                        'codigo_produto', 'codigo_convenio', 'fisico_empresa', 'usuário_fisico_empresa',
                                                        'sit_pagamento_comissao', 'sub_status', 'perc_bonus_repasse', 'numero_ade'
                                                        ] # informe variaveis que contenham as strings que deseja limpar (Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original)
                                                )

        # metodo para transforacao dos valores monetarios
        final_contracts = transformationData().convert_monetary(dataFrame = result,
                                        columns_convert = ['vlr_parc', 'valor_bruto', 'valor_liquido', 'valor_base', 'vlr_comissao_repasse', 'vlr_bonus_repasse'])


        # Se necessario faca as demais alteracoes aqui
            #exemplo:
            ## Spiit no tipo_contrato (001 - Novo Contrato)
        # final_contracts['tipo_contrato'] = final_contracts['tipo_contrato'].str.split("__", expand = True)[1]
        # final_contracts['usuario_digit_banco'] = final_contracts['usuario_digit_banco'].str.split("__", expand = True)[1]
        # final_contracts['cod_usuario_digit_banco'] = final_contracts['usuario_digit_banco'].str.split("__", expand = True)[0]
        # final_contracts['sub_usuario'] = final_contracts['sub_usuario'].str.split("_\(", expand = True)[0]
        
        # metodo par enviar os dados para staging_area no banco de dados
        saveStageArea().inputTable(table = final_contracts)
  

def load_contracts(date: datetime.date):

    
    '''
        Funcao que prepara os dados carregados na staging_area para carga definitiva no banco de dados

        ## FACA A SEGUINTE CONFIGURACAO:

        - atribua ao lado direito da chave,o label da variavel que sera setada no banco de dados, conforme exemplo abaixo. USe os labels tratados.

    '''

    # Atualizando valores na tabela staging_area
    updateStaginAreaContracts().upDatating(bank='INSIRA O BANCO')

    #lista para consultar os atributos das tabelas
    list_tables = ['contrato']

    # metodo que retornar os atributos que atualizaremos, na tabela em producao
    total_dict = inputsDB().totalAttributes(list_tables = list_tables)
    
    # preencher os atributos com o correspondente da tabela carregada no staging_area
    #Tabela tipo_contrato (ex: novo, margem_livre, etc - como vier na fonte)
    total_dict[0]['tipo_contrato'] = 'tipo_contrato'
    
    # status_importacao (sera enviado com default de nao_importado) - nao preencher
    # total_dict[0]['status_importacao'] = ''

    # tipo_operacao (a informacao depende do tipo de contrato)
    total_dict[0]['tipo_operacao'] = ''
    
    # numero
    total_dict[0]['numero_ade'] = ''
    
    #
    total_dict[0]['quantidade_parcela_prazo'] = ''
    
    #
    total_dict[0]['valor_parcela'] = ''
    
    total_dict[0]['valor_bruto'] = ''
    
    total_dict[0]['valor_liquido'] = ''
    
    total_dict[0]['valor_base'] = ''
    
    total_dict[0]['percentual_cms_repasse'] = ''
    
    total_dict[0]['valor_cms_repasse'] = ''
    
    total_dict[0]['percentual_bonus_repasse'] = ''
    
    total_dict[0]['valor_bonus_repasse'] = ''
    
    total_dict[0]['data_pagamento_cliente'] = ''
    
    total_dict[0]['percentual_cms_a_vista'] = ''
    
    total_dict[0]['valor_cms_a_vista'] = ''
    
    # tabela
    total_dict[0]['nome_tabela'] = ''

    # banco
    total_dict[0]['nome_banco'] = ''
    
    # usuario_digitador_banco
    total_dict[0]['codigo_usuario_digitador'] = ''
    
    # convenio
    total_dict[0]['nome_convenio'] = ''
    
    # usuario_substabelecido
    total_dict[0]['nome_usuario_substabelecido'] = ''
    
    #
    total_dict[0]['nome_vendedor'] = 'vendedor'

    # situacao
    total_dict[0]['situacao'] = 'sit_pagamento_cliente'
    
    # situacao
    total_dict[0]['cliente_id'] = 'cliente_id'
    


    # metodo que fara o input dos dados
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict, contractos = True, staging_area_contato = 'INSIRA O ATRIBUTO COM NUMERO DA ADE')
    

#Debug
# CleaningContracts(date=datetime.date(2024, 5, 24))
# load_contracts(date=datetime.date(2024, 5, 24))
