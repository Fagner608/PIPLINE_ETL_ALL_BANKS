import warnings
warnings.filterwarnings("ignore")
# obter propostas
import pandas as pd
import datetime
import os
# Classe para relatorio de producao - recebe contratos nao importados, e cria relatorio
 # basta ajustar os campos que o storm espera receber
import sys
sys.path.append("../../modules")
from relatoriosNaoImportados_v8 import relatoriosNaoImportados
from enumClasses import Connector, Database
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')


from logger import loogerControls
import polars as pl


class comissionToStorm():
      


        def __init__(self):
            self.logger = loogerControls().loggerFunction()
            self.columns_to_rename = [
                                     '#ADE#',	
                                     '#VALOR_BASE#',
                                     '#PRAZO#',
                                     '#CODIGO_TABELA#',
                                     '#DATA_DIGITACAO#',
                                      "#TAX_INFORMADO#",
                                      "#TOMADA_DECISAO#",
                                      "#VALOR_CMS#",
                                      "#SPREAD_ESTIMADO#"
                                        ]
      
            self.columns_select = [
                                   "numero_proposta",
                                   "valor_desembolsado",
                                   "prazo",
                                   'table_namecode',
                                   "data_pagamento",
                                   "tac_total",
                                   "TOMADA_DECISAO",
                                   "VALOR_COMISSAO_ESTIMADO",
                                   "SPREAD_ESTIMADO"
                                   ]
            
            
            

        def comissionReport(self, date: datetime.date, provider: str):

            dados = relatoriosNaoImportados().naoImportados(provider=provider)
            if dados is not None:
                self.logger.info(f"Propostas nao importadas retornadas para o provider {provider}: {dados.shape[0]}")
                return dados
            else:
                 self.logger.info(f"Não existem propostas nao importadas para o provider {provider}.")
            
        def makeReport(self, date: datetime.datetime, provider: str):
            

            self.logger.info("Iniciando produção do relatório de comissão.")
            path_to_save = self.path_to_save = f"../../../Comissão/{date.year}/{date.month}/{date.day}/"
            os.makedirs(path_to_save, exist_ok=True)
            
            dados = self.comissionReport(date=date.date(), provider=provider)

            if dados is not None:

                self.logger.info("Iniciando tratamento.")
                try:               
                    dados = dados[self.columns_select]
                    
                    dados = dados.with_columns(pl.col('data_pagamento').dt.date())
                    dados = dados.rename(dict(zip(dados.columns, self.columns_to_rename)))
                    dados = dados.with_columns(pl.col("#VALOR_BASE#").alias("#VALOR_BASE_BRUTO#"))
                    dados_cms_correta = dados.filter(pl.col('#TOMADA_DECISAO#') == False)
                    dados_tomada_decisao = dados.filter(pl.col('#TOMADA_DECISAO#') == True)
                except Exception as exc:
                     self.logger.warning(f"Falha no tratamento e transformação final no relatório de comissao: {exc}")


                if not dados_cms_correta.is_empty():
                    try:
                        dados_cms_correta = dados_cms_correta.drop(['#TAX_INFORMADO#', '#SPREAD_ESTIMADO#', '#TOMADA_DECISAO#'])    
                        dados_cms_correta = dados_cms_correta.with_columns([
                            pl.col("#VALOR_CMS#").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("#VALOR_CMS#"),
                            pl.col("#VALOR_BASE#").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("#VALOR_BASE#"),
                            pl.col("#VALOR_BASE_BRUTO#").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("#VALOR_BASE_BRUTO#")
                        ])
                        dados_cms_correta.write_csv(path_to_save + f'{provider}_{date.strftime("%Y-%m-%d_%H_%M")}.csv', separator = ';')
                        self.logger.info("Relatorio de comissao salvo.")
                    except Exception as exc:
                        self.logger.critical(f"Falha ao salvar o relatorio final de comissao: {exc}")

                if not dados_tomada_decisao.is_empty():
                    
                    try:
                        dados_tomada_decisao = dados_tomada_decisao.drop(["#TOMADA_DECISAO#"])
                        dados_tomada_decisao = dados_tomada_decisao.with_columns([
                            pl.col("#VALOR_CMS#").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("#VALOR_CMS#"),
                            pl.col("#VALOR_BASE#").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("#VALOR_BASE#"),
                            pl.col("#VALOR_BASE_BRUTO#").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("#VALOR_BASE_BRUTO#"),
                            pl.col("#TAX_INFORMADO#").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("#TAX_INFORMADO#"),
                            pl.col("#SPREAD_ESTIMADO#").cast(float).map_elements(lambda x: locale.currency(float(x), symbol=False, grouping=True)).alias("#SPREAD_ESTIMADO#")
                        ])
                        dados_tomada_decisao.write_csv(path_to_save + f'{provider}_{date.strftime("%Y-%m-%d_%H_%M")}_TOMADA_DECISAO.csv', separator = ';')
                        self.logger.info("Relatorio tomada de comissao (tomada de decisao) salvo.")
                    except Exception as exc:
                        self.logger.critical(f"Falha ao salvar o relatório final de comissao (tomada de decisao): {exc}")




# debug     
# comissionToStorm().makeReport(date = datetime.datetime.today(), provider = 'BMS')