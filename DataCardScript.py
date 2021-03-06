#! /usr/bin/python                                                                                                                                                      

import os
import sys
import math
import ROOT
from Config import *

SRbins = SRBins #make sure the bin number is consistent with the number of region histogram bins


for sig in signals:

    txtline = []
    txtline.append("echo 'Making datacards from the text files'\n")
    for b in range(SRBins):
        txtline.append("python MakeCard.py --bins %i --sig %s\n"%(b, sig))
    txtline.append("echo 'Making datacards completed'\n")
    fsh = open("MakeDataCardScript.sh", "w")
    fsh.write(''.join(txtline))
    fsh.close()
    os.system('chmod 744 MakeDataCardScript.sh')
    os.system('./MakeDataCardScript.sh')
    os.system('ls datacard_Bin*.txt > ls.txt')

    df = {}
    with open('ls.txt','r') as ifile:
        for line in ifile:
            line = line.rstrip()
            k = line.replace("datacard_Bin","")
            k = k.replace(".txt","")
            df[k]= line

    cardcomb = []
    for b in range(SRBins):
        lt = SRBinLabelList[b]+"="+df[SRBinLabelList[b]]
        cardcomb.append(lt)

    bsline = []
    bsline.append("echo 'combining datacards for signal %s'\n"%sig)
    bsline.append("combineCards.py "+" ".join(cardcomb)+" > CCDataCard_T2tt_"+sig+".txt\n")
    bsline.append("echo 'combining datacards completed'\n")
    bsline.append("rm datacard_Bin*.txt\n")
    bsline.append("echo 'moving combined datacards to DataCard dir'\n")
    bsline.append("mv CCDataCard_T2tt_*.txt DataCard/\n")
    bsline.append("echo 'combine datacard process completed'\n")
    bsline.append("echo '.....................'\n")
    bsline.append("echo '.....................'\n")

    bsh = open("CombineDataCardScript.sh", "w")
    bsh.write(''.join(bsline))
    bsh.close()
    os.system('chmod 744 CombineDataCardScript.sh')
    os.system('./CombineDataCardScript.sh')
