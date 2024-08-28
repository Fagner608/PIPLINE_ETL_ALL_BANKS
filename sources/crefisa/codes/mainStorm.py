import producionToSorm
import comissionToSorm
import cleaningTransform_importation
from downloads_importados_storm import download_importados_storm
import datetime
from tqdm import tqdm

def main(date: datetime.date, bank: str):
        
        
        processos = [
                    (f"Download dos dados de importacao {date} - crefisa",  download_importados_storm().tqdm_bar),
                    (f"Limpando e trnsformando dados de importacao {date} - crefisa", cleaningTransform_importation.cleaningImportation),
                     (f"Gerenciando status de importação - crefisa", cleaningTransform_importation.statusManager),
                     (f"Preparando relatório storm de comissão {date} - {bank}", comissionToSorm.comissionToStorm().makeReport),
                    (f"Preparando relatório storm de produção {date} - {bank}", producionToSorm.productionToStorm().makeReport)
                    ]
        
       
        


        with tqdm(total = len(processos), desc = f"Gerando relatórios - {bank}") as pbar_total:
            for processo_desc, process_func in processos:
                pbar_total.set_description(processo_desc)
                process_func(date = date, bank = bank)
                pbar_total.update(1)

# Debug
# main(date = datetime.date.today(), bank='BANCO CREFISA')
