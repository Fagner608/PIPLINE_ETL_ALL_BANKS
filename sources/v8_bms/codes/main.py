import main_download
import main_tranformLoad
import datetime
import mainStorm


def main():
    # Extract - neste caso, a extração será de um DB
    main_download.main(date = datetime.date.today())
    
    # Transform and Load - fazer um DB próprio para este banco (postgre) - espera-se receber alto volume de proposta
    date = datetime.date.today() - datetime.timedelta(days = 5)
    while date <= datetime.date.today():
        main_tranformLoad.main(date=date)
        date += datetime.timedelta(days = 1)
    
    # Gerando relatórios Storm
    mainStorm.main(date=datetime.datetime.today(), bank='V8 DIGITAL')


if __name__ == "__main__":
    main()
    print("Processos V8 - BMS finalizados.")
        