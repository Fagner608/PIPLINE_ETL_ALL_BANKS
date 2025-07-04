from connectionDB import ConectionDB
from enumClasses import Connector, Database
from logger import loogerControls
logger = loogerControls().loggerFunction()

import updateQuerys


def updateProdTables(db_name: str = Database.BM_BMS.value):
    

    list_querys_to_execute = {'cliente': updateQuerys.updateClient,
                              'contrato': updateQuerys.updateContrato
                              }

    for k, v in list_querys_to_execute.items():
        logger.info(f"Iniciando update da {k} - producao.")
        try:
                con = ConectionDB().psycopgConnection(db_name)
                cur = con.cursor()
                cur.execute(v)
                affected_rows = cur.rowcount # <-- captura o numero de linhas afetadas
                con.commit()
                logger.info(f"Update rows: {affected_rows} da tabela {k} - producao bem sucedido")
                cur.close()
                con.close()
                # logger.info(f"Update da tabela {k} - producao bem sucedido.")

        except Exception as exc:
                logger.critical(f"Falha no update da {k} - producao: {exc}")
                con.rollback()
                logger.info("Rollback executado")
                cur.close()
                con.close()