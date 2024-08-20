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
import time

    # barra de progressao
from tqdm import tqdm

    #warnings
import warnings
warnings.filterwarnings('ignore')


# Classe para baixar tabelas
class download():

    def __init__(self):
        self.credentials = dotenv_values("../data/.env")
        self.return_driver = login(bank = 'crefisa', 
                                   credentials = self.credentials).send_keys(url='https://comissoes.factafinanceira.com.br/',  # insira a URL da página de login
                                                                             element_list = ['fieldset.relative:nth-child(2) > div:nth-child(1) > input:nth-child(2)', 
                                                                                             'fieldset.relative:nth-child(3) > div:nth-child(1) > input:nth-child(2)',
                                                                                               'button.flex'] #insira o CSS_select do usuario, senha e botao 'enter'
                                                                             )
        self.driver = self.return_driver
        


    def __contaCorrente(self, date_work: datetime.date):
                
                '''

                    Classe para fazer o downlod do relatório de producao.
                    
                    ### date_work: informado no modulo main.py, quando chama a modulo main_download.py

                '''
                

                for i in listdir("./download_tmp/"):
                    remove(f"./download_tmp/{i}")
                path_to_save = f'../download/{date_work.year}/{date_work.month}/extra/{date_work}.csv'

                # Realiza dowenload somente se o download não existir
                # if not path.exists(path_to_save):
                if True:
                    driver = self.driver
                    date_work_start = (date_work - datetime.timedelta(days = 30))
                    date_work = date_work.strftime("%d/%m/%Y")
                    # Entrando na página de comissões
                    ########################## Inicie aqui o codigo de extracao ##########################|
                    
                    #exemplo            
                    try:
                        button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gap-1 > div:nth-child(2) > a:nth-child(1)')))
                        driver.execute_script("arguments[0].click();", button)
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[2]'))).click()
                        for tag, date in zip(['#dataCadastroIniP', '#dataCadastroFimP'], [date_work_start.strftime("%d/%m/%Y"), date_work]):
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag))).send_keys(0)
                            for _ in range(0, 8):
                                    driver.find_element(By.CSS_SELECTOR, tag).send_keys(Keys.BACKSPACE)

                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag))).send_keys(date)
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag))).send_keys(date)
                        ActionChains(driver).send_keys(Keys.TAB)
                        button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[2]/button[1]')))
                        driver.execute_script("arguments[0].click();", button)
                        
                        ## Aguardar data da efetivação
                        time.sleep(5)
                        teste_table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.min-w-full')))
                        table = teste_table.get_attribute('outerHTML')
                        teste_leitura = pd.read_html(table)[0]
                        iterable_day = 1
                        date_search = (date_work_start + datetime.timedelta(days = iterable_day))
                        while not teste_leitura['DATA'].isin([date_search.strftime("%d/%m/%Y")]).any():
                            time.sleep(5)
                            teste_table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.min-w-full')))
                            table = teste_table.get_attribute('outerHTML')
                            teste_leitura = pd.read_html(table)[0]
                            iterable_day += 1
                            date_search = (date_work_start + datetime.timedelta(days = iterable_day))
                            
                        button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.bg-facta400')))
                        driver.execute_script("arguments[0].click();", button)

                    except TimeoutException:
                        driver.refresh()
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gap-1 > div:nth-child(2) > a:nth-child(1)'))).click()
                        
                ########################## Fim do codigo de extracao ##########################|
                

    def dowloadContaCorrente(self, date_work: datetime.date):

        '''

            Executa a classe self.__contaCorrente() e faz a transferencia do download para a pasta download correta.

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/extra/{date_work}.csv'
        
        # Realiza dowenload somente se o download não existir
        if not path.exists(path_to_save):
            try:
                self.__contaCorrente(date_work=date_work)            
            except TimeoutException:
                self.__contaCorrente(date_work=date_work)

            # move o arquivo para a pasta correta            
            move_file(date= date_work, type_transference= ['extra'])

   
    def __comission(self, date_work: datetime.date):
                
                '''

                    Classe para fazer o downlod do relatório de producao.
                    
                    ### date_work: informado no modulo main.py, quando chama a modulo main_download.py

                '''
                

                for i in listdir("./download_tmp/"):
                    remove(f"./download_tmp/{i}")
                path_to_save = f'../download/{date_work.year}/{date_work.month}/comission/{date_work}.csv'



                # if not path.exists(path_to_save):
                if True:
                    driver = self.driver
                    date_work_start = (date_work - datetime.timedelta(days = 20))
                    date_work = date_work.strftime("%d/%m/%Y")
                    # Entrando na página de comissões
                    ########################## Inicie aqui o codigo de extracao ##########################|
                    
                    #exemplo             
                    try:
                        # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gap-1 > div:nth-child(3) > a:nth-child(1)'))).click()
                        driver.get("https://comissoes.factafinanceira.com.br/relatorio-a-vista")
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[1]/div[2]'))).click()
                        for tag, date in zip(['#dataCadastroIniP', '#dataCadastroFimP'], [date_work_start.strftime("%d/%m/%Y"), date_work]):
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag))).send_keys(0)
                            for _ in range(0, 8):
                                    driver.find_element(By.CSS_SELECTOR, tag).send_keys(Keys.BACKSPACE)

                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag))).send_keys(date)
                            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, tag))).send_keys(date)
                        ActionChains(driver).send_keys(Keys.TAB)

                        ################### problema esta aqui ###################
                        
                        button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[2]/button[1]')))
                        driver.execute_script("arguments[0].click();", button)
                        driver.execute_script("arguments[0].click();", button)
                        ## Aguardar data da efetivação
                        time.sleep(5)
                        teste_table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.min-w-full')))
                        table = teste_table.get_attribute('outerHTML')
                        teste_leitura = pd.read_html(table)[0]
                        iterable_day = 1
                        date_search = (date_work_start + datetime.timedelta(days = iterable_day))
                        while not teste_leitura['EFETIVAÇÃO'].isin([date_search.strftime("%d/%m/%Y")]).any():
                            time.sleep(5)
                            teste_table = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.min-w-full')))
                            table = teste_table.get_attribute('outerHTML')
                            teste_leitura = pd.read_html(table)[0]
                            iterable_day += 1 
                            date_search = (date_work_start + datetime.timedelta(days = iterable_day))
                        
                        button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.bg-facta400')))
                        driver.execute_script("arguments[0].click();", button)

                    except TimeoutException:
                        driver.refresh()
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.gap-1 > div:nth-child(2) > a:nth-child(1)'))).click()
                        
                ########################## Fim do codigo de extracao ##########################|
                
    def dowloadComission(self, date_work: datetime.date):

        '''

            Executa a classe self.__production() e faz a transferencia do download para a pasta download correta.

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/comission/{date_work}.csv'
        
        # Realiza dowenload somente se o download não existir
        if not path.exists(path_to_save):
            try:
                self.__comission(date_work=date_work)            
            except:
                self.__comission(date_work=date_work)

            # move o arquivo para a pasta correta            
            move_file(date= date_work, type_transference= ['comission'])

    def tqdm_bar(self, date_work = datetime.date):
        '''
            Executa as classes anteriores, mostrando barra de progressao.

        '''


        processos = [
            #  ("Download do relatório de conta corrente FACTA", self.dowloadContaCorrente),
             ("Download do relatório de comissão FACTA", self.dowloadComission)
             ]
        
        with tqdm(total=len(processos), desc="Executando processos") as pbar_total:
            for processo_desc, processo_func in processos:
                
                pbar_total.set_description(processo_desc)
                try:
                    processo_func(date_work = date_work)
                except Exception as exc:
                    raise(exc)
                    
                pbar_total.update(1)

# Debug - exemplo de chamar do modulo
# download().tqdm_bar(date_work = datetime.date.today())