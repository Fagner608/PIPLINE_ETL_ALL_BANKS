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
from return_user_mail import retorna_conBFF, retorna_usermail
import psycopg2
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
import tables_cod
from dotenv import dotenv_values
####### AJUSTAR AS COLUNAS PARA A TABELA DE COMISSÃO CREFISA


class comissionToStorm():
      
        def __init__(self):
            self.credentials = dotenv_values("../data/.env")
            self.columns_to_rename = [
                                        'PROPOSTA',	
                                        'DATA CADASTRO',	
                                        'BANCO',	
                                        'ORGAO',	
                                        'CODIGO TABELA',	
                                        'TIPO DE OPERACAO',	
                                        'NUMERO PARCELAS',	
                                        'VALOR OPERACAO',	
                                        'VALOR LIBERADO',	
                                        'USUARIO BANCO',	
                                        'SITUACAO',	
                                        #'DATA DE PAGAMENTO',	
                                        'CPF',	
                                        'NOME',	
                                        'FORMALIZACAO DIGITAL',
                                        "TAX_INFORMADO"
                                        ]


                       
            
            # ['#ADE#',	
            #                           '#VALOR_BASE#',	
            #                           '#VALOR_CMS#',	
            #                           '#VALOR_BONUS#',	
            #                           '#PRAZO#',	
            #                           '#DATA_DIGITACAO#',	
            #                           '#CODIGO_TABELA#',	
            #                           '#VALOR_BASE_BRUTO#']
      		


            self.columns_select = [
                                   "NUMERO PROPOSTA",
                                   "DATA DE PAGAMENTO",
                                   'BANCO',
                                   "ORGAO",
                                   'ID TABELA',
                                   "TIPO_DE_OPERACAO",
                                   'NUMERO PARCELAS',
                                   "VALOR OPERACAO",
                                   "VALOR LIBERADO",
                                   "USUARIO BANCO",
                                   "SITUACAO",
                                   "CPF",
                                   "NOME",
                                   "FORMALIZACAO_DIGITAL",
                                   "ID VENDEDOR",
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

        def comissionReport(self, date: datetime.date, bank: str):
            dados = relatoriosNaoImportados_v8_bms().naoImportados(bank=bank)

            if not dados.empty:
                
                return dados
            
        def makeReport(self, date: datetime.datetime, bank: str):
            path_to_save = self.path_to_save = f"../../../Produção/{date.year}/{date.month}/{date.day}/"
            
            dados = self.comissionReport(date=date.date(), bank=bank)

            if dados is not None:
                dados = dados[self.columns_select]

                ## data cadastro
                dados['DATA DE PAGAMENTO'] = pd.to_datetime(dados['DATA DE PAGAMENTO']).dt.date
                ## código tabela
                dados['ID TABELA'] = dados['ID TABELA'].map(tables_cod.tables)
                ## inserir nome certo do usuario
                engine = psycopg2.connect(
                    host = self.credentials['HOSTBFF'],
                    dbname = self.credentials['USERBFF'],
                    user = self.credentials['USERBFF'],
                    password = self.credentials['PASSWORDBFF'],
                    port = self.credentials['PORTBFF'],
                    sslmode = 'require'
                )
                result_query = []
                search = dados['ID VENDEDOR'].to_list()
                for idx, mail in enumerate(search):
                    try:
                        result = pd.read_sql(f"select email from public.users where id = '{mail}'", con=engine)
                        result_query.append(result['email'][0])
                    except Exception:
                        result_query.append("NA")
                        continue
                engine.close()
                dados['USUARIO BANCO'] = result_query
                dados.drop(['ID VENDEDOR'], axis = 1, inplace = True)

                dados.columns = self.columns_to_rename
                dados.insert(11, "DATA DE PAGAMENTO", dados['DATA CADASTRO'])

                ## calculando tomada decisao
                dados['#VALOR_CMS#'] = [round(float(j) * self.COMISSIONS_TAX_RATE_LIMIT[x[-4:]], 2) for x, j in zip(dados['CODIGO TABELA'],dados['VALOR LIBERADO'])]
                dados['spread_estimado'] = [round(float(j) * 0.06, 2) for j in dados['VALOR LIBERADO']]
                ## compara valores de comissão calculados com tac recebida, se comissão for maior, fazer arquivo de tomada de decisão
                dados_cms_correta = dados[dados['#VALOR_CMS#'] <= (dados['TAX_INFORMADO'].astype(float) + dados['spread_estimado'])]
                dados_tomada_decisao = dados[dados['#VALOR_CMS#'] > (dados['TAX_INFORMADO'].astype(float) + dados['spread_estimado'])]
                dados_cms_correta.drop(['TAX_INFORMADO', 'spread_estimado', '#VALOR_CMS#'], axis = 1, inplace = True)
                dados_tomada_decisao.drop(['TAX_INFORMADO', 'spread_estimado', '#VALOR_CMS#'], axis = 1, inplace = True)
                
                os.makedirs(path_to_save, exist_ok=True)
                if not dados_cms_correta.empty:
                    dados_cms_correta['VALOR OPERACAO'] = dados_cms_correta['VALOR OPERACAO'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_cms_correta['VALOR LIBERADO'] = dados_cms_correta['VALOR LIBERADO'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_cms_correta.to_csv(path_to_save + f'{bank}_{date.strftime("%Y-%m-%d_%H_%M")}.csv', index = False, sep = ';', encoding='latin1')

                if not dados_tomada_decisao.empty:
                    dados_tomada_decisao['VALOR OPERACAO'] = dados_tomada_decisao['VALOR OPERACAO'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_tomada_decisao['VALOR LIBERADO'] = dados_tomada_decisao['VALOR LIBERADO'].map(lambda x: locale.currency(float(x), symbol=False, grouping=True))
                    dados_tomada_decisao.to_csv(path_to_save + f'{bank}_{date.strftime("%Y-%m-%d_%H_%M")}_TOMADA_DECISAO.csv', index = False, sep = ';', encoding='latin1')




# debug     
# comissionToStorm().makeReport(date = datetime.datetime.today(), bank = 'V8 DIGITAL')