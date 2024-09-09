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
from selenium.webdriver import Keys, ActionChains

    # manipulacao dedados
import datetime
import pandas as pd
from time import strptime
import time

    # barra de progressao
from tqdm import tqdm


# Classe para baixar tabelas
class download():

    def __init__(self):
        self.credentials = dotenv_values("../data/.env")
        self.return_driver = login(bank = 'nova_pan', 
                                   credentials = self.credentials).send_keys(url='https://sistema.novafinanceira.com/consignado/CorretorExterno/inicio',  # insira a URL da página de login
                                                                             element_list = ['#usuario', '#senha', '.btn'] #insira o CSS_select do usuario, senha e botao 'enter'
                                                                             )
        self.driver = self.return_driver
        

    def Comission(self, date_work: datetime.date):

        '''

            Classe para fazer o downlod do relatório de comissão.
            
            ### date_work: informado no modulo main.py, quando chama a modulo main_download.py

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/comission/{date_work}.csv'

        # Realiza dowenload somente se o download não existir
        driver = self.driver
        date_to = date_work
        date_from = date_to - datetime.timedelta(days = 30)
        # Entrando na página de comissões
        ########################## Inicie aqui o codigo de extracao ##########################|
        
        #exemplo
        WebDriverWait(driver, 20).until(lambda driver: driver.execute_script("return document.readyState") == 'complete')            
        try:
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'st-icon bi bi-currency-dollar')]"))).click()
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'Exportação de Comissão') and .//i[@class='bi bi-file-arrow-down-fill']]"))).click()
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'btn btn-warning ed-contra-senha ed-cursor-pointer')]"))).click()
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'contra_senha')))
            except TimeoutException as exc:
                WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
                button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'btn btn-warning ed-contra-senha ed-cursor-pointer')]")))
                driver.execute_script("arguments[0].click();", button)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'contra_senha')))
            except TimeoutException:
                pass    
            driver.find_element(By.ID, 'contra_senha').send_keys(self.credentials['USER_AUTHENTICATION'])
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'btn-yes'))).click()
        ## iniciar inserção de datas
            for input_camp, date_insert in zip(['data_inicio', 'data_fim'], [date_from, date_to]):
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, 'data_inicio')]")))
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, 'data_fim')]")))    
                    for _ in range(0, 20):
                        time.sleep(.5)
                        try:
                            driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(Keys.BACKSPACE)
                            # pass
                        except NoSuchElementException:
                            time.sleep(2)
                            driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(Keys.BACKSPACE)
                    time.sleep(2)
                    driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(datetime.datetime.strftime(date_insert, "%d/%m/%Y"))
                    time.sleep(2)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ed-download-arquivo-contratos-digitados")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
            
        except TimeoutException:
            driver.refresh()
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'st-icon bi bi-currency-dollar')]"))).click()
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(., 'Exportação de Comissão') and .//i[@class='bi bi-file-arrow-down-fill']]"))).click()
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'btn btn-warning ed-contra-senha ed-cursor-pointer')]"))).click()
            WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'contra_senha')))
            except TimeoutException as exc:
                WebDriverWait(driver,200 ).until(lambda x:  x.execute_script("return document.readyState"))
                button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//a[contains(@class, 'btn btn-warning ed-contra-senha ed-cursor-pointer')]")))
                driver.execute_script("arguments[0].click();", button)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'contra_senha')))
            except TimeoutException:
                pass    
            driver.find_element(By.ID, 'contra_senha').send_keys(self.credentials['USER_AUTHENTICATION'])
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'btn-yes'))).click()
        ## iniciar inserção de datas
            for input_camp, date_insert in zip(['data_inicio', 'data_fim'], [date_from, date_to]):
                    print(input_camp)
                    print(date_insert)
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, 'data_inicio')]")))
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id, 'data_fim')]")))    
                    for _ in range(0, 20):
                        try:
                            driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(Keys.BACKSPACE)
                            # pass
                        except NoSuchElementException:
                            time.sleep(2)
                            driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(Keys.BACKSPACE)
                    time.sleep(2)
                    driver.find_element(By.XPATH, f"//input[contains(@id, '{input_camp}')]").send_keys(datetime.datetime.strftime(date_insert, "%d/%m/%Y"))
                    time.sleep(2)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "ed-download-arquivo-contratos-digitados")))
            time.sleep(1)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
            
        
        ########################## Fim do codigo de extracao ##########################|
        
        #Exemplo para persistir dados se for um dataframe

        # try:    
        #     tabela.to_csv(path_to_save, index=False, decimal = ',')
        # except FileNotFoundError:
        #     makedirs(path_to_save, exist_ok = True)
        #     tabela.to_csv(path_to_save, index=False, decimal = ',')
    



    def dowloadComission(self, date_work: datetime.date):

        '''

            Executa a classe self.Comission() e faz a transferencia do download para a pasta download correta.

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/comission/{date_work}.csv'
        
        # Realiza dowenload somente se o download não existir
        # if not path.exists(path_to_save):
        if True:
            try:
                self.Comission(date_work=date_work)            
            except TimeoutException:
                self.Comission(date_work=date_work)

            # move o arquivo para a pasta correta            
            move_file(date= date_work, type_transference= ['comission'])



    def __production(self, date_work: datetime.date):
                
                '''

                    Classe para fazer o downlod do relatório de producao.
                    
                    ### date_work: informado no modulo main.py, quando chama a modulo main_download.py

                '''
                

                for i in listdir("./download_tmp/"):
                    remove(f"./download_tmp/{i}")
                driver = self.driver
                date_2 = date_work - datetime.timedelta(days = 7)
                # Entrando na página de comissões
                ########################## Inicie aqui o codigo de extracao ##########################|

                # Exemplo

                # try:
                #     button = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#menu4')))
                #     driver.execute_script('arguments[0].click();', button)
                #     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#listaMenu4 > li:nth-child(2) > a:nth-child(1)'))).click()
                # except TimeoutException:
                #     WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#menu4'))).click()
                #     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#listaMenu4 > li:nth-child(2) > a:nth-child(1)'))).click()
                    
                

                # try:
                #     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtAutenticacaoSenhaFinanceira'))).send_keys(self.credentials['USER_AUTHENTICATION'])
                #     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button.btn:nth-child(2)'))).click()
                #     WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.swal2-confirm'))).click()
                # except TimeoutException:
                #     pass            
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).clear()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).click()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataInicial'))).send_keys(date_2.strftime("%d/%m/%Y"))
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).clear()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).click()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#txtDataFinal'))).send_keys(datetime.date.today().strftime("%d/%m/%Y"))
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado'))).click()

                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoDeData > option:nth-child(1)'))).click()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoDeData > option:nth-child(1)'))).click()

                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlStatusPagCliente > option:nth-child(3)'))).click()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlStatusPagCliente > option:nth-child(3)'))).click()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado > option:nth-child(1)'))).click()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#ddlTipoResultado > option:nth-child(1)'))).click()
                # WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btn'))).click()
                
                # try:
                #     allert = driver.switch_to.alert
                #     driver_alert = allert.text

                #     if driver_alert == 'NENHUM RESULTADO FOI ENCONTRADO.':
                #         allert.dismiss()
                #         # Salvando arquivo vazio

                # except NoAlertPresentException:
                #     pass
        
                ########################## Fim do codigo de extracao ##########################|



    def dowloadProductiion(self, date_work: datetime.date):

        '''

            Executa a classe self.__production() e faz a transferencia do download para a pasta download correta.

        '''

        path_to_save = f'../download/{date_work.year}/{date_work.month}/production/{date_work}.csv'
        
        # Realiza dowenload somente se o download não existir
        # if not path.exists(path_to_save):
        if True:
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
                ("Download do relatório de comissão crefisa", self.dowloadComission),
                #    ("Download do relatório de produção do crefisa", self.dowloadProductiion)
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


## estou testando o downladComission