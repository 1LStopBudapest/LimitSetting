#! /usr/bin/python                                                                                                                                                      

import os
import sys
import math
import ROOT
import re

sys.path.append('../')
from Config import *

def get_parser():
    ''' Argument parser.                                                                                                                                                
    '''
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--cid',           action='store',                     type=str,            default='0',         help="condor job ID?"
 )
    return argParser

options = get_parser().parse_args()
condorId = options.cid

if condorId == '0':
    print('Use proper condor job ID with --cid option')
    sys.exit()

signals = Signals[Era]

msignals = [] #root files not produced from condor jobs
csignals = [] #corrupted root files produced from condor jobs

base_name = "higgsCombine_T2tt_{}.AsymptoticLimits.mH120.root"
base_out = "CombineFilesCondor."+condorId+".{}.out"

for i, suffix in enumerate(signals):
    old_filename = base_name.format(i)
    new_filename = f"higgsCombine_T2tt_{suffix}.AsymptoticLimits.mH120.root"
    out_file = base_out.format(i)
    
    if os.path.exists(old_filename):
        
        if not os.path.exists(out_file):
            print(f"Skipping: {out_file} not found (required for check)!")
            continue

        with open(out_file, 'r') as f_out:
            content = f_out.read()
            if 'Expected  2.5%: r <' in content:
                os.rename(old_filename, new_filename) #Do one dry run (with commenting out this line) before actual renaming
                os.system(f"mv {new_filename} ../")
                print(f"Renamed: {old_filename} -> {new_filename}")
            else:
                print(f"Corrupted file: {old_filename} as {out_file} does show fit error and not r value")
                csignals.append(suffix)

    else:
        print(f"Warning: {old_filename} not found!")
        msignals.append(suffix)

RerunSignals = msignals + csignals
if not len(RerunSignals): os.system('rm *.log *.err *.out *.root')

if len(RerunSignals):
    print("\n\nPlease run condor jobs again with the following signal points\n")
    print(RerunSignals)
    print("\n\nAdd the above signal list to the Config.py file and comment out the existing one for the condor job rerun\n")


#Printing remaining working signal point 
print(signals)
print(RerunSignals)
set2 = set(RerunSignals)
result = [item for item in signals if item not in set2]
print(result)

