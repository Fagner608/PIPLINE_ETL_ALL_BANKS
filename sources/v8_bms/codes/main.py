import sys
sys.path.append("../../modules")
from extractProductionData import Extract
import main_tranformLoad
import datetime
import mainStorm



def main(date: datetime.datetime = datetime.datetime.today()):
    
    # Extração
    Extract().persist(date_work = date)
    
    # Transformação e tratamento
    main_tranformLoad.main(date=datetime.date.today())

    # Carga    
    mainStorm.main(date = date, provider='BMS')


if __name__ == "__main__":
    main()
    print("Processos V8 - BMS finalizados.")
    # logger.info(f"Execucao do robô de importacao V8 - BMS finalizado")
        