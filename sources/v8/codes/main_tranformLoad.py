import cleaningTransforma_comission
import cleaningTransform_production
import cleaningTransform_contracts

import datetime
from tqdm import tqdm

def main(date: datetime.date):
    
    processos = [(f"Limpando e trnsformando dados de comissão {date} - v8 - cartão", cleaningTransforma_comission.CleaningComission),
                 (f"Atualizando tabelas do banco de dados {date} - v8 - cartão", cleaningTransforma_comission.load_comission),
                #  (f"Limpando e trnsformando dados de produção {date} - v8 - cartão", cleaningTransform_production.CleaningProduction),
                #  (f"Atualizando tabelas do banco de dados {date} - v8 - cartão", cleaningTransform_production.load_production),
                 (f"Limpando e trnsformando dados de produção {date} - v8 - cartão", cleaningTransform_contracts.CleaningContracts),
                 (f"Input dos contratos {date} - v8 - cartão", cleaningTransform_contracts.load_contracts)]

              
    with tqdm(total = len(processos), desc = "Executando Transformação e carga - crefisa") as pbar_total:
        for processo_desc, process_func in processos:
            pbar_total.set_description(processo_desc)
            process_func(date = date)
            pbar_total.update(1)


# Debug
# main(date = datetime.date(2024,6,18))
# print("Transformação e carga crefisa finalizados.")
