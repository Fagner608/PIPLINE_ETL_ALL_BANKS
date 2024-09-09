# imports

import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB

import datetime



def CleaningComission(date: datetime.date):

    '''
        Funcao para executar limpeza, tratamento e transformacao no relatorio de comissao
        ### date: argumnento setado no modulo main.py, quando chama o modulo main_transformLoad.py

        Execute a funcao uma primeira vez para pegar os novos labels, e informar nos argumentos que seguem.

    '''

    ## Carga da tabela de comissão
    comission = read_downaload().read_data(
                        bank='crefisa', # informe o nome do banco conforme esta no diretorio criado
                        date = date,
                        type_transference = ['comission'],
                        engine = ['csv'], # informe o engine para leitura
                        decimal = ',',
                        thousands = '.',
                        parse_dates=['PG Cliente'],
                        format_parse_dates='%d/%m/%Y',
                        header = 0
                    )

    ## Codigo segue o fluxo se o arquivo for lido com sucesso
    if comission is not None:
        result = comission

        # metodo para limpeza de valores monetarios
        result = cleaningData().cleaning(dataFrame = result,
                                        typeData = ['monetary'],
                                        columns_convert = ['valor_base', 'r$_à_vista', 'r$_bônus'] # informe variaveis com valores monetarios, conforme exemplo
                                        )


        # metodo para limpeza de strings
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
                                                        ] # informe variaveis que contenham as strings que deseja limpar (Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original)
                                                )

        # metodo para transforacao dos valores monetarios
        final_comission = transformationData().convert_monetary(dataFrame = result,
                                    columns_convert = ['valor_base', 'r$_à_vista', 'r$_bônus'] # informe variaveis com valores monetarios, conforme exemplo
                                    )


        # Se necessario faca as demais alteracoes aqui
            #exemplo:
        # final_comission['codigo_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[0]
        # final_comission['nome_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[1]
            
        # metodo par enviar os dados para staging_area no banco de dados
        saveStageArea().inputTable(table = final_comission)


def load_comission(date: datetime.date):

    '''
        Funcao que prepara os dados carregados na staging_area para carga definitiva no banco de dados

        ## FACA A SEGUINTE CONFIGURACAO:

        - atribua ao lado direito da chave,o label da variavel que sera setada no banco de dados, conforme exemplo abaixo. USe os labels tratados.

    '''


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
    total_dict[0]['tipo'] = 'tipo_contrato'

    # tabela tipo_operacao (ex: )
    total_dict[1]['nome_operacao'] = ''

    # Tabela cliente
    total_dict[2]['nome_cliente'] = ''
    total_dict[2]['cpf_cliente'] = ''

    # Tabela vendedor (exemplo: The One - como vier na fonte)
    total_dict[3]['nome_vendedor'] = ''
    total_dict[3]['codigo_vendedor'] = ''

    # Tabela usuario_substabelecido
    total_dict[4]['nome_usuario_substabelecido'] = ''
    total_dict[4]['codigo_usuario_substabelecido'] = ''

    # Tabela convenio (exemplo: Baixa Renda - como vier na fonte)
    total_dict[5]['nome_convenio'] = ''
    total_dict[5]['codigo_convenio'] = ''

    # Tabela usuario_digitador_banco
    total_dict[6]['nome_usuario_digitador'] = ''
    total_dict[6]['codigo_usuario_digitador'] = ''

    # Tabela banco
    total_dict[7]['nome_banco'] = ''

    # Tabela tabela
    total_dict[8]['nome_tabela'] = ''
    total_dict[8]['codigo_tabela'] = ''

    # metodo que fara o input dos dados
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict)
    

# Debug
# CleaningComission(date=datetime.date(2024,5,24))
# load_comission(date=datetime.date(2024,5,24))