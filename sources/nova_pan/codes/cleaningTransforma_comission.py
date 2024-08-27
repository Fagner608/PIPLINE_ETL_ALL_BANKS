# imports

import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB

import datetime
from re import findall



def CleaningComission(date: datetime.date):

    '''
        Funcao para executar limpeza, tratamento e transformacao no relatorio de comissao
        ### date: argumnento setado no modulo main.py, quando chama o modulo main_transformLoad.py

        Execute a funcao uma primeira vez para pegar os novos labels, e informar nos argumentos que seguem.

    '''

    ## Carga da tabela de comissão
    comission = read_downaload().read_data(
                        bank='nova_pan', # informe o nome do banco conforme esta no diretorio criado
                        date = date,
                        type_transference = ['comission'],
                        engine = ['csv'], # informe o engine para leitura
                        decimal = '.',
                        encoding = 'ISO-8859-1',
                        header = 0,
                        parse_dates = ['DAT_CREDITO', 'DAT_EMPRESTIMO'],
                        format_parse_dates = ['%d/%m/%Y']
                        )

    ## Codigo segue o fluxo se o arquivo for lido com sucesso


    if comission is not None:
        comission = comission[comission.NOM_BANCO.str.contains('PAN')]
    

    if comission is not None and not comission.empty:
        result = comission

        # metodo para limpeza de valores monetarios
        result = cleaningData().cleaning(dataFrame = result,
                                        typeData = ['monetary'],
                                        columns_convert = ['val_base_comissao', 'val_comissao_total'] # informe variaveis com valores monetarios, conforme exemplo
                                        )

        # metodo para limpeza de strings
        # result = cleaningData().cleaning(dataFrame = result,
        #                                     typeData = ['string'],
                                        
        #                                 columns_convert =[] # informe variaveis que contenham as strings que deseja limpar (Não insira atributos que contenham: nome de cliente, Id de contrato ou proposta, número de contrato ou proposta, datas SE estes campos precisarem manter o valor original)
        #                                         )

        # metodo para transforacao dos valores monetarios
        final_comission = transformationData().convert_monetary(dataFrame = result,
                                    columns_convert = ['val_base_comissao', 'val_comissao_total'] # informe variaveis com valores monetarios, conforme exemplo
                                    )


        # Se necessario faca as demais alteracoes aqui
            #exemplo:
        # final_comission['codigo_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[0]
        # final_comission['nome_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[1]
        final_comission['codigo_tabela'] = final_comission['dsc_produto'].apply(
            lambda x: findall(r'\d{3,6}', x)[0] if findall(r'\d{3,6}', x) else findall(r'\d{3,3}', x)[0]
        )
        final_comission['dsc_produto'] = final_comission['dsc_produto'].map(lambda x: x.split(" - ")[0] if x.split(" - ") else x)         
        final_comission['dsc_produto'] = final_comission['dsc_produto'].map(lambda x: x.split("- ")[0] if x.split("- ") else x)         
        final_comission['dsc_tipo_proposta_emprestimo'] = final_comission['dsc_tipo_proposta_emprestimo'].str.upper()
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
    total_dict[0]['tipo'] = 'dsc_produto'

    # tabela tipo_operacao (ex: )
    total_dict[1]['nome_operacao'] = 'dsc_tipo_proposta_emprestimo'

    # Tabela cliente
    total_dict[2]['nome_cliente'] = 'nom_cliente'
    total_dict[2]['cpf_cliente'] = 'cod_cpf_cliente'

    # Tabela vendedor (exemplo: The One - como vier na fonte)
    total_dict[3]['nome_vendedor'] = ''
    total_dict[3]['codigo_vendedor'] = ''

    # Tabela usuario_substabelecido
    total_dict[4]['nome_usuario_substabelecido'] = ''
    total_dict[4]['codigo_usuario_substabelecido'] = ''

    # Tabela convenio (exemplo: Baixa Renda - como vier na fonte)
    total_dict[5]['nome_convenio'] = 'dsc_produto'
    total_dict[5]['codigo_convenio'] = ''

    # Tabela usuario_digitador_banco
    total_dict[6]['nome_usuario_digitador'] = ''
    total_dict[6]['codigo_usuario_digitador'] = ''

    # Tabela banco
    total_dict[7]['nome_banco'] = 'nom_banco'

    # Tabela tabela
    total_dict[8]['nome_tabela'] = 'dsc_tipo_proposta_emprestimo'
    total_dict[8]['codigo_tabela'] = 'codigo_tabela'

    # metodo que fara o input dos dados
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict)
    

# Debug
# CleaningComission(date=datetime.date.today())
# load_comission(date=datetime.date.today())