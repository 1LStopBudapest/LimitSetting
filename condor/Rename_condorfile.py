#! /usr/bin/python                                                                                                                                                      

import os
import sys
import math
import ROOT
import re

sys.path.append('../')
from Config import *

signals = Signals[Era]

base_name = "higgsCombine_T2tt_{}.AsymptoticLimits.mH120.root"

for i, suffix in enumerate(signals):
    old_filename = base_name.format(i)
    new_filename = f"higgsCombine_T2tt_{suffix}.AsymptoticLimits.mH120.root"
    
    if os.path.exists(old_filename):
        os.rename(old_filename, new_filename) #Do one dry run (with commenting out this line) before actual renaming
        os.system(f"mv {new_filename} ../")
        print(f"Renamed: {old_filename} -> {new_filename}")
        
    else:
        print(f"Warning: {old_filename} not found!")

