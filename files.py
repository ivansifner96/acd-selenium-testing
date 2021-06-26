import pandas as pd
from login import *
element = []
userInputs = []
verification = []
fileElements = []
fileSize = []
fileErrors = []

def print_to_pandas(option):
    if(option == 1):
        raw_data = {
            'element' : element,
            'userInputs' : userInputs,
            'verification' : verification
        }

        df = pd.DataFrame(raw_data, columns = ['element', 'userInputs', 'verification'])
        df.to_csv(os.getcwd()+'\\Csv_output\\testselect.csv')
    else:
        raw_data = {
            'fileElements' : fileElements,
            'fileSize' : fileSize,
            'fileErrors': fileErrors
        }
        
        df = pd.DataFrame(raw_data, columns = ['fileElements', 'fileSize', 'fileErrors'])
        #########Csv path
        df.to_csv(os.getcwd()+'\\Csv_output\\testuploadfiles.csv')

def clickElement(element, attempts=5):
    counter = 0
    action = ActionChains(driver)
    while(counter < attempts):
        time.sleep(1)
        try:                       
            action.move_to_element(element).click().perform()
            print("you can click me")
            verification.append("No errors")
            break
        except:
            counter += 1
            print("element is not clickable right now")
            if(counter == attempts):
                verification.append("Error")

def find_selectControllers(record):
    time.sleep(2)
    element = findElementsXpath("//div[@class = ' css-1uc0gfp-control']")[record]
    return element

def traverse_select():
    time.sleep(2)
    #####Claim po zelji za koji zelite testirati select i upload funkcionalnosti
    driver.get("https://clarity-staging.acdcorp.com/adjuster/claims/detail/"
                +"773259ff-07b7-4589-b928-108fb3cab92b?type=files&queue="
                +"my-claims&pageOffset=0&pageSize=10")
    allSelects = checkPresenceOfAllElements("//div[@class = ' css-1uc0gfp-control']", 'xpath')
    for record in range(0, len(allSelects)):
        action = ActionChains(driver)
        time.sleep(1)
        fileName = findElementsXpath(
            "./parent::div/parent::div/following-sibling::div/a/span", allSelects[record])[0]
        action.move_to_element(allSelects[record]).click().perform()
        selectelement = WebDriverWait(driver,20, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_all_elements_located((
                By.XPATH,"//div[@class = ' css-26l3qy-menu']"+
                "//div[contains(@id, 'react-select')]")))
        selectLength = len(selectelement)
        print(selectLength)
        for reactSelect in range(0, selectLength):
            action = ActionChains(driver)
            selectElement = findElementsXpath("//div[@class = ' css-26l3qy-menu']"
                +"//div[contains(@id, 'react-select')]")[reactSelect]
            print(fileName.text)
            element.append(fileName.text + selectElement.text)
            userInputs.append('click')
            clickElement(selectElement)
            time.sleep(1)
            if(reactSelect == selectLength - 1):
                break
            allSelects[record].click()
        print(len(verification))
        print(len(userInputs))
        print(len(element))
    print_to_pandas(1)

def findErrors(fileList):
    global fileSize
    global fileElements
    global fileErrors
    listOfAll = checkVisibilityOfAllElements("//li[@class = 'filepond--item' "
        +"and contains(@data-filepond-item-state,'processing-complete')]//"
        +"div[@class = 'filepond--file-info']/span[1]", 'xpath')
    fileElements = [x.text for x in listOfAll]
    print(fileElements)
    fileSize = [findElementsXpath(
        "./following-sibling::span", x)[0].text for x in listOfAll]
    fileErrors = ["No errors"] * len(fileElements)
    difference = set(fileList).symmetric_difference(set(fileElements))
    listOfErrors = findElementsXpath("//li[@class = 'filepond--item'" 
        +"and contains(@data-filepond-item-state,'processing-error')]"
        +"//div[@class = 'filepond--file-info']/span[1]")
    if(len(listOfErrors)> 0):
        errorSize = [findElementsXpath("./following-sibling::span", x)[0].text 
            for x in listOfErrors]
        print(difference)
        filteredList = list(difference)
        errors = ["Error"] * len(errorSize)
        fileElements.extend(filteredList)
        fileSize.extend(errorSize)
        fileErrors.extend(errors)
        print("Test is almost finished")
        print(filteredList)
    print_to_pandas(2)


def upload():
    fileLista = []
    uploadBtn = checkPresenceOfElement(
        "//span[contains(text(), 'Upload')]/parent::button", 'xpath')
    time.sleep(2)
    uploadBtn.click()
    ############Test file path
    path = os.getcwd()+"\\TestFajlovi"
    dir = os.listdir(path)
    for file in dir:
        print(type(file))
        time.sleep(2)
        element = driver.find_element_by_class_name(
            'filepond--browser').send_keys(path+"/"+file)
        fileLista.append(file)
        time.sleep(2)
        while(len(findElementsXpath(
            "//li[@data-filepond-item-state= 'processing']")) > 0):
            print("waiting for the file to upload")
            time.sleep(2)
        startCatchingErrors()
        time.sleep(2)
    findErrors(fileLista)
    dumpToJson(os.getcwd()+'/Error_output/selectAndUpload', 'selectAndUpload.json')

site_login()
traverse_select()
upload()
driver.quit()