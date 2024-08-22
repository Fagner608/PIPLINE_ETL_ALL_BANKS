import main_download
import main_tranformLoad
import datetime
import mainStorm


if __name__ == "__main__":

    # Extract
    main_download.main(date = datetime.date.today())
    
    # Transform and Load
    date = datetime.date.today() - datetime.timedelta(days = 5)
    # date = datetime.date(2024, 8, 21)
    while date <= datetime.date.today():
        main_tranformLoad.main(date=date)
        date += datetime.timedelta(days = 1)
    
    # Gerando relatórios Storm
    mainStorm.main(date=datetime.date.today(), bank='FACTA FINANCEIRA')
        