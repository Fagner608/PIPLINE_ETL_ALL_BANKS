# imports
import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea
from inputDataTransformed import inputsDB
import datetime
from re import findall
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


    if contracts is not None:
        contracts = contracts[contracts.NOM_BANCO.str.contains('PAN')]
    

    if contracts is not None and not contracts.empty:
        result = contracts

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
        final_contracts = transformationData().convert_monetary(dataFrame = result,
                                    columns_convert = ['val_base_comissao', 'val_comissao_total'] # informe variaveis com valores monetarios, conforme exemplo
                                    )


        # Se necessario faca as demais alteracoes aqui
            #exemplo:
        # final_contracts['codigo_usuario_digitador'] = final_contracts['usuário_dig_banco'].str.split('__', expand = True)[0]
        # final_contracts['nome_usuario_digitador'] = final_contracts['usuário_dig_banco'].str.split('__', expand = True)[1]
        final_contracts['codigo_tabela'] = final_contracts['dsc_produto'].apply(
            lambda x: findall(r'\d{3,6}', x)[0] if findall(r'\d{3,6}', x) else findall(r'\d{3,3}', x)[0]
        )
        final_contracts['dsc_produto'] = final_contracts['dsc_produto'].map(lambda x: x.split(" - ")[0] if x.split(" - ") else x)         
        final_contracts['dsc_produto'] = final_contracts['dsc_produto'].map(lambda x: x.split("- ")[0] if x.split("- ") else x)         
        final_contracts['dsc_tipo_proposta_emprestimo'] = final_contracts['dsc_tipo_proposta_emprestimo'].str.upper()
        # metodo par enviar os dados para staging_area no banco de dados
        saveStageArea().inputTable(table = final_contracts)


def load_contracts(date: datetime.date):

    
    '''
        Funcao que prepara os dados carregados na staging_area para carga definitiva no banco de dados

        ## FACA A SEGUINTE CONFIGURACAO:

        - atribua ao lado direito da chave,o label da variavel que sera setada no banco de dados, conforme exemplo abaixo. USe os labels tratados.

    '''

    # Atualizando valores na tabela staging_area
    updateStaginAreaContracts().upDatating(bank='BANCO PAN')

    #lista para consultar os atributos das tabelas
    list_tables = ['contrato']

    # metodo que retornar os atributos que atualizaremos, na tabela em producao
    total_dict = inputsDB().totalAttributes(list_tables = list_tables)
    
    # preencher os atributos com o correspondente da tabela carregada no staging_area
    #Tabela tipo_contrato (ex: novo, margem_livre, etc - como vier na fonte)
    total_dict[0]['tipo_contrato'] = 'dsc_produto'
    
    # status_importacao (sera enviado com default de nao_importado) - nao preencher
    # total_dict[0]['status_importacao'] = ''

    # tipo_operacao (a informacao depende do tipo de contrato)
    total_dict[0]['tipo_operacao'] = 'dsc_tipo_proposta_emprestimo'
    
    # numero
    total_dict[0]['numero_ade'] = 'num_proposta'
    
    #
    total_dict[0]['quantidade_parcela_prazo'] = 'qtd_parcela'
    
    #
    total_dict[0]['valor_parcela'] = ''
    
    total_dict[0]['valor_bruto'] = 'val_base_comissao'
    
    total_dict[0]['valor_liquido'] = 'val_base_comissao'
    
    total_dict[0]['valor_base'] = 'val_base_comissao'
    
    total_dict[0]['percentual_cms_repasse'] = ''
    
    total_dict[0]['valor_cms_repasse'] = 'val_comissao_total'
    
    total_dict[0]['percentual_bonus_repasse'] = ''
    
    total_dict[0]['valor_bonus_repasse'] = ''
    
    total_dict[0]['data_pagamento_cliente'] = 'dat_credito'
    
    total_dict[0]['percentual_cms_a_vista'] = ''
    
    total_dict[0]['valor_cms_a_vista'] = ''
    
    # tabela
    total_dict[0]['nome_tabela'] = 'codigo_tabela'

    # banco
    total_dict[0]['nome_banco'] = 'nom_banco'
    
    # usuario_digitador_banco
    total_dict[0]['codigo_usuario_digitador'] = ''
    
    # convenio
    total_dict[0]['nome_convenio'] = ''
    
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
                         total_dict = total_dict, contracts = True, staging_area_contato = 'num_proposta')
    

#Debug
# CleaningContracts(date=datetime.date.today())
# load_contracts(date=datetime.date.today())
