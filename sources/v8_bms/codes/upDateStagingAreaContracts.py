# fazer desta uma classe base para retornar contratos nao importados e chamar nas demais funcoes para relatorios
import sqlite3
import sys
sys.path.append("../../modules")
from inputDataTransformed import inputsDB
from connectionDB import ConectionDB
from logger import loogerControls

import pandas as pd



class updateStaginAreaContracts():

    '''
    Método base para atualizações na tabela staging_area.
    Cada tabela demandará seu conjunto de instruções sql.
    '''

    def __init__(self):
        self.logger = loogerControls().loggerFunction()

    def upDatating(self, bank: str, db_name: str, provider: str):
        
        '''
         Retorna propostas com status de importacao 'nao_importadas'
        '''
        #### substituir esta conexão com a do DB postgre
        # instanciando engine
        con = ConectionDB().psycopgConnection(db_name)
        cur = con.cursor()
        
        ############ Digite aqui suas querys ############
        # exemlo

        query = f'''
        alter table temp_table add column BANCO text;
        alter table temp_table add column PROVEDOR text;
        alter table temp_table add column ORGAO text;
        alter table temp_table add column TIPO_DE_OPERACAO text;
        alter table temp_table add column SITUACAO text;
        alter table temp_table add column FORMALIZACAO_DIGITAL text;
        alter table temp_table add column status_importacao text;
        alter table temp_table add column TAXA float;
        alter table temp_table add column VALOR_COMISSAO_ESTIMADO float;
        alter table temp_table add column SPREAD_ESTIMADO float;
        alter table temp_table add column TOMADA_DECISAO bool;

        
        

        --Atualizando
        update temp_table
        set status_importacao = '2';

        --Atualizando
        update temp_table
        set SITUACAO = 'PAGO';

        -- atualizando banco
        update temp_table
        set BANCO = '{bank}';
        
        -- atualizando provedor
        update temp_table
        set PROVEDOR = '{provider}';

        -- buscando Id do provider no DB producao
        update temp_table
        set PROVEDOR = (select id_provider from provider where temp_table.PROVEDOR = provider.nome_provider limit 1);

        
        -- atualizando orgao
        update temp_table
        set ORGAO = 'FGTS';
        

        -- atualizando orgao
        update temp_table
        set TIPO_DE_OPERACAO = 'MARGEM LIVRE (NOVO)';

        -- atualizando orgao
        update temp_table
        set FORMALIZACAO_DIGITAL = 'SIM';


        --Atualizando taxa de comissão
        with table_grid_tax as (
            select 
            --substring(table_namecode, 3),
            table_grid,
            case 
            when substring(table_namecode from 3) = '0001' then 0.22
            when substring(table_namecode from 3) = '0002' then 0.21
            when substring(table_namecode from 3) = '0003' then 0.19
            when substring(table_namecode from 3) ='0004' then 0.16
            when substring(table_namecode from 3) = '0005' then 0.14
            when substring(table_namecode from 3) = '0006' then 0.22
            when substring(table_namecode from 3) = '0007' then 0.33
            when substring(table_namecode from 3) = '0008' then 0.33
            when substring(table_namecode from 3) = '0009' then 0.149
            when substring(table_namecode from 3) = '0010' then 0.189
            when substring(table_namecode from 3) = '0011' then 0.114
            when substring(table_namecode from 3) = '0012' then 0.33
            when substring(table_namecode from 3) = '00BR' then 0.2390
            when substring(table_namecode from 3) = '0014' then 0.189
            when substring(table_namecode from 3) = '0015' then 0.10
            when substring(table_namecode from 3) = '0017' then 0.2390
            when substring(table_namecode from 3) = '0018' then 0.25
            when substring(table_namecode from 3) = '0019' then 0.33
            when substring(table_namecode from 3) = '0020' then 0.25
            when substring(table_namecode from 3) = '0021' then 0.39
            when substring(table_namecode from 3) = '0022' then 0.39
            when substring(table_namecode from 3) = '0023' then 0.39
            when substring(table_namecode from 3) = '0024' then 0.39
            when substring(table_namecode from 3) = '0025' then 0.39
            when substring(table_namecode from 3) = '0026' then 0.39
            when substring(table_namecode from 3) = '0027' then 0.39
            when substring(table_namecode from 3) = '0029' then 0.60
            else 0.00 end as taxa
            from tabelas
            )
            update temp_table tt
            set "taxa"  = tgt."taxa"
            from table_grid_tax tgt
            where tt."ID TABELA" = tgt."table_grid";

        --Atualizando valor de comissão
        update temp_table 
        set valor_comissao_estimado = cast("VALOR LIBERADO" as float) * taxa; 

        -- Atualizando spread_estimado
        update temp_table
        set spread_estimado = cast("VALOR LIBERADO" as float) * 0.06;

        
        -- Atualizando tomada_decisao
        update temp_table
        set tomada_decisao = (cast("TAX_INFORMADO" as float) + spread_estimado) < valor_comissao_estimado

        '''
        try:
            cur.execute(query)
            con.commit()
            self.logger.info(f"Sucesso ao executar query de atualizacao das tabelas do DB {db_name} - temp_table.")
        except Exception as exc:
            self.logger.critical(f"Falha ao executar query de atualizacao das tabelas da tamp_table: {exc}")
            con.rollback()
            self.logger.info("Rollback executado")
        cur.close()
        con.close()
        
   