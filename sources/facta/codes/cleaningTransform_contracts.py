# imports
import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime
from upDateStagingAreaContractsFacta import updateStaginAreaContracts
# import cleaningTransform_extra

# Funcao para executar limpeza, tratamento e transformacao
def CleaningContracts(date: datetime.date):

    '''
        Funcao para executar limpeza, tratamento e transformacao nos contratos (podem ser do relatorio de producao ou de comissao)
        ### date: argumnento setado no modulo main.py, quando chama o modulo main_transformLoad.py

        Execute a funcao uma primeira vez para pegar os novos labels, e informar nos argumentos que seguem.

    '''
    ## Carga da tabela desejada
    contracts = read_downaload().read_data(
                        bank='facta', # informe o nome do banco conforme esta no diretorio criado
                        date = date,
                        type_transference = ['comission'],
                        engine = ['excel'], # informe o engine para leitura
                        decimal = '.',
                        thousands = ',',
                        sheet_name = 'data',
                        parse_dates=['DATA_REGISTRO', 'DATA_PAGAMENTO_CLIENTE', 'DATAEFETIVACAO'],
                        format_parse_dates='%d/%m/%Y',
                        header = 0
                    )
    ## Codigo segue o fluxo se o arquivo for lido com sucesso
    if contracts is not None:

        # metodo para limpeza de valores monetarios
        result = cleaningData().cleaning(dataFrame = contracts,
                                        typeData = ['monetary'],
                                        columns_convert = ['vl_liquido', 'vl_bruto', 'saldo_devedor', 'vl_comiss'] # informe variaveis com valores monetarios, conforme exemplo
                                        )


        # metodo para limpeza de strings
        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                        
                                        columns_convert =['ds_tabcom', 'numero_contrato'] # informe variaveis que contenham as strings que deseja limpar (Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original)
                                                )

        # metodo para transforacao dos valores monetarios
        final_contracts = transformationData().convert_monetary(dataFrame = result,
                                    columns_convert = ['vl_liquido', 'vl_bruto', 'saldo_devedor', 'vl_comiss'] # informe variaveis com valores monetarios, conforme exemplo
                                    )


        # Se necessario faca as demais alteracoes aqui
            #exemplo:
        final_contracts['codigo_tabela'] = final_contracts['ds_tabcom'].str.split('__', expand = True)[0]
        final_contracts['nome_tabela'] = final_contracts['ds_tabcom'].str.split('__', expand = True)[1]
            
        # metodo par enviar os dados para staging_area no banco de dados
        saveStageArea().inputTable(table = final_contracts)
  

def load_contracts(date: datetime.date):

    
    '''
        Funcao que prepara os dados carregados na staging_area para carga definitiva no banco de dados

        ## FACA A SEGUINTE CONFIGURACAO:

        - atribua ao lado direito da chave,o label da variavel que sera setada no banco de dados, conforme exemplo abaixo. USe os labels tratados.

    '''

    # Atualizando valores na tabela staging_area
    updateStaginAreaContracts().upDatating(bank = 'FACTA FINANCEIRA')
    
    # Fazendo conciliação com contaCorrente
    # CleaningExtra(date=date)
    
    #lista para consultar os atributos das tabelas
    list_tables = ['contrato']

    # metodo que retornar os atributos que atualizaremos, na tabela em producao
    total_dict = inputsDB().totalAttributes(list_tables = list_tables)
    
    # preencher os atributos com o correspondente da tabela carregada no staging_area
    #Tabela tipo_contrato (ex: novo, margem_livre, etc - como vier na fonte)
    total_dict[0]['tipo_contrato'] = 'tipo_operacao'
    
    # status_importacao (sera enviado com default de nao_importado) - nao preencher
    # total_dict[0]['status_importacao'] = ''

    # tipo_operacao (a informacao depende do tipo de contrato)
    total_dict[0]['tipo_operacao'] = 'tipo_operacao'
    
    # numero
    total_dict[0]['numero_ade'] = 'numero_contrato'
    
    #
    total_dict[0]['quantidade_parcela_prazo'] = 'numeroprestacao'
    
    #
    total_dict[0]['valor_parcela'] = ''
    
    total_dict[0]['valor_bruto'] = 'vl_bruto'
    
    total_dict[0]['valor_liquido'] = 'vl_liquido'
    
    total_dict[0]['valor_base'] = 'vl_liquido'
    
    total_dict[0]['percentual_cms_repasse'] = ''
    
    total_dict[0]['valor_cms_repasse'] = 'vl_comiss'
    
    total_dict[0]['percentual_bonus_repasse'] = ''
    
    total_dict[0]['valor_bonus_repasse'] = 'bonus'
    
    total_dict[0]['data_pagamento_cliente'] = 'data_pagamento_cliente'
    
    total_dict[0]['percentual_cms_a_vista'] = ''
    
    total_dict[0]['valor_cms_a_vista'] = 'vl_comiss'
    
    # tabela
    total_dict[0]['nome_tabela'] = 'nome_tabela'

    # banco
    total_dict[0]['nome_banco'] = 'banco'
    
    # usuario_digitador_banco
    total_dict[0]['codigo_usuario_digitador'] = ''
    
    # convenio
    total_dict[0]['nome_convenio'] = 'averbador'
    
    # usuario_substabelecido
    total_dict[0]['nome_usuario_substabelecido'] = ''
    
    #
    total_dict[0]['nome_vendedor'] = 'corretor'

    # situacao
    total_dict[0]['situacao'] = ''
    
    # situacao
    total_dict[0]['cliente_id'] = 'cliente_id'
    

    # metodo que fara o input dos dados
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict, contracts = True, staging_area_contato = 'numero_contrato')
    

#Debug
CleaningContracts(date=datetime.date(2024, 7, 23))
load_contracts(date=datetime.date(2024, 7, 23))
