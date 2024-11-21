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
    argParser.add_argument('--fname',           action='store',                     type=str,            default='cname.txt',         help="Which sample?" )

    return argParser

options = get_parser().parse_args()

fname = options.fname




with open(fname,'a') as ofile:
    ofile.write('\n')
    for CRbin in CRSRMap:
        ofile.write(CRbin+'_norm_WJetsAndTop rateParam '+CRbin+' WJets 1\n')
        ofile.write(CRbin+'_norm_WJetsAndTop rateParam '+CRbin+' ttbar 1\n')
        ofile.write(CRbin+'_norm_WJetsAndTop rateParam '+CRbin+' SingleTop 1\n')
        for mbin in CRSRMap[CRbin]:
            ofile.write(CRbin+'_norm_WJetsAndTop rateParam '+mbin+' WJets (@0*1) '+CRbin+'_norm_WJetsAndTop\n')
            ofile.write(CRbin+'_norm_WJetsAndTop rateParam '+mbin+' ttbar (@0*1) '+CRbin+'_norm_WJetsAndTop\n')
            ofile.write(CRbin+'_norm_WJetsAndTop rateParam '+mbin+' SingleTop (@0*1) '+CRbin+'_norm_WJetsAndTop\n')
    ofile.write('\n')
