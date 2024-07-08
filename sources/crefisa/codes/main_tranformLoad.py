import cleaningTransforma_comission
import cleaningTransform_production
import cleaningTransform_contracts

import datetime
from tqdm import tqdm

def main(date: datetime.date):
    
    processos = [
                 (f"Limpando e trnsformando dados de produção {date} - crefisa", cleaningTransform_production.crefisaCleaningProduction),
                 (f"Atualizando tabelas do banco de dados {date} - crefisa", cleaningTransform_production.load_crefisa_production),
                 (f"Limpando e trnsformando dados dos contratos {date} - crefisa", cleaningTransform_contracts.crefisaCleaningContracts),
                 (f"Input dos contratos {date} - crefisa", cleaningTransform_contracts.load_contracts)
                ]

              
    with tqdm(total = len(processos), desc = "Executando Transformação e carga - crefisa") as pbar_total:
        for processo_desc, process_func in processos:
            pbar_total.set_description(processo_desc)
            process_func(date = date)
            pbar_total.update(1)


# Debug
# main(date = datetime.date(2024,6,24))
# print("Transformação e carga crefisa finalizados.")

