import streamlit as st
import sqlite3
import pandas as pd
import base64

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('importacoes.db')
cursor = conn.cursor()

# Função para filtrar os dados da tabela contrato com base nos atributos selecionados
    # recebe argumentos na linha 49
def filtrar_contratos(numero_ade, nome_banco, status_importacao, tipo_operacao, data_inicial, data_final):
    query = "SELECT * FROM contrato WHERE 1=1"

    if numero_ade:
        query += f" AND numero_ade ='{numero_ade}'"
    if nome_banco:
        query += f" AND nome_banco='{nome_banco}'"
    if status_importacao:
        query += f" AND status_importacao='{status_importacao}'"
    if tipo_operacao:
        query += f" AND tipo_operacao='{tipo_operacao}'"
    if data_inicial and data_final:
        query += f" AND Date(data_pagamento_cliente) BETWEEN '{data_inicial}' AND '{data_final}'"
    df = pd.read_sql(query, conn)
    return df

# Função principal para o aplicativo Streamlit
def main():
    st.set_page_config(layout="wide")

    st.title('Filtrar Contratos')

    # Sidebar para seleção dos filtros
    st.sidebar.title('Filtros')

    # Obter valores únicos para os filtros
    nome_banco_options = cursor.execute("SELECT DISTINCT nome_banco FROM contrato").fetchall()
    nome_banco = st.sidebar.selectbox('Banco', options=[x[0] for x in nome_banco_options])
    
    status_importacao_options = cursor.execute("SELECT DISTINCT status_importacao FROM contrato").fetchall()
    status_importacao = st.sidebar.selectbox('Status de Importação', options=[x[0] for x in status_importacao_options])

    tipo_operacao_options = cursor.execute("SELECT DISTINCT tipo_operacao FROM contrato").fetchall()
    tipo_operacao = st.sidebar.selectbox('Tipo de Operação', options=[x[0] for x in tipo_operacao_options])

    data_inicial = st.sidebar.date_input("Data Inicial", None)
    data_final = st.sidebar.date_input("Data Final", None)
    
    numero_ade = st.sidebar.text_input("Numero ade", None)

    # Botão para acionar a filtragem
    if st.sidebar.button('Filtrar'):
        st.subheader('Resultado da Filtragem')
        contratos_filtrados = filtrar_contratos(numero_ade, nome_banco, status_importacao, tipo_operacao, data_inicial, data_final)

        import re
        contratos_filtrados['numero_ade'] = contratos_filtrados['numero_ade'].map(lambda x: re.sub(",", "", str(x)))
        contratos_filtrados['contrato_id'] = contratos_filtrados['contrato_id'].map(lambda x: re.sub(",", "", str(x)))

        st.dataframe(contratos_filtrados, width=0) 

        # Botão para baixar em Excel
        if not contratos_filtrados.empty:
            
            csv = contratos_filtrados.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="contratos_filtrados.csv">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

# Executar o aplicativo
if __name__ == '__main__':
    main()
