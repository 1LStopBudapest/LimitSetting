#! /usr/bin/python                                                                                                                                                      

import os
import sys
import math
import ROOT

txtline = []
txtline.append("echo 'Making root file for SMS plot'\n")
txtline.append("python3 MakeSMSRootFile_dm.py\n")
txtline.append("mv limit_scan_T2tt.root PlotsSMS/\n")

fsh = open("SMSRootFileScript.sh", "w")
fsh.write(''.join(txtline))
fsh.close()
os.system('chmod 744 SMSRootFileScript.sh')
os.system('./SMSRootFileScript.sh')
os.system('rm SMSRootFileScript.sh')

