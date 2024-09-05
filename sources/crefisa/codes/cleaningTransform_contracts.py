import sys

sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime


from upDateStagingAreaContractsCrefisa import updateStaginAreaCrefisa

# nocaso da cregisa, ferei a atualização usndo a tabela de produção
def crefisaCleaningContracts(date: datetime.date):

        # Trabalhando na tabela de produção
    production = read_downaload().read_data(
                        bank='crefisa',
                        date = date,
                        type_transference = ['production'],
                        engine = ['html'],
                        decimal = ',',
                        thousands = '.',
                        parse_dates=['DATA_DIGIT_BANCO', 'DATA_PAGAMENTO_CLIENTE', 'DATA_PAGAMENTO_COMISSAO', 'DATA_FISICO_EMPRESA', 'DATA_SUB_STATUS'],
                        format_parse_dates='%d/%m/%Y',
                        header = 0
                    )
    if production is not None:

        result = cleaningData().cleaning(dataFrame = production,
                                                typeData = ['monetary'],
                                                columns_convert = ['vlr_parc', 'valor_bruto', 'valor_liquido', 'valor_base', 'vlr_comissao_repasse', 'vlr_bonus_repasse'])


        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                            columns_convert =['filial', 'grupo_vendedor', 'cod_vendedor', 'vendedor', 
                                                        'prazo',  'perc_comissao_repasse', 'cpf', 'sit_banco', 'sit_pagamento_cliente',
                                                        'banco', 'convenio', 'tabela', 'sub_usuario','situacao_pendencia', 'tipo_contrato',
                                                        'codigo_produto', 'codigo_convenio', 'fisico_empresa', 'usuario_fisico_empresa',
                                                        'sit_pagamento_comissao', 'sub_status', 'perc_bonus_repasse', 'numero_ade'
                                                        ]
                                                )

        final_production = transformationData().convert_monetary(dataFrame = result,
                                        columns_convert = ['vlr_parc', 'valor_bruto', 'valor_liquido', 'valor_base', 'vlr_comissao_repasse', 'vlr_bonus_repasse'])


        ## Spiit no tipo_contrato (001 - Novo Contrato)
        final_production['tipo_contrato'] = final_production['tipo_contrato'].str.split("__", expand = True)[1]
        final_production['usuario_digit_banco'] = final_production['usuario_digit_banco'].str.split(" - ", expand = True)[1]
        final_production['cod_usuario_digit_banco'] = final_production['usuario_digit_banco'].str.split(" - ", expand = True)[0]
        final_production['sub_usuario'] = final_production['sub_usuario'].str.split("_\(", expand = True)[0]
        # print(final_production[['vlr_parc', 'valor_bruto', 'valor_liquido', 'valor_base', 'vlr_comissao_repasse', 'vlr_bonus_repasse']].head())
        saveStageArea().inputTable(table = final_production)





def load_contracts(date: datetime.date):
    
    # Atualizando valores na tabela staging_area
    updateStaginAreaCrefisa().upDatating(bank='BANCO CREFISA')
    
    list_tables = ['contrato']
    total_dict = inputsDB().totalAttributes(list_tables = list_tables)

    # preencher os atributos com o correspondente da tabela carregada no staging_area
    #Tabela tipo_contrato (ex: novo, margem_livre, etc - como vier na fonte)
    # Tipo de contrato
    total_dict[0]['tipo_contrato'] = 'tipo_contrato'
    
    # status_importacao (preciso pensar no gerenciamento do status)
    ## requer uma query auxiliar
    # total_dict[0]['status_importacao'] = ''

    # tipo_operacao (a informacao depende do tipo de contrato)
    ## requer uma query auxiliar
    total_dict[0]['tipo_operacao'] = 'tipo_contrato'
    
    # numero
    total_dict[0]['numero_ade'] = 'numero_ade'
    
    #
    total_dict[0]['quantidade_parcela_prazo'] = 'prazo'
    
    #
    total_dict[0]['valor_parcela'] = 'vlr_parc'
    
    total_dict[0]['valor_bruto'] = 'valor_bruto'
    
    total_dict[0]['valor_liquido'] = 'valor_liquido'
    
    total_dict[0]['valor_base'] = 'valor_base'
    
    total_dict[0]['percentual_cms_repasse'] = 'perc_comissao_repasse'
    
    total_dict[0]['valor_cms_repasse'] = 'vlr_comissao_repasse'
    
    total_dict[0]['percentual_bonus_repasse'] = 'perc_bonus_repasse'
    
    total_dict[0]['valor_bonus_repasse'] = 'vlr_bonus_repasse'
    
    total_dict[0]['data_pagamento_cliente'] = 'data_pagamento_cliente'
    
    total_dict[0]['percentual_cms_a_vista'] = ''
    
    total_dict[0]['valor_cms_a_vista'] = ''
    
    # tabela
    total_dict[0]['nome_tabela'] = 'codigo_produto'

    # banco
    total_dict[0]['nome_banco'] = 'banco'
    
    # usuario_digitador_banco
    total_dict[0]['codigo_usuario_digitador'] = 'login_sub_usuario'
    
    # convenio
    total_dict[0]['nome_convenio'] = 'convenio'
    
    # usuario_substabelecido
    total_dict[0]['nome_usuario_substabelecido'] = 'sub_usuario'
    
    #
    total_dict[0]['nome_vendedor'] = 'vendedor'

    # situacao
    total_dict[0]['situacao'] = 'sit_pagamento_cliente'
    
    # situacao
    total_dict[0]['cliente_id'] = 'cliente_id'
    


    # Input data
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict, contracts = True)
    

#Debug
# crefisaCleaningContracts(date=datetime.date.today())
# load_contracts(date=datetime.date(2024, 6, 24))
# print("finalizado")
