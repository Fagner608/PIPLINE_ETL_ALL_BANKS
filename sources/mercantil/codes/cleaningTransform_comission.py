import sys

## Importando modulos proprietarios
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB

# modulo para manipulacao de date
import datetime


# Funcao para executar limpeza, tratamento e transformacao no crefisa
def CleaningComission(date: datetime.date):

    '''
        Limpeza e transformação:

        1 -Funcao para limpar dados (como acentos e espaços em tranco), tranformar dados (unificando formato de valores monetários e datas) e
            1.1 - Utiliza metodos proprietarios para carga dos dados (read_download) para fazer a carga.
            1.2 - Utiliza metodos proprietarios para o tratamento de valores monetarios.
            1.3. Utiliza metodos proprietarios para o tratamento de strings.
            OBS: observe que, ao executar, o codigo retorna os labels das colunas transformados, voce deve preencher os argumentos das funcoes 'cleaning' e 'convert_monetary' com os labels transformados
            Apague as colunas de exemplo, e insira as corretas.
            Faça todas as alteracoes necessarias no dataset (como split dos dados) antes do input na staging_area.
    '''
    
    # Trabalhando na tabela de comissao
    comission = read_downaload().read_data(
                    bank='crefisa',
                    date = date,
                    type_transference = ['comission'],
                    engine = ['csv'],
                    decimal = '.',
                    thousands = ',',
                    parse_dates=['PG Cliente'],
                    format_parse_dates='%d/%m/%Y',
                    header = 0
                )



    # Retorna instancias dos atributros listados transformados
    # preencher com os labels transformados
    result = cleaningData().cleaning(dataFrame = comission,
                                    typeData = ['monetary'],
                                    columns_convert = ['valor_base'])
    

    # Retorna instancias dos atributros listados transformados
    # preencher com os labels transformados
    result = cleaningData().cleaning(dataFrame = result,
                                        typeData = ['string'],
                                    columns_convert =['físico']
                                            )

    final_comission = transformationData().convert_monetary(dataFrame = result,
                                    columns_convert = ['valor_base'])


    ## faca aqui as demais transformacoes
    # Spiit no tipo_contrato (001 - Novo Contrato)
    final_comission['codigo_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[0]
    final_comission['nome_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[1]



    # Input na staging_aread do DB
    saveStageArea().inputTable(table = final_comission)



def load_comission():
    
    '''
        Carga.
        Metodo para carga dos dados no DB de producao.
        Contem lista de tabelas editaveis do DB de producao.

        OBS: voce deve preencher as aspas vazias com o atributo que contenhas as instancias correspondentes ao atributo do
        banco de dados. Como exemplo, o atributo 'nome_cliente' da tabela cliente do DB de producao vai receber instancias do atributo 'cliente' do download;
        o atributo 'cpf_cliente' da tabela cliente do DB de producao vai receber instancias do atributo 'cpf' do download.

        Preencha com as informacoes corretas.

        O metodo loadInput faz o input dos dados.

    '''
    
    # Lista de tabelas editaveis do DB de producao
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



    # Retorna tabelas com estrutura necessarias para input dos dados
    total_dict = inputsDB().totalAttributes(list_tables = list_tables)

    # preencher os atributos com o correspondente da tabela carregada no staging_area
    #Tabela tipo_contrato (ex: novo, margem_livre, etc - como vier na fonte)
    total_dict[0]['tipo'] = ''

    # tabela tipo_operacao (ex: )
    total_dict[1]['nome_operacao'] = ''

    # Tabela cliente
    total_dict[2]['nome_cliente'] = 'cliente'
    total_dict[2]['cpf_cliente'] = 'cpf'

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

    total_dict[8]['nome_tabela'] = ''
    total_dict[8]['codigo_tabela'] = ''

    # Faz o input no DB de producao
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict)
    
