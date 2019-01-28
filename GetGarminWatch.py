
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 05 10:00:24 2018

@author: GelbJ
"""

import os
import win32api
import time, datetime
from shutil import copy2
from distutils.dir_util import copy_tree

##########################################################
## Parametres Principaux
##########################################################


#UserID = "1_VJ"
#Sortie = "J:/__Collecte Montreal 2018/CollectedDatas/ID1_VJ"

UserID = "2_MG"
Sortie = "J:/__Collecte Montreal 2018/CollectedDatas/ID2_MG"

#UserID = "3_DD"
#Sortie = "J:/__Collecte Montreal 2018/CollectedDatas/ID3_DD"

CleanWatch = True


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

def SetNumber(N) :
    if len(str(N))==1 :
        return "0"+str(N)
    else :
        return str(N)

##  Iteration sur ces disques
for Disk in Drives :
    print(Disk)
    try :
        Folders = os.listdir(Disk)
        Readable = True
        print("__ Readable")
    except WindowsError :
        Readable = False
        print("__Not Readable")
    if Readable :
        ## si on trouve une montre garmin !
        if "GARMIN" in Folders and "AUTORUN.INF" in Folders :
            ActivityFolder = Disk+"GARMIN/ACTIVITY"
            ## on trie ces fichiers par date
            FitFiles = [(File,os.path.getctime(ActivityFolder+"/"+File)) for File in os.listdir(ActivityFolder)]
            FitFiles.sort(key=lambda x : x[1])
            i=0
            ##on itere sur les fichiers FIT
            for File,Time in FitFiles :
                i+=1
                Date = datetime.datetime.strptime(time.ctime(Time),"%a %b %d %H:%M:%S %Y")
                OkDate = MakeDate(Date)
                NewName = "ID"+UserID+"_"+OkDate+"_TRAJET"+SetNumber(i)+".fit"
                if os.path.isfile(Sortie+"/"+NewName)==False :
                    copy2(ActivityFolder+"/"+File,Sortie+"/"+NewName)
                else : 
                    raise ValueError("The file seems to already exist !! avoid deleting")
                
            ## Si le nettoyage a ete demande
            if CleanWatch :
                try :
                    os.mkdir(Sortie+"/BackedWatch")
                except :
                    pass
                ## creation d'une sauvegarde (au cas ou)
                Today = datetime.datetime.strptime(time.ctime(),"%a %b %d %H:%M:%S %Y")
                Date = str(Today.day)+"-"+str(Today.month)+"-"+str(Today.year)
                os.mkdir(Sortie+"/BackedWatch/"+Date)
                copy_tree(Disk+"GARMIN/ACTIVITY",Sortie+"/BackedWatch/"+Date)
                for File,Time in FitFiles :
                    os.remove(ActivityFolder+"/"+File)
        
        
print("\a")