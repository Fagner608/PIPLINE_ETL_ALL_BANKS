import cleaningTransform_contracts

import datetime
from tqdm import tqdm

def main(date: datetime.date):
    
    processos = [
                 (f"Limpando e trnsformando dados de produção {date} - v8 - BMS", cleaningTransform_contracts.CleaningContracts),
                 (f"Input dos contratos {date} - v8 - BMS", cleaningTransform_contracts.load_contracts)
                 ]

              
    with tqdm(total = len(processos), desc = "Executando Transformação e carga - v8 - BMS") as pbar_total:
        for processo_desc, process_func in processos:
            pbar_total.set_description(processo_desc)
            process_func(date = date)
            pbar_total.update(1)


# Debug
# main(date = datetime.date.today())
# print("Transformação e carga v8 - BMS finalizados.")
