# imports 
from os import makedirs, path, remove, listdir
import sys

    # modulos base
sys.path.append("../../modules")
from login import login
from sendActions import move_file

    # webscraping
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
    # manipulacao dedados
import datetime
import pandas as pd
from time import strptime

    # barra de progressao
from tqdm import tqdm
import time


# Classe para baixar tabelas
class download_production():

    def __init__(self):
        self.credentials = dotenv_values("../data/.env")
        self.return_driver = login(bank = 'crefisa', 
                                   credentials = self.credentials).send_keys(url='https://desenv.facta.com.br/sistemaNovo/login.php',  # insira a URL da página de login
                                                                             element_list = ['#login', 
                                                                                             '#senha',
                                                                                            '#btnLogin'] #insira o CSS_select do usuario, senha e botao 'enter'
                                                                             )
        self.driver = self.return_driver
        


    def __production(self, date_work: datetime.date):
                
                '''

                    Classe para fazer o downlod do relatório de producao.
                    
                    ### date_work: informado no modulo main.py, quando chama a modulo main_download.py

                '''
                

                for i in listdir("./download_tmp/"):
                    remove(f"./download_tmp/{i}")
                path_to_save = f'../download/{date_work.year}/{date_work.month}/comission/{date_work}.csv'

                # Realiza dowenload somente se o download não existir
                if not path.exists(path_to_save):
                    driver = self.driver
                    date_work_start = (date_work - datetime.timedelta(days = 30)).strftime("%d/%m/%Y")
                    
                    # Entrando na página de comissões
                    ########################## Inicie aqui o codigo de extracao ##########################|
                    
                    #exemplo            
                    try:
                         WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#modalMuralAlertas2 > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)'))).click()
                    except TimeoutException:
                         pass
                    try:
                         button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#modalMuralAlertas > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)')))
                         driver.execute_script("arguments[0].click();", button)
                    except TimeoutException:
                         pass
                    
                    try:
                        driver.get("https://desenv.facta.com.br/sistemaNovo/andamentoPropostas.php")
                        for tag, date in zip(['#periodoini', '#periodofim'], [date_work_start, date_work.strftime("%d/%m/%Y")]):
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag))).send_keys(0)
                            for _ in range(0, 8):
                                    driver.find_element(By.CSS_SELECTOR, tag).send_keys(Keys.BACKSPACE)

                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag))).send_keys(date)
                            
                        button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#pesquisar')))
                        driver.execute_script("arguments[0].click();", button)
                        propopsta = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID,"tblListaProposta")))
                        tabela = propopsta.get_attribute("outerHTML")
                        tabela_lida = pd.read_html(tabela)[0]
                        tabela_lida = tabela_lida.iloc[:tabela_lida.shape[0]-1, :]
                        tabela_lida['Data Cadastro'] = pd.to_datetime(tabela_lida['Data Cadastro'], format='%d/%m/%Y %H:%M').dt.strftime("%d/%m/%Y")
                        iterable_day = 1
                        date_search = date_work
                        while not tabela_lida['Data Cadastro'].isin([date_search.strftime("%d/%m/%Y")]).any():
                            time.sleep(5)
                            propopsta = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID,"tblListaProposta")))
                            tabela = propopsta.get_attribute("outerHTML")
                            tabela_lida = pd.read_html(tabela)[0]
                            tabela_lida = tabela_lida.iloc[:tabela_lida.shape[0]-1, :]
                            tabela_lida['Data Cadastro'] = pd.to_datetime(tabela_lida['Data Cadastro'], format='%d/%m/%Y %H:%M').dt.strftime("%d/%m/%Y")
                            iterable_day = 1
                            date_search = (date_search + datetime.timedelta(days = iterable_day))
                            
                            
                        button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#botaoExcel > a:nth-child(1)')))
                        driver.execute_script("arguments[0].click();", button)

                    except TimeoutException:
                        driver.refresh()
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gap-1 > div:nth-child(2) > a:nth-child(1)'))).click()
                        
                ########################## Fim do codigo de extracao ##########################|


    def dowloadPrducion(self, date_work: datetime.date):

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
                    ("Download do relatório de produção FACTA", self.dowloadPrducion)
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
# download_production().tqdm_bar(date_work = datetime.date.today())