# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 19:25:39 2019

@author: gelbj
"""


import shutil
import os
from path import Path
import win32api
from datetime import datetime

#########################
## Parametres
#########################

Dates = ["2019-09-06","2019-09-05","2019-09-03","2019-09-09","2019-09-10"]


#########################
## Fonction utilitaires
#########################

def GetNiceDelta(Delta) :
    TotSeconds = Delta.total_seconds()
    Rest = TotSeconds % 3600
    Hour = int((TotSeconds-(Rest))/3600)
    Hour = str(Hour)
    if len (Hour) == 1 :
        Hour = "0"+Hour

    Rest2 = Rest % 60
    Min = int((Rest-(Rest2))/60)
    Min = str(Min)
    if len(Min)==1 :
        Min = "0"+Min

    Sec = str(int(Rest2))
    if len(Sec) == 1 :
        Sec = "0"+Sec

    return (":".join([Hour,Min,Sec]))



def GetCodStartEnd(File) :
    Datas = open(File,"r")
    Rows = Datas.readlines()
    StartValue = "NAN"
    EndValue = "NAN"
    # trouver la premier Row avec des valeurs
    for Row in Rows :
        if "," in Row :
            if Row.split(",")[1] != "\n" :
                Value = int(float(Row.split(",")[0]))
                StartDate = datetime.fromtimestamp(Value)
                StartValue = StartDate.strftime("%H:%M:%S")
                break
    Rows.reverse()
    for Row in Rows :
        if "," in Row :
            if Row.split(",")[1] != "\n" :
                Value = int(float(Row.split(",")[0]))
                EndDate = datetime.fromtimestamp(Value)
                EndValue = EndDate.strftime("%H:%M:%S")
                break
    Datas.close()
    Duree = GetNiceDelta((EndDate-StartDate))

    return (StartValue,EndValue,Duree)




#########################
## Execution
#########################

## Step1 : trouver le fichier d'ecriture
Root = Path(__file__).parent.parent.parent.joinpath("CollectedDatas")
DicoPart = {}


CODDates = []

for Folder in Root.dirs() :
    if "ID" in Folder.name :
        Num = Folder.name.split("_")[0].replace("ID","")
        DicoPart[Num] = Folder


## Step2 : trouver la clef codaxus
Drives = win32api.GetLogicalDriveStrings()
Drives = Drives.split('\000')[:-1]


for Disk in Drives :
    print(Disk)
    try :
        Clef = Path(Disk)
        Files = Clef.files("*.txt")
        Readable = True
        print("__ Readable")
    except WindowsError :
        Readable = False
        print("__Not Readable")
    if Readable :
        # lister les fichiers dans le dossier
        FileNames = [str(F.name) for F in Files]
        if '__ClefCodaxus__.txt' in FileNames :
            # si il s'agit bien d'une clef avec le fichier CODAXUS
            print("we have found the key !!")
            DataPath = Clef.joinpath("data")
            Files = DataPath.files("*.txt")
            for file in Files:
                # iterons sur les fichers presents dans la clef CODAXUS
                name = str(file.name)
                nameList = name.split("_")
                if nameList[0] in Dates:
                    # le ficheir correspond aux dates
                    Part = nameList[-1].split(".")[0].replace("RP","")
                    OutPutName = str(DicoPart[Part].name)+"_"+nameList[0]+"_"+nameList[1]+"_COD.txt"
                    Out = str(DicoPart[Part].joinpath(OutPutName))
                    shutil.copy2(file,Out)

                    #extraire le depart et la fin du fichier codaxus
                    StartTime,EndTime,Duree = GetCodStartEnd(file)
                    CODDates.append([OutPutName,StartTime,EndTime,Duree])


## step2 : ecrire les dates des ficheirs COD
Now = datetime.now()
DateNow = Now.strftime("%Y-%m-%d")
CodFile = open(Root.joinpath("ValidCOD_"+DateNow+".csv"),"w")

CodFile.write("FileName;StartTime;EndTime;Duree\n")

for Row in CODDates :
    CodFile.write(";".join(Row)+"\n")

CodFile.close()

