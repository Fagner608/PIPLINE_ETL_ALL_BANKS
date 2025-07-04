# import send action
from os import makedirs, path, remove, listdir
import sys


sys.path.append("../../modules")
from logger import loogerControls
from login_code import login
from sendActions import move_file


from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


import datetime
import pandas as pd
import polars as pl
from time import strptime

from tqdm import tqdm


import locale
import datetime
import time
from re import search




# Classe para baixar tabeças
class download_importados_storm():

    def __init__(self):
        self.logger = loogerControls().loggerFunction()
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

    def calendar_manipulate(self, days_diff: datetime.timedelta):
            locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
            
            start_date = datetime.date.today() - days_diff
            
            
            print(start_date)
            self.__calendar_handle(path = '#data-picker-filtro-inicio > span:nth-child(2)', date = start_date)


    def __importation(self, bank: str, days_diff: datetime.timedelta):
                
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
            button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.st-item:nth-child(12) > a:nth-child(1) > div:nth-child(1) > span:nth-child(2)')))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", button)
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
            self.calendar_manipulate(days_diff=days_diff)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ed-form-indicadores-submit'))).click()#ed-form-indicadores-submit
            time.sleep(1)
            ## fazer um loop dos últimos 15 arquivos
            ## colocar todos na pasta download_tmp
            ## consolidar com polars e transferir para o download
            #encontrar tr
            
            n_elements = len(driver.find_elements(By.CSS_SELECTOR, '#tabela-indicadores-cms > tbody:nth-child(2) > tr'))
            # max_range = 16 if n_elements > 16 else n_elements
            max_range =  n_elements
            element_click_list = []
            for element in range(1, max_range):
                try:
                    button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#tabela-indicadores-cms > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(9) > div:nth-child(1) > a:nth-child(1) > i:nth-child(1)')))
                    driver.execute_script("arguments[0].click();", button)                                                                                              
                except Exception as exc:
                    self.logger.critical(f"Falha ao fazer o download do botão {element} do relatório de importação: ")
                    element_click_list.append(element)
            
                while any(file.endswith(".part") for file in listdir("./download_tmp")):
                    time.sleep(2)
                    continue

                time.sleep(2)

            if len(element_click_list) > 0:
                element_click_list_two = []
                for element in element_click_list:
                    try:
                        button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#tabela-indicadores-cms > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(9) > div:nth-child(1) > a:nth-child(1) > i:nth-child(1)')))
                        driver.execute_script("arguments[0].click();", button)                                                                                              
                    except Exception as exc:
                        self.logger.critical(f"Falha na segunda tentativa ao fazer o download dos relatorios de importacao")
                        element_click_list_two.append(element)
                
                    while any(file.endswith(".part") for file in listdir("./download_tmp")):
                        time.sleep(2)
                        continue

                    time.sleep(2)
            downloadded_files = len(listdir("./download_tmp"))
            if  downloadded_files != (max_range - 1):
                self.logger.warning(f"O numero de arquivos de importacao baixados ({downloadded_files}) e menor do que o esperado ({max_range - 1}). Algumas propostas podem nao ter o status de importacao corretamente gerenciadas.")
            else:
                self.logger.info("Downloads dos arquivos de importacao finalizado com sucesso.")

            time.sleep(6)
            ## consolidar arquivos com polars
            csv_to_read = [x  for x in listdir("./download_tmp") if x.endswith(".csv")]
            lazzy_dfs = [
                pl.scan_csv("./download_tmp/" + file, 
                    separator=';', 
                    encoding = 'utf8-lossy')
                    .select(['Nome Arquivo', 'ADE'])
                    .with_columns(pl.col('ADE').cast(pl.Utf8))
                    for file in csv_to_read
                ]
            

            df_concate = pl.concat(lazzy_dfs).collect()
            
            for i in listdir("./download_tmp/"):
                remove(f"./download_tmp/{i}")
            
            try:
                root = f'./download_tmp/'
                path_to_save = root + f'importados_consolidado.parquet'
                makedirs(root, exist_ok=True)                
                df_concate.write_parquet(path_to_save)
                self.logger.info(f"Dados de importacao consolidados com sucesso.")
            
            except Exception as exc:
                self.logger.error(f"Erro ao persistir dados de importacao: {exc}.")


    def dowloadImportation(self, date_work: datetime.date, bank: str, days_diff: datetime.timedelta):

        '''

            Classe para fazer o downlod do relatório de comissão.
            
            ### date_work: informe a data de pesquisa no formato datetime.date

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/importation/{date_work}.csv'
        self.__importation(bank=bank, days_diff=days_diff)  
        move_file(date= date_work, type_transference= ['importation'])


    def tqdm_bar(self, bank: str, date = datetime.datetime, days_diff: datetime.timedelta = datetime.timedelta(days = 15)):

        processos = [("Download do relatório de importacao do v8", self.dowloadImportation)]


        with tqdm(total=len(processos), desc="Executando processos") as pbar_total:
            for processo_desc, processo_func in processos:
                
                pbar_total.set_description(processo_desc)
                try:
                    processo_func(date_work = date.date(), bank = bank, days_diff=days_diff)
                except Exception as exc:
                    raise(exc)
                    
                pbar_total.update(1)

# Debug

# download_importados_storm().tqdm_bar(date = datetime.datetime.today(), bank = 'V8 DIGITAL')