# obter propostas
import pandas as pd
import datetime
import os
# Classe para relatorio de producao - recebe contratos nao importados, e cria relatorio
 # basta ajustar os campos que o storm espera receber
import sys
sys.path.append("../../modules")
from relatoriosNaoImportados import relatoriosNaoImportados


####### AJUSTAR AS COLUNAS PARA A TABELA DE COMISSÃO CREFISA


class comissionToStorm():
      
        def __init__(self):
            self.columns_to_rename = ['#ADE#',	
                                      '#VALOR_BASE#',	
                                      '#VALOR_CMS#',	
                                      '#PRAZO#',	
                                      '#DATA_DIGITACAO#',	
                                      '#CODIGO_TABELA#',
                                      '#VALOR_BASE_BRUTO#'	
                                      ]
      
		


            self.columns_select = [
                                   "numero_ade",
                                   "valor_liquido",
                                   'valor_cms_repasse',
                                   "quantidade_parcela_prazo",
                                   "data_pagamento_cliente",	
                                   "nome_tabela",
                                   'tipo_operacao'
                                   
                                   ]


        def comissionReport(self, date: datetime.date, bank: str):
            dados = relatoriosNaoImportados().naoImportados(bank=bank)

            
            if not dados.empty:
                
                dados.drop(['contrato_id', 'cliente_id'], axis = 1, inplace = True)
                
                return dados
            
        def makeReport(self, date: datetime.date, bank: str):
            path_to_save = self.path_to_save = f"../../../Comissão/{date.year}/{date.month}/{date.day}/"
            
            dados = self.comissionReport(date=date, bank=bank)

            if dados is not None:
                dados = dados[self.columns_select]

                dados['#VALOR_BASE_BRUTO#'] = dados['valor_liquido']
                # dados['data_pagamento_cliente'] = pd.to_datetime(dados['data_pagamento_cliente'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%d/%m/%Y")
                cartao = dados[dados["tipo_operacao"].str.contains("Cartão|CARTÃƒO|CARTÃO")]
                normal = dados[~dados["tipo_operacao"].str.contains("Cartão|CARTÃƒO|CARTÃO")]
                cartao.drop(['tipo_operacao'], axis = 1, inplace = True)
                normal.drop(['tipo_operacao'], axis = 1, inplace = True)
                cartao.columns = self.columns_to_rename
                normal.columns = self.columns_to_rename
                os.makedirs(path_to_save, exist_ok=True)
                if not cartao.empty:
                    cartao['#TIPO_COMISSAO#'] = 'FLAT'
                    cartao.drop(['#DATA_DIGITACAO#'], axis = 1, inplace = True)
                    cartao.columns = ['#ADE#', '#VALOR_BASE#',	'#VALOR_CMS_CARTAO#', '#PRAZO#', '#CODIGO_TABELA#', '#VALOR_BASE_BRUTO#', '#TIPO_COMISSAO#']
                    cartao['#PREV_CMS_DIFERIDA#'] = ""
                    cartao.to_csv(path_to_save + f'CARTAO {bank}_{date}.csv', index = False, sep = ';')
                if not normal.empty:
                    normal['#PREV_CMS_DIFERIDA#'] = ""
                    normal.to_csv(path_to_save + f'{bank}_{date}.csv', index = False, sep = ';')


# debug     
# comissionToStorm().makeReport(date = datetime.date.today(), bank = 'BANCO PAN')