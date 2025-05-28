# imports
import sys
# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import cleaningData, transformationData, saveStageArea_BMS
from inputDataTransformed import inputsDB
import datetime
from upDateStagingAreaContracts import updateStaginAreaContracts


EXECUTE_NEXT_STEP = False

# Funcao para executar limpeza, tratamento e transformacao
def CleaningContracts(date: datetime.date):

    '''
        Funcao para executar limpeza, tratamento e transformacao nos contratos (podem ser do relatorio de producao ou de comissao)
        ### date: argumnento setado no modulo main.py, quando chama o modulo main_transformLoad.py

        Execute a funcao uma primeira vez para pegar os novos labels, e informar nos argumentos que seguem.

    '''
    global EXECUTE_NEXT_STEP
    EXECUTE_NEXT_STEP = False
    ## Carga da tabela desejada
    contracts = read_downaload().read_data(
                        bank='v8_bms', # informe o nome do banco conforme esta no diretorio criado
                        date = date,
                        type_transference = ['production'],
                        engine = ['parquet'], # informe o engine para leitura

                    )
    ## Codigo segue o fluxo se o arquivo for lido com sucesso
    if contracts is not None:
        EXECUTE_NEXT_STEP = True
        # metodo para limpeza de valores monetarios
        # result = cleaningData().cleaning(dataFrame = contracts,
        #                                         typeData = ['monetary'],
        #                                         columns_convert = ['iof_total', 'tac_total'] # informe variaveis com valores monetarios, conforme exemplo
        #                                         )


        # # metodo para transforacao dos valores monetarios
        # final_contracts = transformationData().convert_monetary(dataFrame = result,
        #                                 columns_convert = ['iof_total', 'tac_total'])


        final_contracts = contracts
        final_contracts.columns = ["NUMERO PROPOSTA", "STATUS", "NOME", "USUARIO BANCO", "TELEFONE", "CPF", "VALOR OPERACAO", "VALOR LIBERADO", "NUMERO PARCELAS", "DATA DE PAGAMENTO", "DATA DE CRIACAO", "IOF TOTAL", "TAXA TAC", "TAX_INFORMADO", "ID VENDEDOR", "ID TABELA"]
        
        saveStageArea_BMS().inputTable(table = final_contracts)
        # metodo par enviar os dados para uma tabela temporária no DB
        ## trocar por um DB postgres
  

### na staginarea faz a conferência de contratos duplicados e sobe com as varia´veis pra verificação do status.
# então, não vou usar o resto do código


# criar uma tabela para armezar os contratos com o schame acima
def load_contracts(date: datetime.date):

    
    '''
        Funcao que prepara os dados carregados na staging_area para carga definitiva no banco de dados

        ## FACA A SEGUINTE CONFIGURACAO:

        - atribua ao lado direito da chave,o label da variavel que sera setada no banco de dados, conforme exemplo abaixo. USe os labels tratados.

    '''

    if EXECUTE_NEXT_STEP:

        # Aqui a tabela será atualizada para incluir o que falta
        updateStaginAreaContracts().upDatating(bank='V8 DIGITAL')

        # ## inserir código para transferir da temp_table para a tabela de produção

        ###### inserir aqui o status importação####################################


        query_insert_contracts = f'''
                            
                            INSERT INTO contratos_bms ("NUMERO PROPOSTA", "STATUS", "NOME", "USUARIO BANCO", "TELEFONE", "CPF",
                                                        "VALOR OPERACAO", "VALOR LIBERADO", "NUMERO PARCELAS", "DATA DE PAGAMENTO",
                                                        "DATA DE CRIACAO", "IOF TOTAL", "TAXA TAC", "TAX_INFORMADO",
                                                        "ID VENDEDOR", "ID TABELA", "BANCO", "PROVEDOR", "ORGAO",
                                                        "TIPO_DE_OPERACAO", "SITUACAO", "FORMALIZACAO_DIGITAL", "status_importacao")
                            SELECT DISTINCT "NUMERO PROPOSTA", "STATUS", "NOME", "USUARIO BANCO", "TELEFONE", "CPF",
                                            "VALOR OPERACAO", "VALOR LIBERADO", "NUMERO PARCELAS", "DATA DE PAGAMENTO",
                                            "DATA DE CRIACAO", "IOF TOTAL", "TAXA TAC", "TAX_INFORMADO",
                                            "ID VENDEDOR", "ID TABELA", "BANCO", "PROVEDOR", "ORGAO",
                                            "TIPO_DE_OPERACAO", "SITUACAO", "FORMALIZACAO_DIGITAL", "status_importacao"
                            FROM temp_table
                            WHERE temp_table."NUMERO PROPOSTA" IS NOT NULL  -- Filtra valores nulos
                                AND NOT EXISTS (
                                    SELECT 1
                                    FROM contratos_bms
                                    WHERE contratos_bms."NUMERO PROPOSTA" = temp_table."NUMERO PROPOSTA"
                                );
                        '''

        try:
            con, cur = inputsDB().conDatabaseBMS()
            cur.execute(query_insert_contracts)
            con.commit()
            cur.close()
            con.close()

        except Exception as exc:
            print(f"Erro ao registrar contratos no DB: {exc}")
            con.commit()
            cur.close()
            con.close()
            raise


#Debug
# CleaningContracts(date=datetime.date.today())
# load_contracts(date=datetime.date.today())