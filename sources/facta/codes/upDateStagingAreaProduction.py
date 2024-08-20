# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginAreaFacta():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        pass

    def upDatating(self, bank = str):
        
        '''
         Atualiza dados da tabela no staging_area
        '''
        con, cur = inputsDB().conDatabase()
        
        ############ Digite aqui suas querys ############
        # exemlo
        query = f'''

        UPDATE staging_area
        SET banco = '{bank}';
        --WHERE banco = 'facta_financeira'

        -- Atualizando cliente id
        ALTER TABLE staging_area ADD COLUMN cliente_id TEXT;
        UPDATE staging_area
        SET cliente_id = cliente.cliente_id
        FROM cliente
        WHERE staging_area.cpf = cliente.cpf_cliente;

        -- Atualizando convenio
        UPDATE staging_area SET averbador = CASE 
            WHEN averbador = '3' THEN 'INSS'
            WHEN averbador = '20095' THEN 'FGTS'
            WHEN averbador = '23' THEN 'MARINHA'
            WHEN averbador IN ('FGTS', 'INSS', 'RMC', 'INSS Cartão') THEN 'INSS'
            WHEN averbador = 'INSS Cartão' THEN 'INSS - Cartão Benefício'
            WHEN averbador = 'IPE - INST PREV DO ESTADO - RS' OR averbador = '30' THEN 'IPÊ'
            WHEN averbador = 'FACTA FÁCIL - DÉBITO EM CONTA' OR averbador = '390' THEN 'FACTA FÁCIL'
            WHEN averbador = 'SIAPE' OR averbador = '15' THEN 'FEDERAL'
            WHEN averbador = 'DEBITO EM CONTA' THEN 'CRÉDITO PESSOAL - DÉBITO EM CONTA'
            WHEN averbador = 'AUXILIO BRASIL' THEN 'AUXÍLIO-BRASIL'
            WHEN averbador = 'PREFEITURA DE PORTO ALEGRE - RS' THEN 'PREF. DE PORTO ALEGRE - RS'
            WHEN averbador = 'GOVERNO DA BAHIA' THEN 'GOVERNO BA'
            WHEN averbador = 'GOVERNO DO ESTADO RS' THEN 'GOVERNO RS'
            ELSE averbador
        END;

        -- Atualizando tipo de contrato/operacao
        UPDATE staging_area SET tipo_operação = CASE 
            WHEN tipo_operação IN ('13', 'novo_digital', 'novo_digital_(repr_legal)', 'novo_digital_consignado', '37') THEN 'MARGEM LIVRE (NOVO)'
            WHEN tipo_operação IN ('14', '32', 'refin_digital', 'refin_da_portabilidade', 'refin_da_portabilidade_(repr_legal)', 'refin_digital_+_margem_livre') THEN 'REFINANCIAMENTO'
            WHEN tipo_operação IN ('17', 'portabilidade_digital', '43') THEN 'PORTABILIDADE'
            WHEN tipo_operação IN ('18', 'refin_da_portabilidade', '44') THEN 'REFINANCIAMENTO DA PORTABILIDADE'
            WHEN tipo_operação IN ('33', '36', '38', '11', 'cartao_digital_rmc', 'cartao_digital_rmc_(repr_legal)', 'cartao_consignado_beneficio', 'cartao_consignado_benef_(repr_legal)', '45', '46', '47', '48', 'saque_complementar_rcc', 'saque_complementar_rcc_(repr_legal)', 'saque_complementar_rmc') THEN 'CARTÃO C/ SAQUE'
            ELSE tipo_operação
        END;
        -- estes tipos de contratos podem aparecer
        	-- refin_da_portabilidade_(repr_legal)
        	-- saque_complementar_rcc
        	-- saque_complementar_rcc_(repr_legal)
        	-- saque_complementar_rmc
        	-- refin_digital_+_margem_livre
        	-- saque_complementar_rmc_(repr_legal)


        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            # raise
            pass
        con.commit()
        cur.close()
        con.close()
        
   