import streamlit as st
import sqlite3
import pandas as pd
import base64
import io
import subprocess
import os

# Função para abrir um diretório no Windows Explorer
def open_directory(directory_path):
    subprocess.Popen(f'explorer "{os.path.realpath(directory_path)}"')

# Função para executar o arquivo .lnk
def run_batch_file(file_path):
    subprocess.Popen(['cmd', '/c', file_path], shell=True)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('../ZZ/importacoes.db')
cursor = conn.cursor()

# Função para filtrar os dados da tabela contrato com base nos atributos selecionados
def filtrar_contratos(numero_ade, nome_banco, status_importacao, tipo_operacao, data_inicial, data_final):
    query = "SELECT * FROM contrato WHERE 1=1"

    if numero_ade:
        query += f" AND numero_ade ='{numero_ade}'"
    if nome_banco and nome_banco != 'Todos':
        query += f" AND nome_banco='{nome_banco}'"
    if status_importacao and status_importacao != 'Todos':
        query += f" AND status_importacao='{status_importacao}'"
    if tipo_operacao and tipo_operacao != 'Todos':
        query += f" AND tipo_operacao='{tipo_operacao}'"
    if data_inicial and data_final:
        query += f" AND Date(data_pagamento_cliente) BETWEEN '{data_inicial}' AND '{data_final}'"
        
    df = pd.read_sql(query, conn)
    return df

# Função para exportar DataFrame para Excel
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Contratos Filtrados')
        worksheet = writer.sheets['Contratos Filtrados']
        worksheet.set_column('A:Z', 20)
    output.seek(0)
    return output.getvalue()

# Função principal para o aplicativo Streamlit
def main():
    # Configura a página do Streamlit
    st.set_page_config(page_title="Automação e Relatórios", layout="wide")

    # Título do aplicativo
    st.title("Automação de Scripts e Relatórios")

    # Descrição
    st.markdown("### Selecione o script para execução ou filtre os contratos para análise:")

    # Dicionário com os nomes dos botões e caminhos dos arquivos .lnk
    batch_files = {
        "V8 - CARTAO": "executa_v8 - Atalho.lnk",
        "FACTA": "executa_facta - Atalho.lnk",
        "CREFISA": "executar_crefisa - Atalho.lnk",
        "PAN": "executar_nova_pan - Atalho.lnk",
        "MERCANTIL": "executar_main_mercantil - Atalho.lnk",
        "BANRISUL": "executar_banrisul - Atalho.lnk",
    }

    # Sidebar com os filtros
    with st.sidebar:
        st.header("Menu de Scripts")

        # Estilo dos botões
        button_style = """
        <style>
        .stButton button {
            width: 100%;
            height: 50px;
            font-size: 16px;
        }
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)

        # Criação dos botões para scripts
        for name, path in batch_files.items():
            if st.button(name):
                run_batch_file(path)
                st.sidebar.success(f"Executando {name}...")

        # Linha separadora
        st.markdown("---")

        # Título da seção de relatórios
        st.subheader("Obter Relatórios")

        # Botões para abrir diretórios
        if st.button("Comissão"):
            print(os.getcwd())
            open_directory(r"Y:\FINANCEIRO\11 - RELATÓRIOS DIÁRIOS E MENSAIS\01 - Importações Diárias\Importações\Fagner - NAO USAR\Comissão")
            st.sidebar.success("Abrindo diretório de Comissão...")

        if st.button("Produção"):
            open_directory(r"Y:\FINANCEIRO\11 - RELATÓRIOS DIÁRIOS E MENSAIS\01 - Importações Diárias\Importações\Fagner - NAO USAR\Produção")
            st.sidebar.success("Abrindo diretório de Produção...")

        # Linha separadora para a seção de filtros de contratos
        st.markdown("---")
        st.header("Filtros de Contratos")

        # Filtros de contratos
        nome_banco_options = ['Todos'] + [x[0] for x in cursor.execute("SELECT DISTINCT nome_banco FROM contrato").fetchall()]
        nome_banco = st.selectbox('Banco', options=nome_banco_options)

        status_importacao_options = ['Todos'] + [x[0] for x in cursor.execute("SELECT DISTINCT status_importacao FROM contrato").fetchall()]
        status_importacao = st.selectbox('Status de Importação', options=status_importacao_options)

        tipo_operacao_options = ['Todos'] + [x[0] for x in cursor.execute("SELECT DISTINCT tipo_operacao FROM contrato").fetchall()]
        tipo_operacao = st.selectbox('Tipo de Operação', options=tipo_operacao_options)

        data_inicial = st.date_input("Data Inicial", None)
        data_final = st.date_input("Data Final", None)
        
        numero_ade = st.text_input("Numero ADE", None)

        st.markdown("layout v4")

    # Botão para acionar a filtragem (fora da barra lateral)
    if st.button('Filtrar Contratos'):
        st.subheader('Resultado da Filtragem')
        contratos_filtrados = filtrar_contratos(numero_ade, nome_banco, status_importacao, tipo_operacao, data_inicial, data_final)

        # Corrigir formato das colunas
        import re
        contratos_filtrados['numero_ade'] = contratos_filtrados['numero_ade'].map(lambda x: re.sub(",", "", str(x)))
        contratos_filtrados['contrato_id'] = contratos_filtrados['contrato_id'].map(lambda x: re.sub(",", "", str(x)))

        # Exibir a tabela no centro da página
        st.dataframe(contratos_filtrados, width=0) 

        # Botão para baixar em CSV
        if not contratos_filtrados.empty:
            csv = contratos_filtrados.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href_csv = f'<a href="data:file/csv;base64,{b64}" download="contratos_filtrados.csv">Download CSV</a>'
            st.markdown(href_csv, unsafe_allow_html=True)

            # Botão para baixar em Excel
            excel = to_excel(contratos_filtrados)
            b64 = base64.b64encode(excel).decode()
            href_excel = f'<a href="data:file/xlsx;base64,{b64}" download="contratos_filtrados.xlsx">Download Excel</a>'
            st.markdown(href_excel, unsafe_allow_html=True)



# Executar o aplicativo
if __name__ == '__main__':
    main()
