from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from login import *
from datetime import datetime
import pandas as pd
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

GENERAL_ROOT = ("//div/span[contains(text(), 'General')]/parent::div"
            +"/parent::div//div[@class = 'form-control']")
VEHICLE_FILTER = ("//div/span[contains(text(), 'Vehicle filters')]/parent::div"
            +"/parent::div//div[@class = 'form-control']")
VEHICLE_FILTER_LOC = ("//div/span[contains(text(), 'Vehicle location filters')]"
            +"/parent::div/parent::div//div[@class = 'form-control']")
DATE_CREATED = ("//legend[contains(text(), 'Date created')]/parent::fieldset"
            +"//div[@class = 'form-control']")
DATE_COMPLETED = ("//legend[contains(text(), 'Date completed')]/parent::fieldset"
            +"//div[@class = 'form-control']")
DATE_BUTTON = ("//div[@class = 'css-g84q6c-dropdownClass']//"
            +"div[@class='datepicker-week']/button[not(contains(@class, 'day-disabled'))"
            +"and starts-with(@class, 'datepicker-day')]")
APPLY_BUTTON = "//button[contains(text(), 'Apply')]"
ERROR_CLASS = "//div[@class = 'css-1c6miek-bigAlertErrorClass']/div[2]"

general_dict = {}
vehicle_dict = {}
vehicleLoc_dict = {}
dateCreated_dict = {}
dateCompleted_dict = {}
listOfActions = []
inputValues = []
elementName = []
appErrors = ''

def clear_list():
    global inputValues
    global elementName
    global elementFoundStatus
    global appErrors
    inputValues.clear()
    elementName.clear()
    appErrors = ''

def print_to_pandas(fileName):
    global appErrors
    raw_data = {
        'elementName' : elementName,
        'inputValues' : inputValues,
        'elementFoundStatus' : elementFoundStatus,
    }
    startCatchingErrors()
    df = pd.DataFrame(raw_data, columns = ['elementName', 'inputValues', 
                                           'elementFoundStatus'])
    df.to_csv(os.getcwd()+'\\Csv_output\\'+appErrors+fileName+'')
    clear_list()
'''
######Testovi############Moguce drugacije definirati broj testova i vrstu inputa, 
selekta, date-a, ali ih ne zaboraviti dodati u funkciju test_dicts
'''

def checkTestStatus(claimsLength):
    if(appErrors == ''):
        return (claimsLength > 0 and 
        "claims_found_successfully" or 
        "no_claims_found"
        )
    return 'no_claims_found'

def test1():
    global elementFoundStatus
    args = {
        "From" : 1,
        "To" : 29
    }
    claimsLength = traverseAdvSrchElements(args)
    elementFoundStatus = checkTestStatus(claimsLength)
    print(elementFoundStatus)
    print_to_pandas(appErrors+elementFoundStatus+'advSearchtest1.csv')

def test2():
    global elementFoundStatus
    args = {
        "From" : 1,
        "To" : 29,
        "FROM" : 29,
        "TO"  : 1
    }
    claimsLength = traverseAdvSrchElements(args)
    elementFoundStatus = checkTestStatus(claimsLength)
    print(elementFoundStatus)
    print_to_pandas(appErrors+elementFoundStatus+'advSearchtest2.csv')

def test3():
    global elementFoundStatus
    args = {
        "Vehicle year" : "2010",
        "Claim number" : "00118310V2"
    }
    claimsLength = traverseAdvSrchElements(args)
    elementFoundStatus = checkTestStatus(claimsLength)
    print(elementFoundStatus)
    print_to_pandas(appErrors+elementFoundStatus+'advSearchtest3.csv')

def test4():
    global elementFoundStatus
    args = {
        "Vehicle year" : "20102010",
        "Claim number" : "00118310V2"
    }
    claimsLength = traverseAdvSrchElements(args)
    elementFoundStatus = checkTestStatus(claimsLength)
    print(elementFoundStatus)
    print_to_pandas(appErrors+elementFoundStatus+'advSearchtest4.csv')

def test5():
    global elementFoundStatus
    args = {
        "Vehicle year" : "201020102010",
        "Claim number" : "00118310V2"
    }
    claimsLength = traverseAdvSrchElements(args)
    elementFoundStatus = checkTestStatus(claimsLength)
    print(elementFoundStatus)
    print_to_pandas(appErrors+elementFoundStatus+'advSearchtest5.csv')


def test6():
    global elementFoundStatus
    args = {
        "Location type" : "Repair facility"
    }
    claimsLength = traverseAdvSrchElements(args)
    elementFoundStatus = checkTestStatus(claimsLength)
    print(elementFoundStatus)
    print_to_pandas(appErrors+elementFoundStatus+'advSearchtest6.csv')

def test7():
    global elementFoundStatus
    args = {
        "Claim status" : "New",
        "Owner type" : "Claimant"
    }
    claimsLength = traverseAdvSrchElements(args)
    elementFoundStatus = checkTestStatus(claimsLength)
    print(elementFoundStatus)
    print_to_pandas(appErrors+elementFoundStatus+'advSearchtest7.csv')

dates = ["From", "To", "FROM", "TO"]
selects = ["Claim status", "Estimate type", "Claim service type",
            "Owner type", "Adjuster", "Client auditor", "Appraiser type", 
            "Client appraiser", "Coverage type", "CAT claim",
            "Vehicle type", "Location type", "Location state"]

def find_elements(root):
    generalValues = checkPresenceOfAllElements(root, 'xpath')
    generalKeys = [x.text for x in findElementsXpath(root
    +"/preceding-sibling::span")]
    return generalKeys, generalValues

def checkElementType(str):
    if(str in dates):
        return "dateType"
    elif(str in selects):
        return "selectType"
    else:
        return "input"

def clear_fields(types, element, action):
    if(types == "dateType"):
        checkDate = findElementsXpath(".//input", element)[0]
        if(checkDate.get_attribute('value') != "__/__/____"):
            checkDate.click()
            checkDate.send_keys("a" + Keys.BACKSPACE)
            checkDate.click()
    elif(types == "input"):
        inputType = findElementsXpath(".//input", element)[0]
        if(inputType.get_attribute('value') != ""):
            print("you need to clear" + inputType.get_attribute('value'))
            inputType.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
    elif(types == "selectType"):
        print("you need to clear the field")
        checkClear = findElementsXpath(
            ".//div[contains(@class, 'form-select__clear-indicator')]",
            element)
        if(len(checkClear) > 0):
            checkClear[0].click()
            action.move_to_element(element).click().perform()

def populateDates(record,action,args):
    global inputValues
    global elementName
    today = datetime.today()
    time.sleep(2)
    checkDate = findElementsXpath(".//input", record[1])[0]
    action.move_to_element(record[1]).click().perform()
    datem = str(datetime(today.year, today.month, (args[record[0]]+1)))
    date = checkPresenceOfAllElements(DATE_BUTTON,'xpath')
    index = args[record[0]]
    date = date[index].click()
    inputValues.append(datem[0:10])
    print(datem[0:10])
    elementName.append(record[0])

def populateSelectElements(record, action,args):
    global inputValues
    global elementName
    action.move_to_element(record[1]).click().perform()
    selects = checkElementToBeClickable(
        "//div[contains(text(),'"+args[record[0]]+"')]", 'xpath').click()
    time.sleep(2)
    inputValues.append(args[record[0]])
    elementName.append(record[0])

def populateInputFields(record,action,args):
    global inputValues
    global elementName
    inputType = findElementsXpath("./input", record[1])[0]
    print(args[record[0]])
    if(inputType.get_attribute('value') != ""):
        inputType.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
    print("u have to go here")
    inputType.send_keys(args[record[0]])
    inputValues.append(args[record[0]])
    elementName.append(record[0])

def checkAllDictElements(element, args):
    for record in element.items():
        print("element is"+ record[0])
        action = ActionChains(driver)
        types = checkElementType(record[0])
        if(record[0] in args.keys()):
            if(types == "dateType"):
                populateDates(record, action,args)
            elif(types == "selectType"):        
                populateSelectElements(record, action,args)
            else:
                populateInputFields(record,action,args)
        else:
            if(types == "dateType"):
                clear_fields(types, record[1], action)
            elif(types == "input"):
                clear_fields(types, record[1], action)
            elif(types == "selectType"):
                clear_fields(types, record[1], action)

def traverseAdvSrchElements(args):
    global appErrors
    action = ActionChains(driver)
    time.sleep(1)
    for element in listOfActions:        
        checkAllDictElements(element,args)
    time.sleep(2)
    applyButton = checkElementToBeClickable(APPLY_BUTTON,"xpath")
    action.move_to_element(applyButton).click().perform()
    time.sleep(6)
    claims = findElementsXpath("//div[@class = 'claims-scroll']//a")
    if(len(findElementsXpath(ERROR_CLASS)) > 0):
        print("There is an error in the app")
        appErrors = 'testFailed'
    return len(claims)              
    
def test_dicts(x):
    return {
        '1': test1(),
        '2': test2(),
        '3': test3(),
        '4': test4(),
        "5": test5(),
        '6': test6(),
        '7': test7()
    }.get(x, 1)    # 1 is default if x not 

def find_searchClaims():
    action = ActionChains(driver)
    time.sleep(2)
    print('function call')
    searchContainer = checkPresenceOfElement("css-15oyjs9-container", "class")
    searchBar = searchContainer.find_element_by_class_name('css-1fjg8gh-control')
    action.reset_actions()
    action.move_to_element(searchBar).click().send_keys('test').perform()
    return searchBar

def testAdvancedSearch():
    searchBar = find_searchClaims()
    time.sleep(3)
    advancedSearch = WebDriverWait(driver,20).until(EC.element_to_be_clickable(
        (By.LINK_TEXT,"Advanced search"))).click()
    putInDict()
    time.sleep(2)
    test_dicts(str(1))
    dumpToJson(os.getcwd()+'/Error_output/advancedSearch', 'advancedSearch.json')

def putInDict():
    global general_dict
    global dateCreated_dict
    global dateCompleted_dict
    global vehicle_dict
    global vehicleLoc_dict
    global listOfActions
    dateCrKeys, dateCrValues = find_elements(DATE_CREATED)
    dateCoKeys, dateCoValues = find_elements(DATE_COMPLETED)
    generalKeys, generalValues = find_elements(GENERAL_ROOT)
    vehicleKeys, vehicleValues = find_elements(VEHICLE_FILTER)
    vehicleLocKeys, vehicleLosValues = find_elements(VEHICLE_FILTER_LOC)
    dateCreated_dict = dict(zip(dateCrKeys, dateCrValues))
    dateCompleted_dict = dict(zip(dateCoKeys, dateCoValues))
    dateCompleted_dict['FROM'] = dateCompleted_dict['From']
    del dateCompleted_dict['From']
    dateCompleted_dict['TO'] = dateCompleted_dict['To']
    del dateCompleted_dict['To']
    general_dict = dict(zip(generalKeys, generalValues))
    vehicle_dict = dict(zip(vehicleKeys, vehicleValues))
    vehicleLoc_dict = dict(zip(vehicleLocKeys, vehicleLosValues))
    listOfActions.append(dateCreated_dict)
    listOfActions.append(dateCompleted_dict)
    listOfActions.append(general_dict)
    listOfActions.append(vehicle_dict)
    listOfActions.append(vehicleLoc_dict)

site_login()
testAdvancedSearch()
driver.quit()