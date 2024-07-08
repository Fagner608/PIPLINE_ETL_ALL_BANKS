import sys

sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime

from upDateStagingAreaProductionCrefisa import updateStaginAreaCrefisa
# Funcao para executar limpeza, tratamento e transformacao no crefisa

def crefisaCleaningProduction(date: datetime.date):

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
                                                        'banco', 'convenio', 'tabela', 'usuario_digit_banco',
                                                        'usuario_digit_banco_subestabelecido', 'sub_usuario',
                                                        'login_sub_usuario', 'situacao_pendencia', 'tipo_contrato',
                                                        'codigo_produto', 'codigo_convenio', 'fisico_empresa', 'usuário_fisico_empresa',
                                                        'sit_pagamento_comissao', 'sub_status', 'perc_bonus_repasse', 'numero_ade'
                                                        ]
                                                )

        final_production = transformationData().convert_monetary(dataFrame = result,
                                        columns_convert = ['vlr_parc', 'valor_bruto', 'valor_liquido', 'valor_base', 'vlr_comissao_repasse', 'vlr_bonus_repasse'])


        ## Spiit no tipo_contrato (001 - Novo Contrato)
        final_production['tipo_contrato'] = final_production['tipo_contrato'].str.split("__", expand = True)[1]
        saveStageArea().inputTable(table = final_production)





def load_crefisa_production(date: datetime.date):
    

    # Atualizando valores na tabela staging_area
    updateStaginAreaCrefisa().upDatating(bank='BANCO CREFISA')

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



    total_dict = inputsDB().totalAttributes(list_tables = list_tables)

    # preencher os atributos com o correspondente da tabela carregada no staging_area
    #Tabela tipo_contrato (ex: novo, margem_livre, etc - como vier na fonte)
    total_dict[0]['tipo'] = 'tipo_contrato'

    # tabela tipo_operacao (ex: )
    total_dict[1]['nome_operacao'] = ''

    # Tabela cliente
    total_dict[2]['nome_cliente'] = 'cliente'
    total_dict[2]['cpf_cliente'] = 'cpf'

    # Tabela vendedor (exemplo: The One - como vier na fonte)
    total_dict[3]['nome_vendedor'] = 'vendedor'
    total_dict[3]['codigo_vendedor'] = 'cod_vendedor'

    # Tabela usuario_substabelecido
    total_dict[4]['nome_usuario_substabelecido'] = ''
    total_dict[4]['codigo_usuario_substabelecido'] = ''

    # Tabela convenio (exemplo: Baixa Renda - como vier na fonte)
    total_dict[5]['nome_convenio'] = 'convenio'
    total_dict[5]['codigo_convenio'] = ''

    # Tabela usuario_digitador_banco
    total_dict[6]['nome_usuario_digitador'] = 'sub_usuario'
    total_dict[6]['codigo_usuario_digitador'] = 'login_sub_usuario'

    # Tabela banco
    total_dict[7]['nome_banco'] = 'banco'

    total_dict[8]['nome_tabela'] = 'tabela'
    total_dict[8]['codigo_tabela'] = 'codigo_produto'


    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict)
    

# Debug
# crefisaCleaningProduction(date = datetime.date(2024,6,18))
# load_crefisa_production(date = datetime.date(2024,6,18))
