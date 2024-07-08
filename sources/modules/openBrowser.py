# selenium
from selenium import webdriver
from selenium.webdriver.firefox import service
from selenium.webdriver.firefox.options import Options
from pathlib import Path


# class para abrir no navegador
class openFirefox():

    def __init__(self):
        pass


    def _initializeDriver(self, bank: str):

        #instanciando método options do selenium, e setando alguns valroes
        options = Options()
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        # options.set_preference("browser.download.dir", fr"{str(Path().absolute())}\\download")
        options.set_preference("browser.download.dir", fr"{str(Path().absolute())}\\download_tmp")
        # options.set_preference("browser.download.dir", f"../{bank}/download_tmp")
        
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        driver = webdriver.Firefox(options=options)
        driver.maximize_window()
        return driver
    
