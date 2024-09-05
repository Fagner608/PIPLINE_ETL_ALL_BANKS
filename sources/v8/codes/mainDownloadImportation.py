import producionToSorm
import comissionToSorm
import cleaningTransform_importation
from downloads_importados_storm import download_importados_storm
import datetime
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

def main(date: datetime.date, bank: str):
        
        
        processos = [
                    (f"Download dos dados de importacao {date} - {bank}",  download_importados_storm().tqdm_bar),
                    (f"Limpando e transformando dados de importacao {date} - {bank}", cleaningTransform_importation.cleaningImportation),
                    (f"Gerenciando status de importação - {bank}", cleaningTransform_importation.statusManager),
                    ]
        
       
        


        with tqdm(total = len(processos), desc = f"Gerenciado status de importação - {bank}") as pbar_total:
            for processo_desc, process_func in processos:
                pbar_total.set_description(processo_desc)
                process_func(date_work = date, bank = bank)
                pbar_total.update(1)

# Debug
# main(date = datetime.date(2024, 9, 2), bank='V8 DIGITAL')
