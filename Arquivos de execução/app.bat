@echo off

where pip >nul 2>nul
IF ERRORLEVEL 1 (
    echo "pip não está instalado. Instale o Python e o pip primeiro."
    exit /b 1
)

pip install -r requirements.txt
pip install -r requirements_1.txt
pip install -r requirements_2.txt

streamlit run teste_layout_v3.py
