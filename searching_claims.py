from login import *
import pandas as pd

OTHER_RECIPENT = ("//div[@class = 'field-row input-row']/"
            +"span[contains(text(), 'Other recipients')]"
            +"/parent::div//input")
REQUIRED_NOTE_FIELD = ("//div[@class = 'field-row input-row']"
        +"//span[contains(@class, 'IndicatorClass')]"
        +"/parent::span/following-sibling::div/textarea")
ALL_NOTES = "//div[contains(@class, 'notes-table')]//div[@class = 'table-row content']"
ADD_NOTE = "//button[contains(text(), 'Add note')]"
###NAPOMENA####
'''
U find_searchClaims funkciji i start_testing funkciji mozete dodati
bilo koju rijec za testiranje searcha te napraviti test na njemu
Rijec koju ste dodali u find_searchClaims istu morate obavezno
dodati i u start_testing funkciju.
'''


'''
Razliciti testovi, moguce ih definirati na bilo koji nacin
i skripta ce za specificirani note dodati random jedan od testova,
potrebno svaki test dodati u varijablu testovi, pri tome 
argument To kada je 999 oznacava da ne postoji osoba za selekt, inace
ima redni testNum selekta tipa, 0, 3, 4 itd..Ako se doda preveliki testNum
skripta se ne rusi nego se odabire random selekt
'''
def test1():
    args = {
        "To" : 3,
        "Other_recipients" : "noviprimatelj@gmail.com",
        "Note" : "Automatic test note"
    }
    return args

def test2():
    args = {
        "To" : 999,
        "Other_recipients" : "",
        "Note" : ""
    }
    return args

def test3():
    args = {
        "To" : 0,
        "Other_recipients" : "noviprimatelj1@gmail.com, noviprimatelj2@gmail.com",
        "Note" : "Automatic test note"
    }
    return args

def test4():
    args = {
        "To" : 4,
        "Other_recipients" : "",
        "Note" : "Automatic test note"
    }
    return args

tests = {
    1 : test1,
    2 : test2,
    3 : test3,
    4 : test4
}

def odaberiRandomTest(arg):
    func = tests.get(arg, lambda : 'aaaaa')
    return func()

def printToPandas(failError, selectInput, inputNote, otherNote, claimList, testNum):
    raw_data = {
        'claimList' : claimList,
        'selectInput' : selectInput,
        'inputNote' : inputNote,
        'otherNote' : otherNote,
        'failError' : failError
    }

    print(str(len(claimList)))
    print(str(len(inputNote)))
    print(str(len(otherNote)))
    print(str(len(failError)))
    df = pd.DataFrame(raw_data, columns = ['claimList', 'selectInput', 
        'inputNote', 'otherNote', 'failError'])
    df.to_csv(os.getcwd()+'\\Csv_output\\'+testNum+'')
    time.sleep(2)

def findElementsXpath(xpath, element=''):
    print(element)
    ###find element nested inside other element
    if(isinstance(element, WebElement)):
        return element.find_elements_by_xpath(xpath)
    else:
        ###find all elements
        return driver.find_elements_by_xpath(xpath)

def checkIfSelectedElementSpecified(argumenti, selectInput):
    ####999 if select item is specified
    if(argumenti["To"] != 999):
        selektovi = findElementsXpath(
            "//div[@class = ' css-26l3qy-menu']//"
            +"div[starts-with(@id, 'react-select' )]")
        time.sleep(1)
        try:
            selekt = selektovi[argumenti["To"]]
            selectInput.append(findElementsXpath(
                ".//div[@class = 'recipient-option']", selekt)[0].text)
            selektovi[argumenti["To"]].click()
        except:
            index = random.randint(0,len(selektovi)-1)
            selekt = selektovi[index]
            selectInput.append(findElementsXpath(
                ".//div[@class = 'recipient-option']", selekt)[0].text)
            selektovi[index].click()
    else:
        selectInput.append('')

def find_searchClaims():
    action = ActionChains(driver)
    time.sleep(2)
    print('function call')
    searchContainer = checkPresenceOfElement("css-15oyjs9-container", "class")
    searchBar = searchContainer.find_element_by_class_name('css-1fjg8gh-control')
    action.reset_actions()
    action.move_to_element(searchBar).click().send_keys('test').perform()
    return searchBar

def start_testing():
    searchBar = find_searchClaims()
    options = [x.text for x in checkPresenceOfAllElements("//div[@class = ' css-1ljkvdv']"
    +"//div[starts-with(@id, 'react')]"
    +"//div[@class = 'claim-option-header']", "xpath")]
    constraint5 = len(options) >= 5 and 5 or len(options)
    options = random.sample(options, constraint5)
    time.sleep(2)
    action = ActionChains(driver)
    action.move_to_element(searchBar).click().send_keys('test').perform()
    driver.refresh()
    print(options)
    for i in range(0, constraint5):
        find_searchClaims()
        option = ("//div[starts-with(@id, 'react')]//div[@class = 'claim-option-header'" 
            +"and contains(text(), '"+options[i]+"')]")
        print(option)
        checkElementToBeClickable(option, "xpath").click()
        argumenti = odaberiRandomTest(random.randint(1,4))
        print(argumenti)
        add_note(options[i], i, argumenti)
        time.sleep(2)
        driver.refresh()
    dumpToJson(os.getcwd()+'/Error_output/searchingClaims', 'searchingClaims.json')

def successNotification(sviNoteovi):
    noviNoteovi = len(findElementsXpath(ALL_NOTES))
    if(noviNoteovi > sviNoteovi):
        print("You successfully added the note")
        return "You successfully added the note"
    else:
        print("Error in adding note")
        return "Error in adding notes"

def add_note(options, testNum, argumenti):
    failError = []
    selectInput = []
    claimList = []
    inputNote = []
    otherNote = []
    notedHeading = checkElementToBeClickable(
        "//div/a[contains(text(), 'Notes')]", "xpath").click()
    time.sleep(2)
    dodavanjeNota = findElementsXpath(
        "//span[contains(text(), 'Add note')]/parent::button")
    if(dodavanjeNota[0].is_enabled):
        dodavanjeNota[0].click()
        time.sleep(1)
        sviNoteovi = len(findElementsXpath(
            ALL_NOTES))
        rootSelect = checkElementToBeClickable("css-1uc0gfp-control", "class").click()
        time.sleep(1)
        checkIfSelectedElementSpecified(argumenti,selectInput)
        claimList.append(options)
        inputNote.append(argumenti['Note'])
        otherNote.append(argumenti['Other_recipients'])
        otherRecipient = findElementsXpath(
            OTHER_RECIPENT)[0].send_keys(argumenti["Other_recipients"])
        obavezniNoteField = findElementsXpath(REQUIRED_NOTE_FIELD)[0].send_keys(argumenti["Note"])
        dodavanjeNotaunotu = findElementsXpath(
            ADD_NOTE)[0].click()
        time.sleep(4)
        startCatchingErrors()
        failError.append(successNotification(sviNoteovi))
    else:
        print("note cannot be added")
        failError.append("Note is disabled")
    testNum = "searchin_claims"+str(testNum)+".csv"
    printToPandas(failError, selectInput, inputNote,otherNote, claimList, testNum)

site_login()
start_testing()
driver.quit()
