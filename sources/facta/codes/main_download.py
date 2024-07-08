from downloads import download
from downloads_production import download_production

import datetime

def main(date: datetime.date):
        download().tqdm_bar(date_work = date)
        download_production().tqdm_bar(date_work = date)
        
        
#debug
if __name__ == '__main__':
    date_work = datetime.date.today()
    main(date = date_work)