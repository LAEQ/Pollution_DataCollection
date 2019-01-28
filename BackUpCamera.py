# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 06:36:35 2018

@author: gelbj
"""

import os
import win32api
from distutils.dir_util import copy_tree
import time, datetime

###############################################################################
## Parametres de lancement
###############################################################################

OutPutFolder = "C:/Users/GelbJ/Desktop/Projets/__Collecte reseau cyclable Montreal 05-2018/CollectedDatas/BackUpCamera"

#User = "ID1_SP"

User = "ID2_VJ"

#User = "ID3_MG"

#User = "ID4_DD"

###############################################################################
## Execution
###############################################################################

def MakeDate(Date) :
    if len(str(Date.day))==1 : 
        Day = "0"+str(Date.day)
    else : 
        Day = str(Date.day)
    if len(str(Date.month))==1 : 
        Month = "0"+str(Date.month)
    else : 
        Month = str(Date.month)
    return str(Date.year)+"-"+Month+"-"+Day

## Listing des disques connectes
Drives = win32api.GetLogicalDriveStrings()
Drives = Drives.split('\000')[:-1]

Find = False

for Disk in Drives :
    try :
        Folders = os.listdir(Disk)
        Readable = True
    except WindowsError :
        Readable = False
    if Readable :
        ## si on trouve une camera garmin !
        if "Garmin" in Folders and "GMetrix" in Folders :
            Videos = os.listdir(Disk+"DCIM/100_VIRB")
            for element in Videos :
                if element.split(".")[-1]=="MP4" :
                    F1 = element
                    Time = os.path.getctime(Disk+"DCIM/100_VIRB/"+F1)
                    Date = datetime.datetime.strptime(time.ctime(Time),"%a %b %d %H:%M:%S %Y")
                    StrDate = MakeDate(Date)
                    FinalFolder = OutPutFolder+"/"+User+"_"+StrDate
                    if os.path.isdir(FinalFolder) == False : 
                        os.mkdir(FinalFolder)
                        print("Lancement de la copy ....")
                        Find = True
                        copy_tree(Disk,FinalFolder)
                        break
                    else : 
                        print("Folder already exists : "+FinalFolder+" !! avoiding delete data")

if Find == False :
    print("No camera found")
print("\a")