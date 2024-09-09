# import send action
from sendActions import sendAction
import openBrowser
from selenium.common.exceptions import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
# classe para login
class login():

    def __init__(self, bank: str, credentials: dict):
        self.driver = openBrowser.openFirefox()._initializeDriver(bank = bank)
        self.credentials = credentials
        
    def send_keys(self, url: str, element_list: list, storm = False):
        self.driver.get(url)
        sendAction(driver = self.driver,
                        action='send_keys',
                        element= element_list[0], 
                        key = self.credentials['LOGIN_USER'] if not storm else self.credentials['LOGIN_USER_STORM'])
        
        sendAction(driver = self.driver,
                        action='send_keys',
                        element= element_list[1], 
                        key = self.credentials['LOGIN_PASSWORD'] if not storm else self.credentials['LOGIN_PASSWORD_STORM'])
        
        sendAction(action='waitCaptcha')
       
        try:
            sendAction(driver = self.driver,
                            action='click',
                            element= element_list[2])
        except TimeoutException:
            pass
       
        return self.driver    
