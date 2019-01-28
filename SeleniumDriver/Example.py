# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 18:03:51 2017

@author: jeremy
"""

from selenium import webdriver
import time,os,shutil

###############################################################################
## Parametres
###############################################################################
User = 'Jere'
ID = "2_JG"
Month = "09"
Day = "05"
Date = Month+"/"+Day
Destination = "H:/LAEQ/Collecte Paris/Test/Data"

def WaitFile(File) :
    u=0
    while os.path.isfile(File)==False :
        u+=1
        time.sleep(2)
        if u>=10 :
            raise ValueError("Le fichier ne s'est pas telecharger")
    print("File detected")

###############################################################################
## Script
###############################################################################
driver = webdriver.Chrome(r'H:\Python\SeleniumDriver\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.maximize_window()

## ouverture de myhexoskin
driver.get('https://my.hexoskin.com/en/login')

##se connecter avec le compte de phillipe
Mail = driver.find_element_by_xpath('//*[@id="login_username"]')
Mail.send_keys('philippe.apparicio@ucs.inrs.ca')

Password = driver.find_element_by_xpath('//*[@id="password"]')
Password.send_keys("Mathis642")

Button =  driver.find_element_by_xpath('//*[@id="submit-button"]')
Button.click()

time.sleep(2)

##rentrer dans la page record
Button = driver.find_element_by_xpath('//*[@id="wrap"]/div[1]/div/div/div/ul[1]/li[4]/a')
Button.click()
time.sleep(2)

##delete potential filter
try :
    Button = driver.find_element_by_xpath('//*[@id="s2id_search_user_ids"]/ul/li[1]/a')
    Button.click()
    time.sleep(2)

except :
    pass

##acceder a l'utilisateur voulu
NameField = driver.find_element_by_xpath('//*[@id="s2id_autogen1"]')
NameField.send_keys(User)
Valid = driver.find_element_by_xpath('//*[@id="select2-drop"]/ul')
Valid.click()

Filter = driver.find_element_by_xpath('//*[@id="filter_search_button"]')
Filter.click()

time.sleep(2)
###boucle sur toutes les lignes
Rows = driver.find_elements_by_class_name('duration')
NB = len(Rows)

for e in range(NB) :
    Row = Rows[e]
    if Date in Row.text :
        if "PM" in Row.text :
            Moment = "PM"
        if "AM" in Row.text :
            Moment = "AM"
        Row.click()
        time.sleep(5)
        ##lecture du SVG
        SVG = driver.find_element_by_css_selector('#highcharts-0 > svg > g:nth-child(6)')
        SVG.click()
        time.sleep(1)
        ## telechargement des donnees
        CSV = driver.find_element_by_xpath('//*[@id="highcharts-0"]/div[2]/div/div[6]')
        driver.execute_script("$(arguments[0]).click();", CSV)
        time.sleep(2)
        ##enregistrement du fichier
        File = os.listdir('C:/Users/jeremy/Downloads')[0]
        OkName = File.replace(".crdownload","")
        WaitFile('C:/Users/jeremy/Downloads/'+OkName)
        shutil.copy2('C:/Users/jeremy/Downloads/'+OkName,Destination+'/ID'+ID+"/ID"+ID+"_2017_"+Month+"_"+Day+"_Hx_"+Moment+".csv")
        driver.back()
        time.sleep(2)
        Rows = driver.find_elements_by_class_name('duration')
        time.sleep(1)
        os.unlink('C:/Users/jeremy/Downloads/'+OkName)
        
        
        
        