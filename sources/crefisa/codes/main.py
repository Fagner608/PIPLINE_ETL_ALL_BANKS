import main_download
import main_tranformLoad
import datetime
import mainStorm


if __name__ == "__main__":

    # Extract
    main_download.main(date = datetime.date.today())
    
    # Transform and Load data
    date = datetime.date.today() - datetime.timedelta(days = 5)
    # date = datetime.date.today()
    while date <= datetime.date.today():
        main_tranformLoad.main(date=date)
        date += datetime.timedelta(days = 1)
    
    # Reports
    mainStorm.main(date=datetime.date.today(), bank='BANCO CREFISA')
        