title V8 Digital
chcp 65001
pushd Z:\ || pushd G:\ || pushd Y:\
cd FINANCEIRO\11 - RELATÓRIOS DIÁRIOS E MENSAIS\01 - Importações Diárias\19 - V8 Digital\zz - V8 - coleta tabelas comissões

call \.venv\scripts\activate
python -c "import main;main.download_and_send_report_tables()"
pause