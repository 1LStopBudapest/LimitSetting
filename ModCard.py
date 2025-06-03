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
        if BKmode == 'old':
            ofile.write(CRbin+'_norm_a rateParam '+CRbin+' WJets 1\n')
            ofile.write(CRbin+'_norm_a rateParam '+CRbin+' ttbar 1\n')
            ofile.write(CRbin+'_norm_a rateParam '+CRbin+' SingleTop 1\n')
            ofile.write(CRbin+'_norm_a rateParam '+CRbin+' DY 1\n')
            ofile.write(CRbin+'_norm_a rateParam '+CRbin+' VV 1\n')
            ofile.write(CRbin+'_norm_a rateParam '+CRbin+' TTX 1\n')
        else:
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' WJets 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' ttbar 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' OtherPrompt 1\n')
        for mbin in CRSRMap[CRbin]:
            if BKmode == 'old':
                ofile.write(CRbin+'_norm_a rateParam '+mbin+' WJets (@0*1) '+CRbin+'_norm_a\n')
                ofile.write(CRbin+'_norm_a rateParam '+mbin+' ttbar (@0*1) '+CRbin+'_norm_a\n')
                ofile.write(CRbin+'_norm_a rateParam '+mbin+' SingleTop (@0*1) '+CRbin+'_norm_a\n')
                ofile.write(CRbin+'_norm_a rateParam '+mbin+' DY (@0*1) '+CRbin+'_norm_a\n')
                ofile.write(CRbin+'_norm_a rateParam '+mbin+' VV (@0*1) '+CRbin+'_norm_a\n')
                ofile.write(CRbin+'_norm_a rateParam '+mbin+' TTX (@0*1) '+CRbin+'_norm_a\n')
            else:
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' WJets (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' ttbar (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' OtherPrompt (@0*1) '+CRbin+'_norm_prompt\n')
    ofile.write('\n')
