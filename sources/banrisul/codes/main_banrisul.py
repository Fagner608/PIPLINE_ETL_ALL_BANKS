import main_download
import main_tranformLoad
import datetime
import mainStorm


def main():
    # Extract
    main_download.main(date = datetime.date.today())
    
    # Transform and Load
    date = datetime.date.today() - datetime.timedelta(days = 5)
    while date <= datetime.date.today():
        main_tranformLoad.main(date=date)
        date += datetime.timedelta(days = 1)
    
    # Gerando relatórios Storm
    mainStorm.main(date=datetime.date.today(), bank='Insira o banco')


if __name__ == "__main__":
    main()
        