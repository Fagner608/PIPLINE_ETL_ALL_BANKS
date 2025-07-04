# imports
import sys
import psycopg2 as ps
import polars as pl

# mudulos base
sys.path.append("../../modules")
from readDownload import read_downaload
from cleaningTransformaData import saveStageArea

from inputDataTransformed import inputsDB

from connectionDB import ConectionDB
from enumClasses import Connector, Database
from logger import loogerControls


class CleaningTempTable():


    def __init__(self) -> None:
        self.logger = loogerControls().loggerFunction()



    ## filtra propostas da temp_table
    def getProposals(self, db_name: str = Database.BM_BMS.value):

        query1 = '''

                            with notprocessed_filtred as (
                                select 
                                tt."NUMERO PROPOSTA"
                                from temp_table tt
                                where tt."NUMERO PROPOSTA" is null
                                or tt."CPF" is  null
                                or tt."NOME" is null
                                or tt."VALOR OPERACAO" is null
                                or tt."VALOR LIBERADO" is null
                                or tt."NUMERO PARCELAS" is null
                                or tt."TAX_INFORMADO" is null
                                or tt."ID VENDEDOR" is  null
                                or tt."ID TABELA" is null
                                or length(trim(tt."CPF")) != 11
                            ) insert into notprocessed("NUMERO PROPOSTA")
                            select nf."NUMERO PROPOSTA"
                            from notprocessed_filtred nf
                            where not exists(
                            select 1
                            from notprocessed np
                            where np."NUMERO PROPOSTA" = nf."NUMERO PROPOSTA"
                            )

                '''


        queryString = '''
        with notprocessed as (
            select 
            tt."NUMERO PROPOSTA"
            from temp_table tt
            where tt."NUMERO PROPOSTA" is null
            or tt."CPF" is  null
            or tt."NOME" is null
            or tt."VALOR OPERACAO" is null
            or tt."VALOR LIBERADO" is null
            or tt."NUMERO PARCELAS" is null
            or tt."TAX_INFORMADO" is null
            or tt."ID VENDEDOR" is  null
            or tt."ID TABELA" is null
            or length(trim(tt."CPF")) != 11
        ) delete from temp_table tmp using notprocessed np where tmp."NUMERO PROPOSTA" = np."NUMERO PROPOSTA"
        '''

        self.logger.info(f"Iniciando busca por propostas incompletas.")
        for i, query in enumerate([query1, queryString]):
            try:
                    con = ConectionDB().psycopgConnection(db_name)
                    cur = con.cursor()
                    cur.execute(query)
                    affected_rows = cur.rowcount # <-- captura o numero de linhas afetadas
                    con.commit()
                    if i == 0:
                          self.logger.info(f"Destacando propostas incompletas. Update rows: {affected_rows}")
                    else:
                          self.logger.info(f"Limpando base de dados. Update rows: {affected_rows}")
                           
                    cur.close()
                    con.close()
                    # self.logger.info(f"Update da tabela {k} - producao bem sucedido.")

            except Exception as exc:
                    self.logger.critical(f"Falha na busca por propostas incompletas: {exc}")
                    con.rollback()
                    self.logger.info("Rollback executado")
                    cur.close()
                    con.close()

    ## verifica se as propostas foram arrumadas
    def update(self, db_name: str = Database.BM_BMS.value):
         
        queryString = '''
                        with processed as (
                            select 
                            ct."numero_proposta"
                            from contrato ct
                        ) delete from notprocessed np using processed p where p."numero_proposta" = np."NUMERO PROPOSTA"
        '''

        self.logger.info(f"Iniciando atualizacao da tabela notprocessed.")
        try:
                    con = ConectionDB().psycopgConnection(db_name)
                    cur = con.cursor()
                    cur.execute(queryString)
                    affected_rows = cur.rowcount # <-- captura o numero de linhas afetadas
                    con.commit()
                    self.logger.info(f"Update rows: {affected_rows}")
                    cur.close()
                    con.close()
                    # self.logger.info(f"Update da tabela {k} - producao bem sucedido.")

        except Exception as exc:
                    self.logger.critical(f"Falha na atualização da tabela notprocessed: {exc}")
                    con.rollback()
                    self.logger.info("Rollback executado")
                    cur.close()
                    con.close()


    def count(self, db_name: str = Database.BM_BMS.value):
        try:
                    con = ConectionDB().psycopgConnection(db_name)
                    cur = con.cursor()
                    cur.execute('select count(*) from notprocessed')
                    result = cur.fetchone()[0]
                    if result != 0:
                        self.logger.warning(f"Existem propostas nao processadas: {result}")

                    cur.close()
                    con.close()

        except Exception as exc:
                    self.logger.critical(f"Falha na atualização da tabela notprocessed: {exc}")
                    con.rollback()
                    self.logger.info("Rollback executado")
                    cur.close()
                    con.close()

# CleaningTempTable().getProposals(batch_size = 1000, db_name=Database.BM_BMS.value)
