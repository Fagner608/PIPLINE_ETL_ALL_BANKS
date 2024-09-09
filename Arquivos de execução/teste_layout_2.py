import streamlit as st
import subprocess
import os

# Função para abrir um diretório no Windows Explorer
def open_directory(directory_path):
    # Usa o subprocess para abrir o diretório
    subprocess.Popen(f'explorer "{os.path.realpath(directory_path)}"')

# Função para executar o arquivo .lnk
def run_batch_file(file_path):
    subprocess.Popen(['cmd', '/c', file_path], shell=True)

# Configura a página do Streamlit
st.set_page_config(page_title="Executar Scripts e Relatórios", layout="wide")

# Título do aplicativo
st.title("Executar Scripts e Obter Relatórios")

# Descrição
st.markdown("""
    ### Selecione o script para execução:
    Use o menu lateral para escolher o arquivo de automação que deseja executar.
""")

# Dicionário com os nomes dos botões e caminhos dos arquivos .lnk
batch_files = {
    "V8 - CARTAO": "executa_v8 - Atalho.lnk",
    "FACTA": "executa_facta - Atalho.lnk",
    "CREFISA": "executar_crefisa - Atalho.lnk",
    "PAN": "executar_nova_pan - Atalho",
    # Adicione mais arquivos conforme necessário
}

# Colocando os botões no menu lateral
with st.sidebar:
    st.header("Menu de Scripts")
    
    # Define a largura e altura dos botões
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
    
    # Criação dos botões com mesmo tamanho para os primeiros arquivos
    for name, path in batch_files.items():
        if st.button(name):
            run_batch_file(path)
            st.sidebar.success(f"Executando {name}...")

    # Linha separadora antes do botão "ZZ"
    st.markdown("---")  # Linha horizontal para separar

    # Botão "ZZ" separado
    if st.button("ZZ"):
        run_batch_file("run_zz - Atalho.lnk")
        st.sidebar.success("Executando ZZ...")

    # Linha separadora para a seção "Obter Relatórios"
    st.markdown("---")

    # Título da seção
    st.subheader("Obter Relatórios")

    # Botão para abrir o diretório "Comissão"
    if st.button("Comissão"):
        open_directory(r"\\Serv-agil\agil franquias$\FINANCEIRO\11 - RELATÓRIOS DIÁRIOS E MENSAIS\01 - Importações Diárias\Importações\Fagner - NAO USAR\Comissão")
        st.sidebar.success("Abrindo diretório de Comissão...")

    # Botão para abrir o diretório "Produção"
    if st.button("Produção"):
        open_directory(r"\\Serv-agil\agil franquias$\FINANCEIRO\11 - RELATÓRIOS DIÁRIOS E MENSAIS\01 - Importações Diárias\Importações\Fagner - NAO USAR\Produção")
        st.sidebar.success("Abrindo diretório de Produção...")

# Estilo customizado para a página principal
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition-duration: 0.4s;
    }
    .stButton button:hover {
        background-color: white;
        color: black;
        border: 2px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)
