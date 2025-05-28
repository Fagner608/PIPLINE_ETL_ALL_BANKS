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
from relatoriosNaoImportados import relatoriosNaoImportados_v8_bms
import tables_cod
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')



class productionToStorm():
      


        def __init__(self):
            self.columns_to_rename = [
                                     '#ADE#',	
                                     '#VALOR_BASE#',
                                     #'#VALOR_CMS#',
                                     '#PRAZO#',
                                     '#CODIGO_TABELA#',
                                     #'#VALOR_BASE_BRUTO#',
                                     '#DATA_DIGITACAO#',
                                     "TAX_INFORMADO"
                                        ]
      
            self.columns_select = [
                                   "NUMERO PROPOSTA",
                                   "VALOR LIBERADO",
                                   "NUMERO PARCELAS",
                                   'ID TABELA',
                                   "DATA DE PAGAMENTO",
                                   "TAX_INFORMADO"
                                   ]
            
            self.COMISSIONS_TAX_RATE_LIMIT = {
                                                "0001": 0.22,
                                                "0002": 0.21,
                                                "0003": 0.19,
                                                "0004": 0.16,
                                                "0005": 0.14,
                                                "0006": 0.22,
                                                "0007": 0.33,
                                                "0008": 0.33,
                                                "0009": 0.149,
                                                "0010": 0.189,
                                                "0011": 0.114,
                                                "0012": 0.33,
                                                "00BR": 0.2390,
                                                "0014": 0.189,
                                                "0015": 0.10,
                                                "0017": 0.2390,
                                                "0018": 0.25,
                                                "0019": 0.33,
                                                "0020": 0.25,
                                                "0021": 0.39,
                                                "0022": 0.39,
                                                "0023": 0.39,
                                                "0024": 0.39,
                                                "0025": 0.39,
                                                "0026": 0.39,
                                                "0027": 0.39,
                                                "0029": 0.60
                                            } 
            
            

        def productionReport(self, date: datetime.date, bank: str):
            dados = relatoriosNaoImportados_v8_bms().naoImportados(bank=bank)

            if not dados.empty:
                
                return dados
            
        def makeReport(self, date: datetime.datetime, bank: str):

            path_to_save = self.path_to_save = f"../../../Comissão/{date.year}/{date.month}/{date.day}/"
            
            dados = self.productionReport(date=date.date(), bank=bank)

            if dados is not None:
                
                dados = dados[self.columns_select]
                
                dados['DATA DE PAGAMENTO'] = pd.to_datetime(dados['DATA DE PAGAMENTO']).dt.date
                dados['ID TABELA'] = dados['ID TABELA'].map(tables_cod.tables)
                dados.columns = self.columns_to_rename
                dados.insert(2, '#VALOR_CMS#', "NA")
                dados.insert(5, '#VALOR_BASE_BRUTO#', dados['#VALOR_BASE#'])
                dados['#VALOR_CMS#'] = [round(float(j) * self.COMISSIONS_TAX_RATE_LIMIT[x[-4:]], 2) for x, j in zip(dados['#CODIGO_TABELA#'],dados['#VALOR_BASE#'])]
                dados['spread_estimado'] = [round(float(j) * 0.06, 2) for j in dados['#VALOR_BASE#']]
                ## compara valores de comissão calculados com tac recebida, se comissão for maior, fazer arquivo de tomada de decisão
                dados_cms_correta = dados[dados['#VALOR_CMS#'] <= (dados['TAX_INFORMADO'].astype(float) + dados['spread_estimado'])]
                dados_tomada_decisao = dados[dados['#VALOR_CMS#'] > (dados['TAX_INFORMADO'].astype(float) + dados['spread_estimado'])]
                
                os.makedirs(path_to_save, exist_ok=True)
                if not dados_cms_correta.empty:
                    dados_cms_correta.drop(['TAX_INFORMADO', 'spread_estimado'], axis = 1, inplace = True)    
                    dados_cms_correta['#VALOR_CMS#'] = dados_cms_correta['#VALOR_CMS#'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_cms_correta['#VALOR_BASE#'] = dados_cms_correta['#VALOR_BASE#'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_cms_correta['#VALOR_BASE_BRUTO#'] = dados_cms_correta['#VALOR_BASE_BRUTO#'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_cms_correta.to_csv(path_to_save + f'{bank}_{date.strftime("%Y-%m-%d_%H_%M")}.csv', index = False, sep = ';', encoding = 'latin1')
                
                if not dados_tomada_decisao.empty:
                    
                    dados_tomada_decisao['TAX_INFORMADO'] = dados_tomada_decisao['TAX_INFORMADO'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_tomada_decisao['spread_estimado'] = dados_tomada_decisao['spread_estimado'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_tomada_decisao['#VALOR_CMS#'] = dados_tomada_decisao['#VALOR_CMS#'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_tomada_decisao['#VALOR_BASE#'] = dados_tomada_decisao['#VALOR_BASE#'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_tomada_decisao['#VALOR_BASE_BRUTO#'] = dados_tomada_decisao['#VALOR_BASE_BRUTO#'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_tomada_decisao.to_csv(path_to_save + f'{bank}_{date.strftime("%Y-%m-%d_%H_%M")}_TOMADA_DECISAO.csv', index = False, sep = ';', encoding = 'latin1')

# debug     
# productionToStorm().makeReport(date = datetime.datetime.today(), bank = 'V8 DIGITAL')