import tkinter as tk
import subprocess

def run_batch_file(file_path):
    # Abre uma nova janela de console para executar o arquivo .bat
    subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', file_path], shell=True)

# Cria a janela principal
root = tk.Tk()
root.title("Executar .bat")

# Cria uma estrutura de layout para os botões
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

# Dicionário com os nomes dos botões e caminhos dos arquivos .bat
batch_files = {
    "V8 - CARTAO": "executa_v8 - Atalho.lnk",
    "FACTA": "executa_facta - Atalho.lnk",
    "CREFISA": "executar_crefisa - Atalho.lnk",
    "PAN": "executar_nova_pan - Atalho",
    "ZZ": "run_zz - Atalho.lnk",
    # Adicione mais arquivos .bat conforme necessário
}

# Define o tamanho fixo dos botões
button_width = 20

# Cria um botão para cada arquivo .bat
for name, path in batch_files.items():
    btn = tk.Button(button_frame, text=name, width=button_width, command=lambda p=path: run_batch_file(p))
    btn.pack(pady=5)

# Inicia o loop principal da interface
root.mainloop()
