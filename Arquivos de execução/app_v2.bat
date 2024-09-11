@echo off

:: Verifica se o pip está instalado
where pip >nul 2>nul
IF ERRORLEVEL 1 (
    echo "pip não está instalado. Instale o Python e o pip primeiro."
    exit /b 1
)

:: Verifica e instala dependências dos 3 arquivos de requirements
pip install -r requirements.txt
pip install -r requirements_1.txt
pip install -r requirements_2.txt

:: Executa o Streamlit
streamlit run teste_layout_v3.py
