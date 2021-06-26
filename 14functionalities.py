from login import *
import pandas as pd
failErrors = []
claimNames = []

def print_to_csv():
    raw_data = {
        'claimNames' : claimNames,
        'failErrors' : failErrors,
    }

    df = pd.DataFrame(raw_data, columns = ['claimNames', 'failErrors'])
    ###################Csv path
    df.to_csv(os.getcwd()+'\\Csv_output\\claimSummaries.csv')

def findClaimSummary(claims):
    global failErrors
    for claim in claims:
        action = ActionChains(driver)
        driver.get(claim)
        summary = checkElementToBeClickable("//div/a[contains(text(), 'Summary')]", 'xpath')
        action.move_to_element(summary).click().perform()
        try:
            time.sleep(1)
            ispis = driver.find_element_by_xpath("//div[@class = 'caption']")
            if("Oops" in ispis.text):
                failErrors.append('Error in application')
            else:
                failErrors.append(ispis.text)
            print(ispis.text)
        except:
            failErrors.append('Summary is fullfilled')
        startCatchingErrors()

def traverse_elements():
    time.sleep(2)
    links = [x.get_attribute('href') 
        for x in findElementsXpath("//div[@class = 'css-ll4s95 nav-menu']//a")]
    global claimNames
    counter = 0
    for link in links:
        time.sleep(1)
        print(link)
        driver.get(link)
        time.sleep(2)
        claims = findElementsXpath("//div[@class = 'claims-scroll']//a")
        claims = [x.get_attribute('href') for x in claims]
        findClaimSummary(claims)
        claimNames.extend(claims)
    print_to_csv()
    dumpToJson(os.getcwd()+'/Error_output/14functionalities', '14functionalities.json')

site_login()
traverse_elements()
driver.quit()