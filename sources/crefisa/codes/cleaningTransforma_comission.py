import sys

sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime


# Funcao para executar limpeza, tratamento e transformacao no crefisa

def crefisaCleaningComission(date: datetime.date):

        ## Trabalhando na tabela de comissão
    comission = read_downaload().read_data(
                        bank='crefisa',
                        date = date,
                        type_transference = ['comission'],
                        engine = ['csv'],
                        decimal = ',',
                        thousands = '.',
                        parse_dates=['PG Cliente'],
                        format_parse_dates='%d/%m/%Y',
                        header = 0
                    )


    if comission is not None:
        result = comission
        result = cleaningData().cleaning(dataFrame = result,
                                        typeData = ['monetary'],
                                        columns_convert = ['valor_base', 'r$_à_vista', 'r$_bônus'])


        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                        columns_convert =['físico',
                                                        'pendência',
                                                        'contrato_id',
                                                        'nº_proposta',
                                                        'cpf_cliente',
                                                        'banco',
                                                        'tipo_contrato',
                                                        '%_à_vista',
                                                        '%_bônus',
                                                        'usuário_dig_banco'
                                                        ]
                                                )

        final_comission = transformationData().convert_monetary(dataFrame = result,
                                    columns_convert = ['valor_base', 'r$_à_vista', 'r$_bônus'])

    
        final_comission['codigo_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[0]
        final_comission['nome_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[1]
        
        saveStageArea().inputTable(table = final_comission)

#obs: quando o DF retorna None, ex: sem df para data, a função abaixo não pode rodar


## Incluir aqui o código de iupdate do staging_area


def load_crefisa_comission(date: datetime.date):
    # leitura dos downloads nos formatos já conhecidos (pegar todos os formatos em que as tabelas estão sendo baixadas)
    # import sys
    # sys.path.append("../../modules")
    # from readDownload import read_downaload
    # # Limpeza, # Tratamento, # Transformação
    # from cleaningTransformaData import cleaningData, transformationData, saveStageArea
    
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



    total_dict = inputsDB().totalAttributes(list_tables = list_tables)

    # preencher os atributos com o correspondente da tabela carregada no staging_area
    total_dict[0]['tipo'] = 'tipo_contrato'

    total_dict[1]['nome_operacao'] = ''

    total_dict[2]['nome_cliente'] = 'nome_cliente'
    total_dict[2]['cpf_cliente'] = 'cpf_cliente'

    total_dict[3]['nome_vendedor'] = ''
    total_dict[3]['codigo_vendedor'] = ''

    total_dict[4]['nome_usuario_substabelecido'] = ''
    total_dict[4]['codigo_usuario_substabelecido'] = ''

    total_dict[5]['nome_convenio'] = ''
    total_dict[5]['codigo_convenio'] = ''

    total_dict[6]['nome_usuario_digitador'] = 'nome_usuario_digitador'
    total_dict[6]['codigo_usuario_digitador'] = 'codigo_usuario_digitador'

    total_dict[7]['nome_banco'] = 'banco'

    total_dict[8]['nome_tabela'] = ''
    total_dict[8]['codigo_tabela'] = ''

    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict)
    

#Debug
# crefisaCleaningComission(date=datetime.date(2024,5,24))
# load_crefisa_comission(date=datetime.date(2024,5,24))
