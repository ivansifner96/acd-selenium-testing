import pandas as pd
import re
from login import *

REQUIRED_FIELDS = ("//div[@class='form-control']/preceding-sibling::span"
                    +"/span/ancestor::div[@class='field-row input-row']")
REQUIRED_INPUT_FIELD = "/div[@class='form-control']/input"
REQUIRED_SELECT_FIELD = "/div[@class='form-control']/div[@class=' css-18gwgt1-container']"
REQUIRED_RB_FIELD = "//div[@class='css-nyf0j8-radioGroupClass']"
REQUIRED_TEXT_FIELD = "//textarea"
REQUIRED_DATE_FIELD = "//div[starts-with(@class, 'css-khfqss-dateTimeInputClass')]"
REQUIRED_PHONE_NUMBERS = ("//div[@class= 'field-row input-row']/"
                    +"span[contains(text(), 'phone')]/parent::div//input")
DATE_LABEL = "//div[@class = 'calendar-month']/div[@class = 'month-browser']/div"
DATE_BUTTON = ("//div[@class='datepicker-week']/button[not(contains(@class, 'day-disabled'))"
                    + "and starts-with(@class, 'datepicker-day')]")
ELEMENT_LABEL = "./parent::div/preceding-sibling::span"
numOfAttempts = 4

my_dict = { 
    "requiredDateField" : [],
    "requiredInputField": [] ,
    "requiredSelectField": [],
    "requiredTextField" : [],
    "requiredRbField" : []
} 

requiredField = []
userInputs = []
verification = []
counter = 0
error = False
checkOtherPhone = True

def clear_dict():
    for value in my_dict.values():
        del value[:]

def findElementsXpath(xpath, element=''):
    print(element)
    if(isinstance(element, WebElement)):
        return element.find_elements_by_xpath(xpath)
    else:
        return driver.find_elements_by_xpath(xpath)

def generateTestNames():
    num = 0
    lista = ['test1.csv', 'test2.csv', 
            'test3.csv', 'test4.csv']
    while(num < len(lista)):
        yield lista[num]
        num += 1

gen = generateTestNames()

def clear_lists():
    requiredField.clear()
    userInputs.clear()
    verification.clear()

def printToPandas():
    raw_data = {
        'requiredField' : requiredField,
        'userInputs' : userInputs,
        'verification' : verification
    }

    df = pd.DataFrame(raw_data, columns = ['requiredField', 'userInputs', 'verification'])
    nextTest = next(gen)
    print(nextTest)
    claimFail = driver.find_elements_by_xpath(
        "//div[contains(text(), 'Claim creation failed!')]")
    print("claimFailIznosi" + str(len(claimFail)))
    if(error == False and (len(claimFail) == 0)):
        nextTest = "test succeeded-" + nextTest
        print("nextTest is" + nextTest)
    df.to_csv(os.getcwd()+'\\Csv_output\\'+nextTest+'')
    time.sleep(2)
	
def find_allRequiredElements():
    reqInput = findElementsXpath(REQUIRED_FIELDS+REQUIRED_INPUT_FIELD)
    reqSelect = findElementsXpath(REQUIRED_FIELDS+REQUIRED_SELECT_FIELD)
    reqRB = findElementsXpath(REQUIRED_FIELDS+REQUIRED_RB_FIELD)
    reqText = findElementsXpath(REQUIRED_FIELDS+REQUIRED_TEXT_FIELD)
    reqDate = findElementsXpath(REQUIRED_FIELDS+REQUIRED_DATE_FIELD)
    my_dict['requiredDateField'].extend(reqDate)       
    my_dict['requiredInputField'].extend(reqInput)
    my_dict['requiredSelectField'].extend(reqSelect)
    my_dict['requiredTextField'].extend(reqText)
    my_dict['requiredRbField'].extend(reqRB)

def find_labels(radioButton):
    listaButtona = findElementsXpath("./label[@class='css-1kww9ww-radioButtonClass']", 
                                    radioButton)
    print(type(listaButtona))
    return listaButtona

def find_select_elements():
    requiredSelectField = "/div[@class='form-control']/div[@class=' css-18gwgt1-container']"
    parentReact = "//div[@class='form-select__menu-list css-1ljkvdv']"
    findString = REQUIRED_FIELDS+requiredSelectField+parentReact
    print(findString)
    selectRoot = WebDriverWait(driver,20).until(EC.element_to_be_clickable(
        (By.XPATH, findString)))
    selects = selectRoot.find_elements_by_xpath('./div')
    print(len(selects))
    selects = selects[random.randint(0, len(selects)-1)]
    return selects

def checkVerificationElements():
    verMessage = findElementsXpath("//div[@class='message validation-message']")
    for element in verMessage:
        verLabel = element.find_element_by_xpath('./parent::div/preceding-sibling::div/span')
        verification.append(element.text + '-' + verLabel.text)
    print("Verification length" + str(len(verification)))
    listDif = (len(userInputs)-len(verification))
    l = [None] * listDif
    verification.extend(l)
    print("verification length is" + str(len(verification)))	

def pickRandomDate():
    dateName = findElementsXpath(DATE_LABEL)[0]
    dateButtonXpath = DATE_BUTTON
    dateButtons = findElementsXpath(dateButtonXpath)
    date = dateButtons[random.randint(0, len(dateButtons) - 1)]
    userInputs.append(date.text + dateName.text)
    date.click()

def checkZipAndPhone(code):
    global counter
    ###perform last 2 tests
    if(counter > 0):
        if(code == 'Zip code*'):
            code = '99999'
        elif(code == 'Location phone*'):
            code = '9999999999'
        else:
            code = 'bbbbb'
    else:
        ### do a regular input
        code = 'bbbbb' 		
    userInputs.append(code)
    return code

def findOtherPhoneTypes():
    global counter
    otherRequiredPhoneType = findElementsXpath(REQUIRED_PHONE_NUMBERS)[:-1]
    randomSelection = random.randint(0,2)
    otherRequiredPhoneType = otherRequiredPhoneType[randomSelection]
    if(counter == 2):
        otherRequiredPhoneType.send_keys('999999999')
        userInputs.append('999999999')
    elif(counter > 2):
        otherRequiredPhoneType.send_keys('9999999999')
        userInputs.append('9999999999')
    phoneLabel = findElementsXpath(
        './parent::div/preceding-sibling::span',otherRequiredPhoneType)[0]
    requiredField.append(phoneLabel.text)

def populateRequiredDate(element):
    print(type(element))
    element.click()
    pickRandomDate()
    label = findElementsXpath(ELEMENT_LABEL, element)[0].text
    requiredField.append(label)
    print(label)

def populateRequiredInput(element):
    label = findElementsXpath(ELEMENT_LABEL, element)[0].text
    print(label)
    requiredField.append(label)
    element.send_keys(checkZipAndPhone(label))

def populateRequiredTextField(element):
    element.send_keys('testiranje_text_area')
    label = findElementsXpath(ELEMENT_LABEL, element)[0].text
    requiredField.append(label)
    userInputs.append('testiranje_text_area')
    print(label)

def populateRequiredSelectElements(element, actions):
    actions.move_to_element(element).click().perform()
    label = findElementsXpath(ELEMENT_LABEL, element)[0].text
    print(label)
    requiredField.append(label)
    selektovi = find_select_elements()
    userInputs.append(selektovi.text)
    selektovi.click()
    actions.reset_actions()

def populateRequiredRadioButton(element, actions):
    global checkOtherPhone
    label = findElementsXpath(ELEMENT_LABEL, element)[0].text
    print(label)
    userInputs.append('select_radio_button')
    requiredField.append(label)
    button = find_labels(element)
    actions.move_to_element(button[random.randint(0, len(button)-1)]).click().perform()
    if(counter >= 2 and checkOtherPhone == True):
        findOtherPhoneTypes()
        checkOtherPhone = False

def findNumOfCreatedClaims():
    driver.get("https://clarity-staging.acdcorp.com/adjuster/claims/all/my-recent-claims")
    numberOfClaimsElement = WebDriverWait(driver,20).until(
        EC.visibility_of_element_located((By.XPATH,"//span[@class = 'index-tracker']")))
    print(numberOfClaimsElement.text)
    return (int(re.findall('(?<=of)(.*)', numberOfClaimsElement.text)[0].replace(' ', '')))

def checkClaimStatus():
    global error
    global numOfCreatedClaims
    afterCreate = findNumOfCreatedClaims()
    if(afterCreate > numOfCreatedClaims):
        numOfCreatedClaims = afterCreate
        error = False
    else:
        error = True
  
def populateReqFields(dict_key, element):
    actions = ActionChains(driver)
    if(dict_key=='requiredDateField'):
        populateRequiredDate(element)
    elif(dict_key=='requiredInputField'):
        populateRequiredInput(element)
    elif(dict_key=='requiredTextField'):
        populateRequiredTextField(element)
    elif(dict_key=='requiredSelectField'):
        populateRequiredSelectElements(element, actions)
    else:
        populateRequiredRadioButton(element, actions)
        
def traverseDom():
    global counter
    global checkOtherPhone
    find_allRequiredElements()
    for i in my_dict.items():
        for a in i[1]:
            populateReqFields(i[0],a)	
    create = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, 
                                    "//button[contains(text(), 'Create')]"))).submit()
    time.sleep(6)
    startCatchingErrors()		
    counter += 1
    checkOtherPhone = True    
    checkVerificationElements()

def startTesting():
    global numOfCreatedClaims
    numOfCreatedClaims = findNumOfCreatedClaims()
    print("num of created claims iznosi"+ str(numOfCreatedClaims))
    time.sleep(2)
    findElementsXpath("//a[@title = 'Create a new claim']")[0].click()
    time.sleep(2)
    for i in range(0, numOfAttempts):
        time.sleep(2)
        traverseDom()
        clear_dict()
        driver.refresh()
        time.sleep(3)
        if(i < numOfAttempts):
            checkClaimStatus()
            time.sleep(2)
            driver.get("https://clarity-staging.acdcorp.com/adjuster/claims/create")
            print("Length userInputs" + str(len(userInputs)))
            print("Length required" + str(len(requiredField)))
            print("Length verification" + str(len(verification)))
            printToPandas()
            clear_lists()
    dumpToJson(os.getcwd()+'/Error_output/ClaimCreation', 'claimCreation.json')

site_login()
startTesting()
driver.quit()
