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
                     (f"Limpando e transformando dados de comissão {date} - {bank}", comissionToSorm.comissionToStorm().makeReport),
                    (f"Limpando e transformando dados de comissão {date} - {bank}", producionToSorm.productionToStorm().makeReport)
                    ]
        
       
        


        with tqdm(total = len(processos), desc = f"Gerando relatórios - {bank}") as pbar_total:
            for processo_desc, process_func in processos:
                pbar_total.set_description(processo_desc)
                process_func(date = date, bank = bank)
                pbar_total.update(1)

# Debug
# main(date = datetime.date(2024, 8, 30), bank='V8 DIGITAL')
