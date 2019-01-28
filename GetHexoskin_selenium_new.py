# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 18:03:51 2017

@author: jeremy
"""

from selenium import webdriver
import time,os,shutil
from path import Path
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

###############################################################################
## Parametres
###############################################################################
File = Path(__file__)
Root = File.parent.parent.parent.joinpath("A)_FieldData")

User = 'Jerem'
ID = "3_JG"
Dates = ["2018/02/26","2018/02/27","2018/02/28","2018/03/01"] #Annee-Mois-Jour
#Destination = str(Root).replace("\\","/")+"/ID"+ID
Destination="C:/Users/gelbj/OneDrive/Bureau/TEMP"
#DriverPath = str(File.parent.joinpath("SeleniumDriver").joinpath("chromedriver_new.exe")).replace("\\","/")
DriverPath = str(File.parent.joinpath("SeleniumDriver").joinpath("geckodriver.exe")).replace("\\","/")

DownloadPath = 'C:/Users/gelbj/Downloads/'

#Decalage = 6*60 # a specifier en minutes

###############################################################################
## Fonction utilitaire
###############################################################################

def WaitFile(File) :
    u=0
    while os.path.isfile(File)==False :
        u+=1
        time.sleep(2)
        if u>=10 :
            raise ValueError("Le fichier ne s'est pas telecharge")
    print("File detected")
    
def GetFileName(File,i=0) : 
    if os.path.isfile(File) == False : 
        return File
    else : 
        P1,P2 = File.split("_HX")
        if i>0 : 
            P1 = P1.replace("_"+str(i),"")
        return GetFileName(P1+"_"+(str(i+1))+"_HX"+P2,i=i+1)
    
###############################################################################
## Script
###############################################################################

DownloadFolder = Path(DownloadPath)
    
## Nettoyage des dates
Months = []
for Date in Dates : 
    Comb = Date.split("/")
    D = str(Comb[1])+"_"+str(Comb[0])
    if D not in Months : 
        Months.append(D)
    
    

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
## demarage de la page web
binary = FirefoxBinary(r"C:\Program Files\Mozilla Firefox\firefox.exe")
driver = webdriver.Firefox(executable_path=DriverPath,firefox_profile=profile)
driver.maximize_window()

## ouverture de myhexoskin
driver.get('https://my.hexoskin.com/en/login')
Mail = driver.find_element_by_xpath('//*[@id="id_username"]')
Mail.send_keys('philippe.apparicio@ucs.inrs.ca')

Password = driver.find_element_by_xpath('//*[@id="id_password"]')
Password.send_keys("Mathis642")

Button =  driver.find_element_by_xpath('//*[@id="login-tab-content"]/form/button')
Button.click()

time.sleep(4)

##aller voir ses enregistrements
driver.get('https://my.hexoskin.com/records-table')

##retrouver le bon participant
Clear = driver.find_element_by_xpath('//*[@id="searchr"]/div[2]/div[1]/div/hx-select/div/div/div[2]')
Clear.click()
time.sleep(2)
Arrow = driver.find_element_by_xpath('//*[@id="searchr"]/div[2]/div[1]/div/hx-select/div/div/div[2]')
Arrow.click()
time.sleep(2)
List = driver.find_element_by_xpath('//*[@id="searchr"]/div[2]/div[1]/div/hx-select/select-dropdown/div/div[2]')
Rows = List.find_elements_by_tag_name("li")
for Row in Rows : 
    if User in Row.text : 
        Row.click()
        break
time.sleep(2)

##Iterer sur les row de la table
Table = driver.find_element_by_xpath('//*[@id="records"]/div[2]/div/table/tbody')
Rows = Table.find_elements_by_tag_name("tr")

for Row in Rows : 
    for Date in Dates : 
        if Date in Row.text :
            TDS = Row.find_elements_by_tag_name("td")
            LastTd = TDS[-1]
            Divs = LastTd.find_elements_by_tag_name("div")
            Div1 = Divs[1]
            ButtonList = Div1.find_element_by_tag_name('ul')
            Links = ButtonList.find_elements_by_tag_name('a')
            Link=Links[0]
            driver.execute_script("arguments[0].click();", Link)
            time.sleep(10)
            File = DownloadFolder.files("*.csv")[0]
            OkName = File.replace(".crdownload","")
            WaitFile(OkName)
            FileDate = Date.replace("/","-")
            OutPutFile = Destination+'/ID'+ID+"/ID"+ID+"_"+FileDate+"_HX.csv"
            if os.path.isfile(OutPutFile) : 
                OutPutFile = GetFileName(OutPutFile)
            shutil.copy2(OkName,OutPutFile)
            time.sleep(1)
            os.unlink(OkName)
            
driver.close()