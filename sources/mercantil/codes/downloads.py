# imports 
from os import makedirs, path, remove, listdir
import sys

    # modulos base
sys.path.append("../../modules")
from login_code import login
from sendActions import move_file

    # webscraping
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

    # manipulacao dedados
import datetime
from time import sleep
import pandas as pd
from time import strptime
from re import search
import locale
locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')

    # barra de progressao
from tqdm import tqdm


# Classe para baixar tabelas
class download():

    def __init__(self):
        self.credentials = dotenv_values("../data/.env")
        self.return_driver = login(bank = 'crefisa', 
                                   credentials = self.credentials).send_keys(url='https://meumb.mercantil.com.br/propostas',  # insira a URL da página de login
                                                                             element_list = ['#mat-input-0', '#mat-input-1', '.mat-button-wrapper'] #insira o CSS_select do usuario, senha e botao 'enter'
                                                                             )
        self.driver = self.return_driver
    

    def __scroll(self, driver: WebDriverWait):
        
        driver.execute_script("window.scrollBy(0, 3000)")
        sleep(1)
        driver.execute_script("window.scrollBy(3000, 0)")
    

    def __calendar_manipulate(self, date_work: datetime.date, driver: WebDriverWait):
        WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
        try:
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ngx-pagination")))
        except ElementClickInterceptedException:
            driver.refresh()
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ngx-pagination")))

        calendar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#mat-date-range-input-0')))
        driver.execute_script("arguments[0].click();", calendar)
        date_1 = date_work - datetime.timedelta(days = 30)
        date_2 = date_work
        if date_1.strftime("%b %Y").upper() == driver.find_element(By.CSS_SELECTOR, '.mat-calendar-period-button > span:nth-child(1)').text :
        
            result = driver.find_elements(By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')
            
            for i in result:
                if i.text == '{:d}'.format(date_1.day):
                    driver.execute_script("arguments[0].click();", i)
                    break
        else:
            calendario = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.mat-calendar-period-button > span:nth-child(1)')))
            driver.execute_script("arguments[0].click();", calendario)
            result = driver.find_elements(By.CSS_SELECTOR, ".mat-calendar-body > tr")
            
            for i in result:
                datas = i.find_elements(By.CSS_SELECTOR, 'td')
                datas = i.find_elements(By.TAG_NAME, 'td')
                click = False
                for j in datas:
                    sleep(.50)
                    if j.text == str(date_1.strftime("%Y")):
                        driver.execute_script("arguments[0].click();", j)
                        click = True
                        break
                if click:
                    break
                
                        
            resulta_month = driver.find_elements(By.CLASS_NAME, "mat-calendar-body")
            for month in resulta_month:
                result_month = month.find_elements(By.TAG_NAME, 'td')
                click = False
                for i in result_month:
                    if search(date_1.strftime("%b").upper(), i.text):
                        driver.execute_script("arguments[0].click();", i)
                        click = True
                        break
                if click:
                    break
            # iteração nos dias
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')))    
            result = driver.find_elements(By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')

            for i in result:
                if i.text == '{:d}'.format(date_1.day):
                    driver.execute_script("arguments[0].click();", i)
                    break



        sleep(2)
        if date_2.strftime("%b %Y").upper() == driver.find_element(By.CSS_SELECTOR, '.mat-calendar-period-button > span:nth-child(1)').text :
            result = driver.find_elements(By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')
            for i in result:
                if date_2 == datetime.date.today():
                    today = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.mat-calendar-body-today')))
                    driver.execute_script('arguments[0].click();', today)
                    break
                else:
                    if i.text == '{:d}'.format(date_2.day):
                        driver.execute_script("arguments[0].click();", i)
                        break
        
        else:
            
            button_pass = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.mat-focus-indicator:nth-child(4)")))
            driver.execute_script("arguments[0].click();", button_pass)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')))
            result = driver.find_elements(By.XPATH, f'//div[@class="mat-calendar-body-cell-content mat-focus-indicator"]')
            for i in result:
                if i.text == '{:d}'.format(date_2.day):
                    sleep(.50)
                    driver.execute_script("arguments[0].click();", i)
                    break

        try:
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(., 'Sem dados')]")))
            date_work += datetime.timedelta(days = 1)
            print("Sem dados para a datra: ", date_work)
            return False
        except TimeoutException:
            exportar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Exportar')]")))
            driver.execute_script("arguments[0].click();", exportar)
            sleep(3)
            xlsx_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'xlsx')]")))
            # xlsx_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.mat-menu-item')))
            driver.execute_script("arguments[0].click();", xlsx_button)
            

    def __production(self, date_work: datetime.date):
                
                '''

                    Classe para fazer o downlod do relatório de producao.
                    
                    ### date_work: informado no modulo main.py, quando chama a modulo main_download.py

                '''
                

                for i in listdir("./download_tmp/"):
                    remove(f"./download_tmp/{i}")
                driver = self.driver
                # Entrando na página de comissões
                ########################## Inicie aqui o codigo de extracao ##########################|

                # Exemplo

                try:
                    driver.get("https://meumb.mercantil.com.br/propostas")
                    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Meus filtros')]"))).click()
                    try:
                        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'INTEGRADAS')]"))).click()
                    except ElementClickInterceptedException:
                        driver.refresh()
                        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Meus filtros')]"))).click()
                        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'INTEGRADAS')]"))).click()
                    self.__scroll(driver=driver)
                    self.__calendar_manipulate(driver = driver, date_work = date_work)
                except TimeoutException:
                    driver.get("https://meumb.mercantil.com.br/propostas")
                    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Meus filtros')]"))).click()
                    try:
                        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'INTEGRADAS')]"))).click()
                    except ElementClickInterceptedException:
                        driver.refresh()
                        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Meus filtros')]"))).click()
                        WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'INTEGRADAS')]"))).click()
                    self.__scroll(driver=driver)
                    self.__calendar_manipulate(driver = driver, date_work = date_work)
                
        
                ########################## Fim do codigo de extracao ##########################|


    def dowloadProductiion(self, date_work: datetime.date):

        '''

            Executa a classe self.__production() e faz a transferencia do download para a pasta download correta.

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/production/{date_work}.csv'
        
        # Realiza dowenload somente se o download não existir
        if not path.exists(path_to_save):
            try:
                self.__production(date_work=date_work)            
            except TimeoutException:
                self.__production(date_work=date_work)

            # move o arquivo para a pasta correta            
            move_file(date= date_work, type_transference= ['production'])

    def tqdm_bar(self, date_work = datetime.date):
        '''
            Executa as classes anteriores, mostrando barra de progressao.

        '''


        processos = [
                #    ("Download do relatório de comissão crefisa", self.dowloadComission),
                   ("Download do relatório de produção do crefisa", self.dowloadProductiion)
                   ]
        
        with tqdm(total=len(processos), desc="Executando processos") as pbar_total:
            for processo_desc, processo_func in processos:
                
                pbar_total.set_description(processo_desc)
                try:
                    processo_func(date_work = date_work)
                except Exception as exc:
                    raise(exc)
                    
                pbar_total.update(1)

# Debug - exemplo de chamaa do modulo
# download().tqdm_bar(date_work = datetime.date.today())