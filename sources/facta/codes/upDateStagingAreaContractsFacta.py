# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
import pandas as pd

class updateStaginAreaContracts():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        pass

    def upDatating(self, bank = str):
        
        '''
         Atualiza dados do staging_area
        '''
        con, cur = inputsDB().conDatabase()
        
        ############ Digite aqui suas querys ############
        # exemlo
        query = f'''

        alter table staging_area add column banco text;
        alter table staging_area add column cliente_id text;
        alter table staging_area add column bonus float;
        alter table staging_area add column codigo_usuario_digitador text;
        alter table staging_area add column sit_pagamento_cliente text;

        
        update staging_area
        set sit_pagamento_cliente = 'PAGO';


        -- atualizando banco
        UPDATE staging_area 
        set banco = '{bank}';
        --where banco = 'facta_financeira'
               
        -- Atualizando cliente id
        UPDATE staging_area
        set cliente_id = cliente.cliente_id
        from cliente
        where staging_area.cpf == cliente.cpf_cliente;
        
        -- atualizando convenio
        UPDATE staging_area
        set convenio = 'CRÉDITO PESSOAL'
        where convenio = 'baixa_renda';
        
        UPDATE staging_area
        set convenio = 'CRÉDITO PESSOAL'
        where convenio = 'inss';
        
        -- atualizando corretor/vendedor
        UPDATE staging_area set corretor = CASE
            WHEN corretor IN ('93052') THEN 'the_one_prestacao_de_servicos_ltda'
        END;

        -- Atualizando tipo de contrato/operacao
        UPDATE staging_area SET tipo_operacao = CASE 
            WHEN tipo_operacao IN ('27', '13', 'novo_digital', 'novo_digital_(repr_legal)', 'novo_digital_consignado', '37', '35') THEN 'MARGEM LIVRE (NOVO)'
            WHEN tipo_operacao IN ('14', '32', 'refin_digital', 'refin_da_portabilidade', 'refin_da_portabilidade_(repr_legal)', 'refin_digital_+_margem_livre') THEN 'REFINANCIAMENTO'
            WHEN tipo_operacao IN ('17', 'portabilidade_digital', '43') THEN 'PORTABILIDADE'
            WHEN tipo_operacao IN ('18', 'refin_da_portabilidade', '44') THEN 'REFINANCIAMENTO DA PORTABILIDADE'
            WHEN tipo_operacao IN ('33', '36', '38', '11', 'cartao_digital_rmc', 'cartao_digital_rmc_(repr_legal)', 'cartao_consignado_beneficio', 'cartao_consignado_benef_(repr_legal)', '45', '46', '47', '48', 'saque_complementar_rcc', 'saque_complementar_rcc_(repr_legal)', 'saque_complementar_rmc') THEN 'CARTÃO C/ SAQUE'
            ELSE tipo_operacao
        END;
        
        -- Atualizando convenio
        UPDATE staging_area SET averbador = CASE 
            WHEN averbador IN ('3', '10226') THEN 'INSS'
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
        
        


        
        '''
        try:
            cur.executescript(query)
        except sqlite3.OperationalError:
            pass
            # raise
        con.commit()
        cur.close()
        con.close()
        
   