import cleaningTransforma_comission
import cleaningTransform_production
import cleaningTransform_contracts

import datetime
from tqdm import tqdm

def main(date: datetime.date):
    
    processos = [
                (f"Limpando e transformando dados de comissão {date} - facta", cleaningTransforma_comission.CleaningComission),
                 (f"Atualizando tabelas do banco de dados {date} - facta", cleaningTransforma_comission.load_comission),
                 (f"Limpando e transformando dados de produção {date} - facta", cleaningTransform_production.CleaningProduction),
                 (f"Atualizando tabelas do banco de dados {date} - facta", cleaningTransform_production.load_production),
                 (f"Limpando e transformando dados de produção {date} - facta", cleaningTransform_contracts.CleaningContracts),
                 (f"Input dos contratos {date} - facta", cleaningTransform_contracts.load_contracts)
                 ]

              
    with tqdm(total = len(processos), desc = "Executando Transformação e carga - facta") as pbar_total:
        for processo_desc, process_func in processos:
            pbar_total.set_description(processo_desc)
            process_func(date = date)
            pbar_total.update(1)


# Debug
# main(date = datetime.date(2024, 8, 23))
# print("Transformação e carga facta finalizados.")
