# import send action
from os import makedirs, path, remove, listdir
import sys


sys.path.append("../../modules")
from login import login
from sendActions import move_file


from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


import datetime
import pandas as pd
from time import strptime

from tqdm import tqdm


import locale
import datetime
import time
from re import search


# Classe para baixar tabeças
class download_importados_storm():

    def __init__(self):
        self.credentials = dotenv_values("../data/.env")
        self.return_driver = login(bank = 'storm', ## Insria o nome do banco
                                   credentials = self.credentials).send_keys(storm = True,
                                                                             url='https://maisagilgestao.stormfin.com.br/',
                                                                             element_list = ['#usuario', '#senha', '.btn']) ## insira a URL do banco e CSS_SELECTOR do login, senha e entrar
        self.driver = self.return_driver


    def __click_button_css_selector(self, path: str, name_button: str):
        driver = self.driver
        try:
            button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'{path}')))
            driver.execute_script("arguments[0].click()", button)
        except:
            print(f"Erro o clicar no {name_button}'")
            raise


    def __calendar_handle(self, path: str, date: datetime.date):
        driver = self.driver
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'{path}'))).click()
        
        time.sleep(2)
        calendar_year = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.bootstrap-datetimepicker-widget > div > div > table > thead > tr > th:nth-child(2)'))).text.upper()
                                                                                                            
        while date.strftime("%B %Y").upper() != calendar_year:
            if int(calendar_year.split(" ")[1]) >= date.year:
                if search('inicio', path):
                    self.__click_button_css_selector(path = 'div.bootstrap-datetimepicker-widget > div > div > table > thead > tr > th:nth-child(1)', name_button = 'Encontrar mês')
                    calendar_year = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.bootstrap-datetimepicker-widget > div > div > table > thead > tr > th:nth-child(2)'))).text.upper()
                time.sleep(1)
                

        try:
            elements = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.datepicker-days > table:nth-child(1)'))) 
        except:
            elements = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.bootstrap-datetimepicker-widget > div > div:nth-child(1)')))


        calendar_element = elements.find_elements(By.CSS_SELECTOR, 'tbody')
                                                    
        found_first_day = False
        linha = 0
        for i in calendar_element:
            result = i.find_elements(By.CSS_SELECTOR, 'tr')
            linha += 1
            for j in result:
                day = j.find_elements(By.CSS_SELECTOR, 'td')
                for k in day:
                    if k.text.isdigit() and int(k.text) == 1:
                        found_first_day = True
                    day = j.find_elements(By.CSS_SELECTOR, 'td')
                    if k.text.isdigit():
                        if str(k.text) == str(date.day):
                            if found_first_day:
                                driver.execute_script("arguments[0].click();", k)
                                # driver.find_element(By.CSS_SELECTOR, '#cod_contrato').click()
                                return
                else: continue

    def calendar_manipulate(self):
            locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
            
            start_date = datetime.date.today() - datetime.timedelta(days = 30)
            
            
            print(start_date)
            self.__calendar_handle(path = '#data-picker-filtro-inicio > span:nth-child(2)', date = start_date)


    def __importation(self, bank: str):
                
            '''
                Download dos dados numa janela de D-20 até D+1
            '''

            # ajustar esta parte para fazer a exclusão dos download na pasta do banco
            for i in listdir("./download_tmp/"):
                remove(f"./download_tmp/{i}")
            driver = self.driver
            # Entrando na página de comissões
            ################ inicio do seu seu codigo ################
            time.sleep(1)
            WebDriverWait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            butoon = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.st-item:nth-child(12) > a:nth-child(1) > div:nth-child(1) > span:nth-child(2)')))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", butoon)
            time.sleep(1)
            try:
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.st-sub-menu:nth-child(13) > a:nth-child(19)'))).click()
            except ElementClickInterceptedException:
                button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.st-sub-menu:nth-child(13) > a:nth-child(19)')))
                driver.execute_script("arguments[0].click();", button)
            time.sleep(1)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.panel-heading'))).click()
            time.sleep(1)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#filtroBanco'))).click()
            time.sleep(1)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//option[contains(text(), '{bank.upper()}')]"))).click()
            self.calendar_manipulate()
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ed-form-indicadores-submit'))).click()#ed-form-indicadores-submit
            time.sleep(1)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ed-form-indicadores-unificado'))).click()#ed-form-indicadores-unificado
            
            ################ fim do seu seu codigo ################
            time.sleep(6)

    def dowloadImportation(self, date_work: datetime.date, bank: str):

        '''

            Classe para fazer o downlod do relatório de comissão.
            
            ### date_work: informe a data de pesquisa no formato datetime.date

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/importation/{date_work}.csv'
        self.__importation(bank=bank)  
        move_file(date= date_work, type_transference= ['importation'])


    def tqdm_bar(self, bank: str, date = datetime.date):

        processos = [("Download do relatório de importacao do crefisa", self.dowloadImportation)]


        with tqdm(total=len(processos), desc="Executando processos") as pbar_total:
            for processo_desc, processo_func in processos:
                
                pbar_total.set_description(processo_desc)
                try:
                    processo_func(date_work = date, bank = bank)
                except Exception as exc:
                    raise(exc)
                    
                pbar_total.update(1)

# Debug
# date = datetime.date(2024, 6, 5)
# download_importados_storm().tqdm_bar(date_work = date, bank = 'crefisa')