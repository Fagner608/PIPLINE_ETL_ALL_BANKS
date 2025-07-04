import sys
sys.path.append("../../modules")

from connectionDB import ConectionDB
from logger import loogerControls
from enumClasses import Connector, Database


# from sendActions import move_file
from os import makedirs, path, remove, listdir
import pandas as pd
import datetime
import query

import polars as pl


## classe para executar a query de extração das prospostas pagas
class Extract():

    def __init__(self) -> None:
        self.logger = loogerControls().loggerFunction()



    def executeQuery(self, date: datetime.datetime, batch_size: int, date_limit: int, db_name: str):
        

        # instanciando engine
        engine = ConectionDB().sqlalchemyConection(db_name)

        # instanciando instring
        queryString = query.MyQuery(date_work = date.date(), date_limit = date_limit)
        all_data = []
        # executando query
        try:
            # dados = pd.read_sql(queryString, con)
            self.logger.info(f'batch_size: {batch_size}')
            self.logger.info(f'date_limit: {date_limit}')
            with engine.connect() as conection:
                for batch in pl.read_database(query = queryString, 
                                            connection=conection, 
                                            batch_size = batch_size, 
                                            iter_batches=True): 


                    all_data.append(batch)
                    self.logger.info(f"Batch carregado: {batch.shape[0]} linhas, do DB railway")
            

            if all_data:
                dados = pl.concat(all_data)
                self.logger.info(f"Obtendo propostas do DB railway")
            else:
                self.logger.warning("Sem dados para os parametros retornados")
       
        
        except Exception as exc:
                self.logger.critical("Erro inesperado ao executar a query do DB railway")
        
        
        # verificando dados baixados
        if not dados.is_empty():
            
            self.logger.info(f"Dados retornados do DB: {Database.RAILWAY.value} - {dados.shape[0]} linhas")
            
            return dados
        else:
            self.logger.warning("Sem dados para os parametros retornados")
        


    def persist(self, date_work: datetime.datetime, batch_size: int = 1000, date_limit: int = 15, db_name: str = Database.RAILWAY.value):

        dados = self.executeQuery(date_work, batch_size=batch_size, date_limit = date_limit, db_name=db_name)

        if dados is not None:

            self.logger.info(f"Persistindo dados de producao")

            try:
                root = f'../download/{date_work.year}/{date_work.month}/production/'
                
                
                path_to_save = root + f'{date_work.date()}.parquet'
                makedirs(root, exist_ok=True)                
                dados.write_parquet(path_to_save)
                self.logger.info(f"Dados de producao {date_work.date()} persistidos com sucesso.")
            
            except Exception as exc:
                self.logger.error(f"Erro ao persistir dados de producao {date_work.date()}: {exc}.")

        else:
            self.logger.warning(f"Nao ha dados para a data {date_work.date()}")


# debug
# Extract().persist(date_work = datetime.datetime.today())