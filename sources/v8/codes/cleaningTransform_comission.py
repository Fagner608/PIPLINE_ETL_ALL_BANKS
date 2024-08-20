import sys

## Importando modulos proprietarios
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import upDateStagingAreaComission
# modulo para manipulacao de date
import datetime


# Funcao para executar limpeza, tratamento e transformacao no v8
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
                                        bank='v8', # informe o nome do banco conforme esta no diretorio criado
                                        date = date,
                                        type_transference = ['comission'],
                                        engine = ['csv'], # informe o engine para leitura
                                        encoding = 'latin1',
                                        sep = ';',
                                        # decimal = ',',
                                        # thousands = '.',
                                        # sheet_name = 0,
                                        # parse_dates=['pag_comissao'],
                                        # format_parse_dates='%Y/%m/%d',
                                        header = 0
                )



    if comission is not None:
        print(comission)
        comission.dropna(inplace = True)
        # Retorna instancias dos atributros listados transformados
        # preencher com os labels transformados
        result = cleaningData().cleaning(dataFrame = comission,
                                        typeData = ['monetary'],
                                        columns_convert = [])
        

        # Retorna instancias dos atributros listados transformados
        # preencher com os labels transformados
        result = cleaningData().cleaning(dataFrame = result,
                                            typeData = ['string'],
                                        columns_convert =['descricao', 'cpf']
                                                )

        # final_comission = transformationData().convert_monetary(dataFrame = result,
        #                                 columns_convert = ['vlr.liq', 'valor_comissão'])


        ## faca aqui as demais transformacoes
        # Spiit no tipo_contrato (001 - Novo Contrato)
        # final_comission['codigo_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[0]
        # final_comission['nome_usuario_digitador'] = final_comission['usuário_dig_banco'].str.split('__', expand = True)[1]


        final_comission = comission
        # Input na staging_aread do DB
        saveStageArea().inputTable(table = final_comission)



def load_comission(date: datetime.date):
    
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
    
    # TENHO QUE TRATAROS LABELS DAS COLUNAS E VALORES DA DESCRICAO
    upDateStagingAreaComission.updateStaginAreaComission().upDatating(bank = 'V8 DIGITAL')
    

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
    total_dict[0]['tipo'] = 'nome_operacao'

    # tabela tipo_operacao (ex: )
    total_dict[1]['nome_operacao'] = 'nome_operacao'

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
    total_dict[5]['nome_convenio'] = 'descricao'
    total_dict[5]['codigo_convenio'] = 'cod'

    # Tabela usuario_digitador_banco
    total_dict[6]['nome_usuario_digitador'] = ''
    total_dict[6]['codigo_usuario_digitador'] = ''

    # Tabela banco
    total_dict[7]['nome_banco'] = 'promotora'

    total_dict[8]['nome_tabela'] = ''
    total_dict[8]['codigo_tabela'] = ''

    # Faz o input no DB de producao
    inputsDB().loadInput(list_tables = list_tables,
                         total_dict = total_dict)

# debug   
date = datetime.date(2024, 8, 16) 
CleaningComission(date=date)
load_comission(date=date)