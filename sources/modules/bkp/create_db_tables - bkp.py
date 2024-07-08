import sqlite3
from tqdm import tqdm
# instanciando conexao
print("Conectando ao banco de dados.")
con = sqlite3.connect("../../ZZ/importacoes.db")
cur = con.cursor()

# Instanciando tabelas
query_create_status_importacao = (
    '''
    create table if not exists status_importacao(status_importacao_id integer primary key autoincrement,
                                                stauts varchar(30) 
                                                )

    '''

)

# Instanciando tabelas
query_create_tipo_contrato = (
    '''
    create table if not exists tipo_contrato(tipo_contrato_id integer primary key autoincrement,
                                            tipo varchar(30) 
                                            )

    '''

)

# Instanciando tabelas
query_create_tipo_operacao = (
    '''
    create table if not exists tipo_operacao(tipo_operacao_id integer primary key autoincrement,
                                            nome_operacao varchar(30) 
                                            )

    '''

)

# Instanciando tabelas
query_create_cliente = (
    '''
    create table if not exists cliente(cliente_id integer primary key autoincrement,
                                        nome_cliente varchar(200) ,
                                        cpf_cliente integer
                                        )

    '''

)

# Instanciando tabelas
query_create_vendedor = (
    '''
    create table if not exists vendedor(vendedor_id integer primary key autoincrement,
                                        nome_vendedor varchar(30) ,
                                        codigo_vendedor integer
                                        )

    '''

)

# Instanciando tabelas
query_create_usuario_substabelecido = (
    '''
    create table if not exists usuario_substabelecido(usuario_substabelecido_id integer primary key autoincrement,
                                                      nome_usuario_substabelecido varchar(30) ,
                                                      codigo_usuario_substabelecido integer 
                                                      )

    '''

)

# Instanciando tabelas
query_create_convenio = (
    '''
    create table if not exists convenio(convenio_id integer primary key autoincrement,
                                        nome_convenio varchar(30) ,
                                        codigo_convenio integer 
                                        )

    '''

)

# Instanciando tabelas
query_create_usuario_digitador_banco = (
    '''
    create table if not exists usuario_digitador_banco(usuario_digitador_banco_id integer primary key autoincrement,
                                                       nome_usuario_digitador varchar(30) ,
                                                       codigo_usuario_digitador varchar(30) 
                                                        )

    '''

)

# Instanciando tabelas
query_create_banco = (
    '''
    create table if not exists banco(banco_id integer primary key autoincrement,
                                    nome_banco varchar(30) 
                                    )

    '''

)

# Instanciando tabelas
query_create_tabela = (
    '''
    create table if not exists tabela(tabela_id integer primary key autoincrement,
                                      nome_tabela varchar(30) ,
                                      codigo_tabela integer 
                                      )

    '''

)

# Instanciando tabelas

query_create_contrato = (
    '''
    create table if not exists contrato(
        contrato_id integer primary key autoincrement,
        tipo_contrato varchar(50),
        status_importacao varchar(50) default 'nao_importado',
        tipo_operacao varchar(50),
        numero_ade integer , --not null
        quantidade_parcela_prazo integer,
        valor_parcela real , --not null
        valor_bruto real , --not null
        valor_liquido real , --not null
        valor_base real , --not null
        percentual_cms_repasse varchar(5),
        valor_cms_repasse real,
        percentual_bonus_repasse varchar(5),
        valor_bonus_repasse real,
        data_pagamento_cliente date , --not null
        percentual_cms_a_vista varchar(5),
        valor_cms_a_vista real , --not null
        nome_tabela varchar(50),
        nome_banco varchar(50),
        nome_usuario_digitador varchar(50),
        nome_convenio varchar(50),
        nome_usuario_substabelecido varchar(50),
        nome_vendedor varchar(50),
        formalizacao_digial varchar(5) default 'SIM',
        FOREIGN KEY (tipo_contrato) REFERENCES tipo_contrato(tipo),
        FOREIGN KEY (status_importacao) REFERENCES status_importacao(stauts),
        FOREIGN KEY (tipo_operacao) REFERENCES tipo_operacao(nome_operacao),
        FOREIGN KEY (nome_tabela) REFERENCES tabela(nome_tabela),
        FOREIGN KEY (nome_banco) REFERENCES banco(nome_banco),
        FOREIGN KEY (nome_usuario_digitador) REFERENCES usuario_digitador_banco(nome_usuario_digitador),
        FOREIGN KEY (nome_convenio) REFERENCES convenio(nome_convenio),
        FOREIGN KEY (nome_usuario_substabelecido) REFERENCES usuario_substabelecido(nome_usuario_substabelecido),
        FOREIGN KEY (nome_vendedor) REFERENCES vendedor(nome_vendedor)
    )
    '''
)


querys_list = [query_create_status_importacao,
               query_create_tipo_contrato,
               query_create_tipo_operacao,
               query_create_cliente,
               query_create_vendedor,
               query_create_usuario_substabelecido,
               query_create_convenio,
               query_create_usuario_digitador_banco,
               query_create_banco,
               query_create_tabela,
               query_create_contrato
               ]

def execute_script(query):
    cur.execute(query)
    con.commit()

print("Criando tabelas")
processos = [
            ("Criando tabela status_importacao", execute_script(querys_list[0])),

            ("Criando tabela tipo_contrato", execute_script(querys_list[1])),

            ("Criando tabela tipo_operacao", execute_script(querys_list[2])),

            ("Criando tabela cliente", execute_script(querys_list[3])),

            ("Criando tabela vendedor", execute_script(querys_list[4])),

            ("Criando tabela usuario_substabelecido", execute_script(querys_list[5])),

            ("Criando tabela convenio", execute_script(querys_list[6])),

            ("Criando tabela usuario_digitador_banco", execute_script(querys_list[7])),

            ("Criando tabela banco", execute_script(querys_list[8])),

            ("Criando tabela tabela", execute_script(querys_list[9])),

            ("Criando tabela contrato", execute_script(querys_list[10])),

             ]

with tqdm(total=len(processos), desc="Executando processos") as pbar_total:
    for processo_desc, processo_func in processos:
        pbar_total.set_description(processo_desc)
        processo_func
        pbar_total.update(1)