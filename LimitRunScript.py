#! /usr/bin/python                                                                                                                                                      

import os
import sys
import math
import ROOT
from Config import *

def get_parser():
    ''' Argument parser.                                                                                                                                                                                                                     
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--signal',           action='store',                     type=str,            default='1000_920',                                help="Which signal point?" )
    argParser.add_argument('--doScan',             action='store',                   type=bool,            default=False,                                             help="running over all signal points" )
    return argParser

options = get_parser().parse_args()

signal = options.signal
doScan = options.doScan

sname = '_T2tt_'+signal

if not doScan:
    txtline = []
    cardname = 'DataCard/CCDataCard'+sname+'.txt'
    txtline.append("combine -M AsymptoticLimits %s --name %s\n"%(cardname, sname))
    fsh = open("RunLimitScript.sh", "w")
    fsh.write(''.join(txtline))
    fsh.close()
    os.system('chmod 744 RunLimitScript.sh')
    print('......................')
    print('Running limit for signal point: ', sname)
    print('......................')
    os.system('./RunLimitScript.sh')

else:
    os.system('ls DataCard/CCDataCard*.txt > lsCard.txt')
    df = {}
    with open('lsCard.txt','r') as ifile:
        for line in ifile:
            line = line.rstrip()
            k = line.replace("DataCard/CCDataCard","")
            k = k.replace(".txt","")
            df[line]= k
    print('......................')
    for i, (k, v) in enumerate(df.items()):
        txtline = []
        txtline.append("combine -M AsymptoticLimits %s --name %s\n"%(k, v))
        fsh = open("RunLimitScript_%i.sh"%i, "w")
        fsh.write(''.join(txtline))
        fsh.close()
        os.system('chmod 744 RunLimitScript_%i.sh'%i)
        print('......................')
        print('Running limit for signal point: ',v)
        print('......................')
        os.system('./RunLimitScript_%i.sh'%i)
