# obter propostas
import pandas as pd
import datetime
import os
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
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
                                    #   '#VALOR_BONUS#',	
                                    #   '#PRAZO#',	
                                    #   '#DATA_DIGITACAO#',	
                                    #   '#CODIGO_TABELA#',	
                                    #   '#VALOR_BASE_BRUTO#'
                                    ]
      
		


            self.columns_select = [
                                   "numero_ade",
                                   "valor_liquido",
                                   'valor_cms_repasse',
                                #    'valor_bonus_repasse',
                                #    "quantidade_parcela_prazo",
                                #    "data_pagamento_cliente",	
                                #    "nome_tabela"
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

                # dados['data_pagamento_cliente'] = pd.to_datetime(dados['data_pagamento_cliente'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%d/%m/%Y")
                dados['valor_cms_repasse'] = dados['valor_cms_repasse'].map(lambda x: locale.currency(x, symbol=False, grouping=True))
                dados.columns = self.columns_to_rename
                dados['#TIPO_COMISSAO#'] = "FLAT"
                os.makedirs(path_to_save, exist_ok = True)
                dados.to_csv(path_to_save + f'{bank}_{date}.csv', index = False, sep = ';', encoding = 'latin1')

# debug     
# comissionToStorm().makeReport(date = datetime.date.today(), bank = 'V8 DIGITAL')
