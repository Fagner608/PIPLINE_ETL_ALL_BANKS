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


# Classe para baixar tabeças
class download():

    def __init__(self):
        self.credentials = dotenv_values("../data/.env")
        self.return_driver = login(bank = 'crefisa', 
                                   credentials = self.credentials).send_keys(url='https://app1.gerencialcredito.com.br/CREFISA/default.asp', element_list = ['#txtUsuario', '#txtSenha', '#btnLogin'])
        self.driver = self.return_driver
        

    def dowloadComission(self, date_work: datetime.date):

        '''

            Classe para fazer o downlod do relatório de comissão.
            
            ### date_work: informe a data de pesquisa no formato datetime.date

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/comission/{date_work}.csv'

        # Realiza dowenload somente se o download não existir
        if True:
            driver = self.driver
            # Entrando na página de comissões
            try:
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#menu1'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#listaMenu1 > li:nth-child(2) > a:nth-child(1)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtAutenticacaoSenhaFinanceira'))).send_keys(self.credentials['USER_AUTHENTICATION'])
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.btn:nth-child(2)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.swal2-confirm'))).click()
            except TimeoutException:
                driver.refresh()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#menu1'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#listaMenu1 > li:nth-child(2) > a:nth-child(1)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtAutenticacaoSenhaFinanceira'))).send_keys(self.credentials['USER_AUTHENTICATION'])
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.btn:nth-child(2)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.swal2-confirm'))).click()

            
            result = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#tableNaoLiberados')))
            html_data = result.get_attribute('outerHTML')
            date_2 = date_work - datetime.timedelta(days = 7)
            date_2 = pd.Timestamp(date_2)
            tabela = pd.read_html(html_data)[0]
            tabela['PG Cliente'] = pd.to_datetime(tabela['PG Cliente'], format='%d/%m/%Y')
            tabela = tabela[tabela['PG Cliente'] >= date_2]
            # tabela = tabela[tabela['PG Cliente'].str.strptime('%d/%m/%Y') >= date_2]
            try:    
                tabela.to_csv(path_to_save, index=False, decimal = ',')
            except FileNotFoundError:
                makedirs(path_to_save, exist_ok = True)
                tabela.to_csv(path_to_save, index=False, decimal = ',')
        


    def __production(self, date_work: datetime.date):
                
                '''
                    Download dos dados numa janela de D-4 até D=1
                '''
                for i in listdir("./download_tmp/"):
                    remove(f"./download_tmp/{i}")
                driver = self.driver
                date_2 = date_work - datetime.timedelta(days = 7)
                # Entrando na página de comissões
                try:
                    button = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#menu4')))
                    driver.execute_script('arguments[0].click();', button)
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#listaMenu4 > li:nth-child(2) > a:nth-child(1)'))).click()
                except TimeoutException:
                    WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#menu4'))).click()
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#listaMenu4 > li:nth-child(2) > a:nth-child(1)'))).click()
                    
                

                try:
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtAutenticacaoSenhaFinanceira'))).send_keys(self.credentials['USER_AUTHENTICATION'])
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.btn:nth-child(2)'))).click()
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.swal2-confirm'))).click()
                except TimeoutException:
                    pass            
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).clear()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).send_keys(date_2.strftime("%d/%m/%Y"))
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).clear()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).send_keys(datetime.date.today().strftime("%d/%m/%Y"))
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado'))).click()

                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoDeData > option:nth-child(1)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoDeData > option:nth-child(1)'))).click()

                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlStatusPagCliente > option:nth-child(3)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlStatusPagCliente > option:nth-child(3)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado > option:nth-child(1)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado > option:nth-child(1)'))).click()
                WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btn'))).click()
                
                try:
                    allert = driver.switch_to.alert
                    driver_alert = allert.text

                    if driver_alert == 'NENHUM RESULTADO FOI ENCONTRADO.':
                        allert.dismiss()
                        # Salvando arquivo vazio

                except NoAlertPresentException:
                    pass
        

    def dowloadProductiion(self, date_work: datetime.date):

        '''

            Classe para fazer o downlod do relatório de comissão.
            
            ### date_work: informe a data de pesquisa no formato datetime.date

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/production/{date_work}.csv'
        if not path.exists(path_to_save):
            try:
                # Realiza dowenload somente se o download não existir
                self.__production(date_work=date_work)            
            except TimeoutException:
                self.__production(date_work=date_work)            
            move_file(date= date_work, type_transference= ['production'])

    def tqdm_bar(self, date_work = datetime.date):

        processos = [("Download do relatório de produção do crefisa", self.dowloadProductiion)]
        # processos = [("Download do relatório de comissão crefisa", self.dowloadComission),
        #            ("Download do relatório de produção do crefisa", self.dowloadProductiion)]
        
        with tqdm(total=len(processos), desc="Executando processos") as pbar_total:
            for processo_desc, processo_func in processos:
                
                pbar_total.set_description(processo_desc)
                try:
                    processo_func(date_work = date_work)
                except Exception as exc:
                    raise(exc)
                    
                pbar_total.update(1)

# Debug
# download().tqdm_bar(date_work = date)