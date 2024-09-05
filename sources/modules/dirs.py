import datetime
import os
import sys
import datetime
from shutil import copy
# class para manipular estrutura de diretórios
class mk_paths():

    def __init__(self, banks_list: list):
        self.bank_list = banks_list
        self.create_comission_dirs()
        self.create_proposal_dirs()
        self.banks_structures()

    def create_proposal_dirs(self):
        date = datetime.date.today()
        path = f"../../Produção/{date.year}/{date.month}/{date.day}"
        os.makedirs(path, exist_ok=True)

    def create_comission_dirs(self):
        date = datetime.date.today()
        path = f"../../Comissão/{date.year}/{date.month}/{date.day}"
        os.makedirs(path, exist_ok=True)

    def banks_structures(self):
        date = datetime.date.today()
        for bank in self.bank_list:
            root = f"../{bank}/"
            path_documentation = f'{root}documentation'
            path_data = f"{root}data/"
            path_download = f'{root}download/{date.year}/{date.month}/'
            path_download_comission = path_download + 'comission'
            path_download_production = path_download + 'production'
            path_download_importation = path_download + 'importation'
            path_download_extra = path_download + 'extra'
            # path_task = f'{root}task/'
            path_codes = f'{root}codes/'
            path_download_tmp = f'{path_codes}/download_tmp/'
            for path in [path_data,
                         path_codes,
                         path_documentation,
                         path_download_comission,
                         path_download_production,
                         path_download_tmp,
                         path_download_importation,
                         path_download_extra
                        #  path_task
                         ]:
                os.makedirs(path, exist_ok=True)

        # movendo pastas
        if os.path.exists(path_codes):
            for file in os.listdir('./base_codes/'):
                if not os.path.exists(path_codes + file):
                    copy(f"./base_codes/{file}", path_codes)
                
                

   
if __name__ == '__main__':
    
    banks = ['bradesco']

    mk_paths(banks_list = banks)