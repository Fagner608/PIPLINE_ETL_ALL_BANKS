import cleaningTransforma_comission
import cleaningTransform_production
import cleaningTransform_contracts

import datetime
from tqdm import tqdm

def main(date: datetime.date):
    
    processos = [
                #  (f"Limpando e transformando dados de comissão {date} - mercantil", cleaningTransforma_comission.CleaningComission),
                #  (f"Atualizando tabelas do banco de dados {date} - mercantil", cleaningTransforma_comission.load_comission),
                 (f"Limpando e transformando dados de produção {date} - mercantil", cleaningTransform_production.CleaningProduction),
                 (f"Atualizando tabelas do banco de dados {date} - mercantil", cleaningTransform_production.load_production),
                 (f"Limpando e transformando dados de produção {date} - mercantil", cleaningTransform_contracts.CleaningContracts),
                 (f"Input dos contratos {date} - mercantil", cleaningTransform_contracts.load_contracts)
                 ]

              
    with tqdm(total = len(processos), desc = "Executando Transformação e carga - mercantil") as pbar_total:
        for processo_desc, process_func in processos:
            pbar_total.set_description(processo_desc)
            process_func(date = date)
            pbar_total.update(1)


# Debug
# main(date = datetime.date.today())
# print("Transformação e carga mercantil finalizados.")
