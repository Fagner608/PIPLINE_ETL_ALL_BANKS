from downloads import download
import datetime

def main(date: datetime.date):
         download().tqdm_bar(date_work = date)

if __name__ == '__main__':
    date_work = datetime.date.today()
    main(date = date_work)