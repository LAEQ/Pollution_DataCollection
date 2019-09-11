# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 11:43:10 2019

@author: gelbj
"""


from path import Path
import win32api
import os
from datetime import datetime
from multiprocessing import Pool
import shutil
import utils
from utils.BruteMP import MPWorker
import random


Cores = 6

Root = Path(__file__).parent.parent.parent.joinpath("CollectedDatas").joinpath("BackupCamera")


######################################
## Fonctions utilitaires
######################################
def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def CompleteDirTree(Root1,Root2) : 
    """
    Permet de s'assurer que l'arborescence de 1 se retrouve bien dans 2
    et la complete au besoin
    Based on : https://stackoverflow.com/questions/40828450/how-to-copy-folder-structure-under-another-directory
    """
    Root1 = str(Root1).replace("\\","/")
    Root2 = str(Root2).replace("\\","/")
    for root, dirs, files in os.walk(Root1, topdown=False) : 
        for Folder in dirs :
            Folder = (root+"/"+Folder).replace("\\","/")
            Folder = Root2 +"/"+ Folder[len(Root1):len(Folder)]
            os.makedirs(Folder,exist_ok=True)


def IsCamera(Folder) :
    try :
        Children = [str(F.name) for F in Folder.dirs()]
        if "DCIM" in Children and "Garmin" in Children :
            return True
        else :
            return False
    except PermissionError :
        #NB : le peripherique n'est pas lisible
        return False

def Worker(Operations) :
    Commandes = []
    for Operation in Operations :
        Commande = "{0}  {1}  {2}".format("copy", r'"%s"' % Operation[0], r'"%s"' % Operation[1])
        Commandes.append(Commande)
    Comm = " & ".join(Commandes)
    os.system(Comm)



######################################
## execution
######################################

Start = datetime.now()

if __name__=="__main__" :
    #1 : trouver la date du jour
    Date = datetime.now().strftime("%Y-%m-%d")
    #2 : trouver les cameras concernees
    Drives = win32api.GetLogicalDriveStrings()
    Drives = Drives.split('\000')[:-1]
    Cameras = [Path(D) for D in Drives if IsCamera(Path(D))]

    #3 : iterer sur ces cameras et lancer les copies
    for Cam in Cameras :
        print("Working on this camera : "+str(Cam))
        IDPart,Cote = [str(F.name) for F in Cam.files("*.txt") if "ID" in str(F.name)][0].split(".")[0].split("-")
        Sortie = Root.joinpath("_".join([IDPart,Date,Cote]))
        print("    Building directories")
        CompleteDirTree(Cam,Sortie)
        #2 : identifier toutes les copies et les stockees
        Operations = []
        print("    Identifying operations")
        for File in Cam.walkfiles() :
            Copy = str(Sortie)+"\\"+(str(File).replace(str(Cam),""))
            print((str(File),Copy))
            Operations.append((str(File),Copy))
        random.shuffle(Operations)
        print("    Starting copies")
        #3 : lancer les operations en mode multiprocessing
        Sequences = chunkIt(Operations,Cores)
        pool = MPWorker(Root)
        for Seq in Sequences :
            pool.AddJob(Worker,Seq)
        pool.Libs = ["os"]
        pool.PrepareJobs()
        #pool.TestJob(1,MaxWait=60)
        pool.RunJobs()



        #pool = Pool(Cores)
        #pool.map(Worker,Operations)

        #4 : faire une verification
        OriginalFiles = set([str(F.name) for F in Cam.walkfiles()])
        CopiedFiles = set([str(F.name) for F in Sortie.walkfiles()])
        Differences = OriginalFiles.difference(CopiedFiles)
        if len(Differences)==0 :
            print("    The copy was well done for this camera : "+str(Cam))
            #5 : cleaning because everuthing was alright !
            DCIM = Cam.joinpath("DCIM")
            print("    ...cleaning DCIM")
            for File in DCIM.walkfiles() :
                os.remove(File)
            print("    ...cleaning Gmetrix")
            GMetrix = Cam.joinpath("GMetrix")
            for File in GMetrix.walkfiles() :
                os.remove(File)
            print("Done")
        else :
            print("    Errors occured during the copy for camera "+str(Cam)+"... you should check it, the files were not cleaned")


pool.CleanMe()

End = datetime.now()

Ellapsed = (End-Start).total_seconds()

Rest = Ellapsed % 60
DurationMin = round((Ellapsed-Rest)/60)

print("Total duration of the copy : {0} min and {1} seconds".format(DurationMin,Rest))


