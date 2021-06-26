from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException 

import json
import os
import time
import random
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

desired = DesiredCapabilities.CHROME
desired['goog:loggingPrefs'] = { 'performance':'ALL' }

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

ERRORS = 'errors'
errors = set()
##############Dodati vlastiti driver path
######Moja google chrome verzija 90.0.4430.212
######Moja google chrome driver verzija 89.0.4398.23
chromedriver= os.getcwd()+"\\ChromeDriver\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, 
                desired_capabilities=desired, chrome_options=chrome_options)

def site_login():
    driver.get_log('browser')
    driver.get("https://clarity-staging.acdcorp.com/")
    driver.find_element_by_name("username").send_keys("itadjuster")
    driver.find_element_by_name("password").send_keys("testing")
    driver.find_element_by_xpath('//input[@value="Log In"]').click()
    print("prolaz")

def log_filter(log_):
    return (
        # is an actual response
        log_["method"] == "Network.responseReceived"
        # and json
        and "json" in log_["params"]["response"]["mimeType"]
    )

def find_errors(requestList):
    global errors
    for x in requestList.values():
        try:
            if(type(x) == str and x.index(ERRORS) > 0):
                errors.add(x)
                print('Error has occured')
                print(errors)
        except ValueError:
            #print(x)
            print('ValueError: no errors found')

def startCatchingErrors():
    # extract requests from logs
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    for log in filter(log_filter, logs):
        request_id = log["params"]["requestId"]
        resp_url = log["params"]["response"]["url"]
        print(f"Caught {resp_url}")
        #print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))
        try:    
            requestList = driver.execute_cdp_cmd("Network.getResponseBody", 
                                            {"requestId": request_id})
            find_errors(requestList)
        except:
            print("nemos provjerit")

def dumpToJson(target_path, target_file):
    now = time.strftime("%Y, %m, %d, %H, %M, %S")
    target_file = now.replace(',', '-')+target_file
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(target_path, target_file), 'w') as f:
        json.dump(list(errors), f, indent = 4)

def driverWait():
    return WebDriverWait(driver,20, ignored_exceptions=ignored_exceptions)

def checkPresenceOfElement(selector, selectorType):
    if(selectorType == 'class'):
        return (driverWait().until(
        EC.presence_of_element_located((By.CLASS_NAME,selector)))
        )
    elif(selectorType== 'xpath'):
        return (driverWait().until(
        EC.presence_of_element_located((By.XPATH,selector)))
        )

def checkPresenceOfAllElements(selector, selectorType):
    if(selectorType == 'class'):
        return (driverWait().until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME,selector)))
        )
    elif(selectorType == "xpath"):
        return (driverWait().until(EC.presence_of_all_elements_located(
        (By.XPATH,selector)))
        )

def checkElementToBeClickable(selector, selectorType):
    if(selectorType == 'class'):
        return (driverWait().until(EC.element_to_be_clickable(
        (By.CLASS_NAME,selector)))
        )
    elif(selectorType == "xpath"):
        return (driverWait().until(EC.element_to_be_clickable(
        (By.XPATH,selector)))
        )

def checkVisibilityOfAllElements(selector, selectorType):
    if(selectorType == 'class'):
        return (driverWait().until(EC.visibility_of_all_elements_located(
        (By.CLASS_NAME,selector)))
        )
    elif(selectorType == "xpath"):
        return (driverWait().until(EC.visibility_of_all_elements_located(
        (By.XPATH,selector)))
        )

def findElementsXpath(xpath, element=''):
    print(element)
    ###find element nested inside other element
    if(isinstance(element, WebElement)):
        return element.find_elements_by_xpath(xpath)
    else:
        ###find all elements
        return driver.find_elements_by_xpath(xpath)

#site_login()
driver.maximize_window()
#driver.quit()

