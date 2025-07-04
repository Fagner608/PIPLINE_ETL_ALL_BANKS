# obter propostas
import pandas as pd
import datetime
import os
# Classe para relatorio de producao - recebe contratos nao importados, e cria relatorio
 # basta ajustar os campos que o storm espera receber
import sys
sys.path.append("../../modules")
from relatoriosNaoImportados_v8 import relatoriosNaoImportados
from logger import loogerControls
from connectionDB import ConectionDB
from enumClasses import Connector, Database
import polars as pl


import tables_cod
from return_user_mail import retorna_conBFF, retorna_usermail
import psycopg2
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
import tables_cod
from dotenv import dotenv_values
####### AJUSTAR AS COLUNAS PARA A TABELA DE COMISSÃO CREFISA


class productionToStorm():
      
        def __init__(self):
            self.logger = loogerControls().loggerFunction()
            self.credentials = dotenv_values("../data/.env")
            self.columns_to_rename = [
                                        'PROPOSTA',	
                                        'DATA CADASTRO',	
                                        'CODIGO TABELA',	
                                        'NUMERO PARCELAS',	
                                        'VALOR OPERACAO',	
                                        'VALOR LIBERADO',	
                                        'CPF',	
                                        'NOME',	
                                        "TOMADA_DECISAO"
                                        ]


            self.columns_select = [
                                   "numero_proposta",
                                   "data_pagamento",
                                   'table_namecode',
                                   'prazo',
                                   "valor_emissao",
                                   "valor_desembolsado",
                                   "cpf_cliente",
                                   "nome_cliente",
                                   "TOMADA_DECISAO",
                                   "id_vendedor"

                                   ]



        def productionReport(self, date: datetime.date, provider: str):
            dados = relatoriosNaoImportados().naoImportados(provider=provider)
            if dados is not None:
                self.logger.info(f"Propostas nao importadas retornadas para o provider {provider}: {dados.shape[0]}")
                return dados
            else:
                 self.logger.info(f"Não existem propostas nao importadas para o provider {provider}.")
            
        def makeReport(self, date: datetime.datetime, provider: str):
            path_to_save = self.path_to_save = f"../../../Produção/{date.year}/{date.month}/{date.day}/"
            os.makedirs(path_to_save, exist_ok=True)
            
            dados = self.productionReport(date=date.date(), provider=provider)
            if dados is not None:
                dados = dados[self.columns_select]
                
                dados = dados.with_columns(pl.col("data_pagamento").dt.date())
                dados = dados.rename(dict(zip(dados.columns, self.columns_to_rename)))
                dados = dados.with_columns(pl.col("DATA CADASTRO").alias("DATA PAGAMENTO"))

                dados = dados.with_columns([
                            pl.col("VALOR OPERACAO").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("VALOR OPERACAO"),
                            pl.col("VALOR LIBERADO").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("VALOR LIBERADO")
                            ])
                dados = dados.with_columns(pl.lit("V8 DIGITAL").alias("BANCO"))
                dados = dados.with_columns(pl.lit("FGTS").alias("ORGAO"))
                dados = dados.with_columns(pl.lit("MARGEM LIVRE (NOVO)").alias("TIPO DE OPERACAO"))
                dados = dados.with_columns(pl.lit("SIM").alias("FORMALIZACAO DIGITAL"))
                dados = dados.with_columns(pl.lit("PAGO").alias("SITUACAO"))
                
                #### solução provisória até o Du arrumar o DB para trazer o email do digitador, e não do cliente ####
                self.logger.info("Iniciando busca por email dos usuarios no BFF")
                search = dados['id_vendedor'].to_list()
                search = ",".join(f"'{x}'" for x in search)
                con = ConectionDB().psycopgConnection(db_name = Database.BFF.value)

                all_data = []
                try:
                    for batch in pl.read_database(query = f"select id, email, partner_id from public.users where id in ({search})", 
                                          connection=con, 
                                          batch_size = 1000, 
                                          iter_batches=True):  


                        all_data.append(batch)
                        self.logger.info(f"Batch carregado: {batch.shape[0]} usuarios, do DB BFF")
                    
                    if all_data:
                        users = pl.concat(all_data)
                        self.logger.info(f"Obtendo usuarios do DB BFF")
                    else:
                        self.logger.warning("Usuarios nao retornados do DB BFF")
            
                except Exception as exc:
                        self.logger.critical(f"Erro inesperado ao buscar usuarios no DB BFF: {exc}")

                con.close()
                dados = dados.join(users.rename({'id': 'id_vendedor', 'email': 'USUARIO BANCO'}), on='id_vendedor', how='left')
                
                ## filtro
                dados = dados.with_columns(
                     pl.when(
                            (pl.col('partner_id') == '11864_SUPER006') & (pl.col('CODIGO TABELA') == 'QU0015')
                     ).then(pl.lit("BR0030"))
                     .otherwise(pl.col("CODIGO TABELA"))
                     .alias("CODIGO TABELA")
                )
                
                dados = dados.drop(['id_vendedor', 'partner_id'])

                dados_cms_correta = dados.filter(pl.col('TOMADA_DECISAO') == False)
                dados_tomada_decisao = dados.filter(pl.col('TOMADA_DECISAO') == True)
                
                
                if not dados_cms_correta.is_empty():
                    try:
                        dados_cms_correta = dados_cms_correta.drop(['TOMADA_DECISAO'])    
                        dados_cms_correta.write_csv(path_to_save + f'{provider}_{date.strftime("%Y-%m-%d_%H_%M")}.csv', separator = ';')
                        self.logger.info("Relatorio de producao salvo.")
                    except Exception as exc:
                        self.logger.critical(f"Falha ao salvar o relatorio final de producao: {exc}")

                if not dados_tomada_decisao.is_empty():
                    try:
                        dados_tomada_decisao = dados_tomada_decisao.drop(["TOMADA_DECISAO"])
                        dados_tomada_decisao.write_csv(path_to_save + f'{provider}_{date.strftime("%Y-%m-%d_%H_%M")}_TOMADA_DECISAO.csv', separator = ';')
                        self.logger.info("Relatorio tomada de producao (tomada de decisao) salvo.")
                    except Exception as exc:
                        self.logger.critical(f"Falha ao salvar o relatório final de producao (tomada de decisao): {exc}")
                    

# debug     
# productionToStorm().makeReport(date = datetime.datetime.today(), provider = 'BMS')