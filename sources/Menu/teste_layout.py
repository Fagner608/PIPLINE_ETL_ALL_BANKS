import streamlit as st

# Defina suas funções principais aqui
def main1():
    st.title("Main 1")
    st.write("Você está na função principal 1")

def main2():
    st.title("Main 2")
    st.write("Você está na função principal 2")

def main3():
    st.title("Main 3")
    st.write("Você está na função principal 3")

# Crie um layout básico com Streamlit
def app():
    st.sidebar.title("Navegação")
    
    # Crie botões na barra lateral
    option = st.sidebar.radio("Escolha uma opção:", ["Main 1", "Main 2", "Main 3"])
    
    # Exiba o conteúdo com base na opção escolhida
    if option == "Main 1":
        main1()
    elif option == "Main 2":
        main2()
    elif option == "Main 3":
        main3()

# Execute a aplicação
if __name__ == "__main__":
    app()
