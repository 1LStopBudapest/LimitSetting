#! /usr/bin/python                                                                                                                                                      

import os
import sys
import math
import ROOT
from Config import *


sigs = []
for sig in signals:
    sigs.append('T2tt_'+sig)

proccs = sigs + bkgs + data

txtline = []

for proc in proccs:
    txtline.append("python MakeTextFile.py --proc %s\n"%(proc))
   
fsh = open("MakeTextFileScript.sh", "w")
fsh.write(''.join(txtline))
fsh.close()
os.system('chmod 744 MakeTextFileScript.sh')
os.system('./MakeTextFileScript.sh')
