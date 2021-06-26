# acd-selenium-testing

There is a need for a little bit of configuration required for those scripts to work.

1. There is 5 scripts in total and each of them can be run by typing :
 python !scriptname!.py => eq. python claim_creation.py.
 Note that login script should not be run because it's solely purpose is
 to provide basic functions to other more important scripts.
 Scripts that you should run are : claim_creation.py, advanced_search.py,
 files.py, searchin_claims.py, 14functionalities.py
 
 2. You may have to change google chrome driver from the folder provided in this repo
 to match your current version of google chrome browser. You can just download
 google chrome driver version from this link https://chromedriver.chromium.org/downloads.
 
 3. If you want to see what is being tested you can proceed without "headless"
 mode. You should just comment those lines in login script like I've showed below.
 
 ![Screenshot_1](https://user-images.githubusercontent.com/54687506/123517059-7a9a2a80-d69f-11eb-965a-dd734430acab.png)
 
 4. The output of each test will be saved as csv for every test and errors in corresponding folder with json format too.
