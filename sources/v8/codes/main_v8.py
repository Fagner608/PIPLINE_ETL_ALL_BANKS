import main_download
import main_tranformLoad
import datetime
import mainToStorm
import mainDownloadImportation


def main():
    # Extract
    main_download.main(date = datetime.date.today())
    
    # Transform and Load
    date = datetime.date.today() - datetime.timedelta(days = 3)
    while date <= datetime.date.today():
        main_tranformLoad.main(date=date)
        mainDownloadImportation.main(date=date, bank='V8 DIGITAL')
        date += datetime.timedelta(days = 1)
    
    # Gerando relatórios Storm
    mainToStorm.main(date=datetime.date.today(), bank='V8 DIGITAL')

if __name__ == "__main__":
    main()
    print("Processos do V8 - cartão finalizados.")