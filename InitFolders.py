# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:15:00 2019

@author: GelbJ
"""

import os
from path import Path


Participants = ["ID1_JR","ID2_LN","ID3_MS","ID4_TA"]

ThisFile = Path(__file__)
Root = ThisFile.parent.parent.parent

os.mkdir(Root.joinpath("CollectedDatas"))
os.mkdir(Root.joinpath("CollectedDatas/BackupCamera"))

for Part in Participants : 
    os.mkdir(Root.joinpath("CollectedDatas/"+Part))


