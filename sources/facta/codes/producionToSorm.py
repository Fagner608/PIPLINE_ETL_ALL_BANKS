# obter propostas
import pandas as pd
import datetime
import os

# Classe para relatorio de producao - recebe contratos nao importados, e cria relatorio
 # basta ajustar os campos que o storm espera receber
import sys
sys.path.append("../../modules")
from relatoriosNaoImportados import relatoriosNaoImportados

class productionToStorm():
      
        def __init__(self):
            self.columns_to_rename = ['PROPOSTA',
                                        'DATA CADASTRO',
                                        'BANCO',
                                        'ORGAO',
                                        'CODIGO TABELA',
                                        'TIPO DE OPERACAO',
                                        'NUMERO PARCELAS',
                                        'VALOR PARCELAS',
                                        'VALOR OPERACAO',
                                        'USUARIO BANCO',
                                        'SITUACAO',
                                        'DATA DE PAGAMENTO',
                                        'CPF',
                                        "NOME",
                                        'FORMALIZACAO DIGITAL'

                                        ]
      
            self.columns_select = [
                                   "numero_ade",
                                   "data_pagamento_cliente",	
                                   "nome_banco",
                                   "nome_convenio",
                                   "nome_tabela",
                                   "tipo_operacao",
                                   "quantidade_parcela_prazo",
                                   "valor_parcela",
                                   "valor_liquido",
                                   "codigo_usuario_digitador",
                                   "situacao",
                                #    "data_pagamento_cliente",
                                   'cpf_cliente',
                                   'nome_cliente',
                                   'formalizacao_digial'
                                   ]


        def productionReport(self, date: datetime.date, bank: str):
            dados = relatoriosNaoImportados().naoImportados(bank=bank)

            
            if not dados.empty:
                
                dados.drop(['contrato_id', 'cliente_id'], axis = 1, inplace = True)
                return dados
            
        def makeReport(self, date: datetime.date, bank: str):
            path_to_save = self.path_to_save = f"../../../Produção/{date.year}/{date.month}/{date.day}/"
            
            dados = self.productionReport(date=date, bank=bank)

            if dados is not None:
                dados = dados[self.columns_select]
                dados['data_pagamento_cliente'] = pd.to_datetime(dados['data_pagamento_cliente'], format='%Y-%m-%d %H:%M:%S').dt.strftime("%d/%m/%Y")
                dados.insert(11, 'DATA DE PAGAMENTO', dados['data_pagamento_cliente'])
                dados.columns = self.columns_to_rename
                os.makedirs(path_to_save, exist_ok=True)
                
                dados.to_csv(path_to_save + f'{bank}_{date}.csv', index = False, sep = ';', encoding = 'latin1')

# debug     
# productionToStorm().makeReport(date = datetime.date.today(), bank = 'FACTA FINANCEIRA')



# USUARIO BANCO inserir usuário banco
