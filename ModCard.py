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
    argParser.add_argument('--skipbin',           action='store',                     type=str,            default='False',         help="if bin skipping is on?" )
    return argParser

options = get_parser().parse_args()

fname = options.fname
skipbin = options.skipbin

skipbins = False
if 'True' in skipbin:
    from SkippingBinsList import ZsigSRbins, ZtBKSRbins
    skipbins = True


with open(fname,'a') as ofile:
    ofile.write('\n')
    for CRbin in CRSRMap:
        if BKmode == 'old':
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' WJets 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' ttbar 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' SingleTop 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' DY 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' VV 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' TTX 1\n')
        else:
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' WJets 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' ttbar 1\n')
            ofile.write(CRbin+'_norm_prompt rateParam '+CRbin+' OtherPrompt 1\n')
        for mbin in CRSRMap[CRbin]:
            if skipbins:
		if f"Bin{mbin}" in ZsigSRbins: continue
                if f"Bin{mbin}" in ZtBKSRbins: continue
            if BKmode == 'old':
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' WJets (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' ttbar (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' SingleTop (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' DY (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' VV (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' TTX (@0*1) '+CRbin+'_norm_prompt\n')
            else:
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' WJets (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' ttbar (@0*1) '+CRbin+'_norm_prompt\n')
                ofile.write(CRbin+'_norm_prompt rateParam '+mbin+' OtherPrompt (@0*1) '+CRbin+'_norm_prompt\n')
    ofile.write('\n')

    

