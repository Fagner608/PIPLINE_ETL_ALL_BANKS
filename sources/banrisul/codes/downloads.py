# imports 
from os import makedirs, path, remove, listdir
import sys

    # modulos base
sys.path.append("../../modules")
from sendActions import move_file
from sendActions import sendAction
from openBrowser import openFirefox

    # webscraping
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

    # manipulacao dedados
import datetime
import pandas as pd
import time
from time import strptime

    # barra de progressao
from tqdm import tqdm


# Classe para baixar tabelas
class download():

    def __init__(self):
        self.credentials = dotenv_values("../data/.env")
        self.return_driver = self.__send_keys(bank = 'banrisul', url="https://bemweb.bempromotora.com.br/autenticacao/login?redirect=%2Fdashboard",  # insira a URL da página de login
                                                                            #  element_list = ['#usuario', '#txtSenha', '#btnLogin'] #insira o CSS_select do usuario, senha e botao 'enter'
                                                                             element_list = ['#usuario', '#btn-login', '#senha', '#btn-login', '#pin'] #insira o CSS_select do usuario, senha e botao 'enter'
                                                                             ) # type: ignore
        self.driver = self.return_driver
        



    def __send_keys(self, url: str, bank: str, element_list: list, storm = False):

        #usuario, clica
        # depois abre senha e recaptcha

        driver = openFirefox()._initializeDriver(bank = bank)
        driver.get(url)
        sendAction(driver = driver,
                        action='send_keys',
                        element= element_list[0], 
                        key = self.credentials['LOGIN_USER'] if not storm else self.credentials['LOGIN_USER_STORM'])
        
        sendAction(driver = driver,
                            action='click',
                            element= element_list[1])
        
        sendAction(driver = driver,
                        action='send_keys',
                        element= element_list[2], 
                        key = self.credentials['LOGIN_PASSWORD'] if not storm else self.credentials['LOGIN_PASSWORD_STORM'])
        
        
        # tentar inputar o PIN
        input_pin = input("Informe o PIN aqui:")
        sendAction(driver = driver,
                        action='send_keys',
                        element= element_list[4], 
                        key = input_pin)
        
        sendAction(action='waitCaptcha')
        try:
            sendAction(driver = driver,
                            action='click',
                            element= element_list[3])
        except TimeoutException:
            pass
       
        return driver    



    def __Comission(self, date_work: datetime.date):

        '''

            Classe para fazer o downlod do relatório de comissão.
            
            ### date_work: informado no modulo main.py, quando chama a modulo main_download.py

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/comission/{date_work}.csv'

        # Realiza dowenload somente se o download não existir
        driver = self.driver
        # Entrando na página de comissões
        ########################## Inicie aqui o codigo de extracao ##########################|
        date_ini = date_work - datetime.timedelta(days = 30)
        #exemplo
        WebDriverWait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(10)
        try:
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.MuiButton-text:nth-child(1)'))).click()
            except TimeoutException:
                pass
            WebDriverWait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            # clica em consignado no 'menu'
            driver.get('https://bemweb.bempromotora.com.br/consignado/consulta-comissao')

            WebDriverWait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

            driver.find_element(By.ID,"efetivacaoDataIni").find_elements(By.TAG_NAME,"svg")[-1].click() 

            driver.find_element(By.ID,"pagamentoDataIni").find_elements(By.TAG_NAME,"input")[0].click()
            time.sleep(0.5)
            
            driver.find_element(By.XPATH,"//*[contains(@class, 'ant-calendar-picker-container')]").find_elements(By.XPATH, "//input[@placeholder='Data de início']")[3].send_keys(date_ini.strftime("%d/%m/%Y"))
            time.sleep(0.5)
            
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ant-calendar-today'))).click()
            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class, 'ant-calendar-range-part') and contains(@class, 'ant-calendar-range-right')]//div[text()='{int(date_work.strftime('%d'))}']"))).click()

            driver.find_element(By.XPATH,"//button[contains(@class, 'ant-btn-primary')]//*[contains(., 'Visualizar')]/..").click()

            try:
                if WebDriverWait(driver,timeout=10).until(EC.visibility_of_element_located((By.XPATH,"//div[contains(text(), 'Não foram encontrados registros.')]"))).is_displayed():
                    print("Sem registros!")
                    return
            except:
                pass

            try:
                element = WebDriverWait(driver,timeout=100).until(EC.visibility_of_element_located((By.XPATH,"//*[starts-with(@class, 'relatorio')]")))
            except Exception:
                raise 

            time.sleep(5)
            WebDriverWait(element,timeout=30).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@class, 'ant-btn ant-btn-dashed')]//*[contains(., 'Download XLSX')]/.."))).click()

            time.sleep(6)


        except TimeoutException:
            driver.refresh()
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.MuiButton-text:nth-child(1)'))).click()
            except TimeoutException:
                pass
            WebDriverWait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            # clica em consignado no 'menu'
            driver.get('https://bemweb.bempromotora.com.br/consignado/consulta-comissao')

            WebDriverWait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

            driver.find_element(By.ID,"efetivacaoDataIni").find_elements(By.TAG_NAME,"svg")[-1].click() 

            driver.find_element(By.ID,"pagamentoDataIni").find_elements(By.TAG_NAME,"input")[0].click()
            time.sleep(0.5)
            
            driver.find_element(By.XPATH,"//*[contains(@class, 'ant-calendar-picker-container')]").find_elements(By.XPATH, "//input[@placeholder='Data de início']")[3].send_keys(date_ini.strftime("%d/%m/%Y"))
            time.sleep(0.5)
            
            # driver.find_element(By.CLASS_NAME,"ant-calendar-range-part ant-calendar-range-right").find_element(By.CLASS_NAME, 'ant-calendar-body').find_element(By.XPATH,"//div[text()='{}']".format(int(date_work.strftime("%d")))).click()

            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(@class, 'ant-calendar-range-part') and contains(@class, 'ant-calendar-range-right')]//div[text()='{int(date_work.strftime('%d'))}']"))).click()
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ant-calendar-today'))).click()
            # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ant-calendar-today'))).send_keys(date_work.strftime("%d/%m/%Y"))

            driver.find_element(By.XPATH,"//button[contains(@class, 'ant-btn-primary')]//*[contains(., 'Visualizar')]/..").click()

            try:
                if WebDriverWait(driver,timeout=10).until(EC.visibility_of_element_located((By.XPATH,"//div[contains(text(), 'Não foram encontrados registros.')]"))).is_displayed():
                    print("Sem registros!")
                    return
            except:
                pass

            try:
                element = WebDriverWait(driver,timeout=100).until(EC.visibility_of_element_located((By.XPATH,"//*[starts-with(@class, 'relatorio')]")))
            except Exception:
                raise 

            time.sleep(5)
            WebDriverWait(element,timeout=30).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@class, 'ant-btn ant-btn-dashed')]//*[contains(., 'Download XLSX')]/.."))).click()

            time.sleep(6)



    def dowloadComission(self, date_work: datetime.date):

        '''

            Executa a classe self.__comission() e faz a transferencia do download para a pasta download correta.

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/comission/{date_work}.csv'
        
        # Realiza dowenload somente se o download não existir
        try:
                self.__Comission(date_work=date_work)            
        except TimeoutException:
                self.__Comission(date_work=date_work)

            # move o arquivo para a pasta correta            
        move_file(date= date_work, type_transference= ['comission'])

    def tqdm_bar(self, date_work = datetime.date):
        '''
            Executa as classes anteriores, mostrando barra de progressao.

        '''


        processos = [
                    ("Download do relatório de comissão Banrisul", self.dowloadComission)
                    ]
        
        with tqdm(total=len(processos), desc="Executando processos") as pbar_total:
            for processo_desc, processo_func in processos:
                
                pbar_total.set_description(processo_desc)
                try:
                    processo_func(date_work = date_work)
                except Exception as exc:
                    raise(exc)
                    
                pbar_total.update(1)

# Debug - exemplo de chamada do modulo
# download().tqdm_bar(date_work = datetime.date.today())