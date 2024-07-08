from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import datetime
from os import makedirs, listdir
from shutil import move
from pathlib import Path
import time

# esta classe tem que herdar a openBrowe
def sendAction(action: str, driver= None, element= None, key= None):

        if action == 'send_keys':
            WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CSS_SELECTOR, element))).send_keys(key)
        if action == 'click':
            
            button = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CSS_SELECTOR, element)))
            driver.execute_script("arguments[0].click();", button)
        if action == 'waitCaptcha':
                input("Verifique se há reCaptcha a ser preenchido. Caso haja, preencha, e depois pression 'ENTER'.")
                respose = input("Você tem certeza que verificou o reCaptcha? [y/n]")
                if respose == 'y':
                        pass
                input("Verifique se há reCaptcha a ser preenchido. Caso haja, preencha, e depois pression 'ENTER'.")
                respose = input("Você tem certeza que verificou o reCaptcha? [y/n]")
                if respose == 'y':
                        pass
                else:
                        print("Fechando programa em 5s")
                        time.sleep(5)
                        quit()
                


def move_file(date: datetime.date, type_transference: list = ['comission', 'production', 'importation', 'extra']):

        path_download_tmp = f"./download_tmp/"
        type_transfer = type_transference[0]
        path_to_move = f'../download/{date.year}/{date.month}/{type_transfer}/'
        
        while len(listdir(path_download_tmp)) == 0:
                continue

        #Ajustar esta parte - para continuar somente se o download estiver concluido
        time.sleep(5)

        while any(file.endswith(".part") for file in listdir(path_download_tmp)):
               time.sleep(2)
               continue
        file = listdir(path_download_tmp)[0]
        move(path_download_tmp + file, path_to_move + f"{date}{Path(file).suffix}")

