import sys
sys.path.append("../../modules")
from downloads_importados_storm import download_importados_storm
import comissionToSorm
import productionToSorm
import cleaningTransform_importation
import datetime
from tqdm import tqdm

def main(date: datetime.date, provider: str):
        
        
        processos = [
                    (f"Download dos dados de importacao {date} - {provider}",  download_importados_storm().dowloadImportation),
                    (f"Limpando e transformando dados de importacao {date} - {provider}", cleaningTransform_importation.cleaningImportation),
                     (f"Gerenciando status de importação - {provider}", cleaningTransform_importation.statusManager),
                    (f"Limpando e transformando dados de comissão {date} - {provider}", comissionToSorm.comissionToStorm().makeReport),
                     (f"Limpando e transformando dados de produção {date} - {provider}", productionToSorm.productionToStorm().makeReport)
                    ]
        
       
        


        with tqdm(total = len(processos), desc = f"Gerando relatórios - {provider}") as pbar_total:
            for processo_desc, process_func in processos:
                pbar_total.set_description(processo_desc)
                process_func(date = date, provider = provider)
                pbar_total.update(1)

# Debug
# main(date = datetime.datetime.today(), provider='BMS')
