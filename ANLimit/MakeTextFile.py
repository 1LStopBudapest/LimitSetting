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
    argParser.add_argument('--proc',           action='store',                     type=str,            default='ttbar',         help="Which sample?" )

    return argParser

options = get_parser().parse_args()

proc = options.proc

isSignal = True if 'T2tt' in proc else False
isData = True if 'Data' in proc else False

if isSignal:
    for p in signals:
        rate = []
        stat = []
        Lumi = []
        PU = []
        JEC = []
        JER = []
        leptonSF = []
        nISR = []
        wPt = []
        BTag_l = []
        BTag_b = []
        if 'T2tt_'+p!= proc: continue
        f = ROOT.TFile.Open('File/RegionPlot_SR_T2tt_'+p+'.root')
        h = f.Get('h_reg_'+proc)
        for b in range(1, h.GetNbinsX() + 1):
            rate.append(h.GetBinContent(b))
            stat.append(h.GetBinError(b))
            Lumi.append(1.025)
            PU.append(1.01)
            JEC.append(1.01)
            JER.append(1.01)
            leptonSF.append(1.01)
            nISR.append(1.05)
            wPt.append(-1)
            BTag_l.append(1.001)
            BTag_b.append(1.00)
        oname = 'File/'+proc+'.txt'
        with open(oname,'w') as ofile:
            ofile.write('rate,'+','.join(list(str(r) for r in rate))+'\n')
            ofile.write('stat,'+','.join(list(str(r) for r in stat))+'\n')
            ofile.write('Lumi,'+','.join(list(str(r) for r in Lumi))+'\n')
            ofile.write('PU,'+','.join(list(str(r) for r in PU))+'\n')
            ofile.write('JEC,'+','.join(list(str(r) for r in JEC))+'\n')
            ofile.write('JER,'+','.join(list(str(r) for r in JER))+'\n')
            ofile.write('leptonSF,'+','.join(list(str(r) for r in leptonSF))+'\n')
            ofile.write('nISR,'+','.join(list(str(r) for r in nISR))+'\n')
            ofile.write('wPt,'+','.join(list(str(r) for r in wPt))+'\n')
            ofile.write('BTag_l,'+','.join(list(str(r) for r in BTag_l))+'\n')
            ofile.write('BTag_b,'+','.join(list(str(r) for r in BTag_b))+'\n')

elif isData:
    rate = []
    f = ROOT.TFile.Open('File/RegionPlot_SR_'+sname[proc]+'.root')
    h = f.Get('h_reg_'+sname[proc])
    for b in range(1, h.GetNbinsX() + 1):
        rate.append(h.GetBinContent(b))
    oname = 'File/'+proc+'.txt'
    with open(oname,'w') as ofile:
        ofile.write('rate,'+','.join(list(str(r) for r in rate))+'\n')
else:
    rate = []
    stat = []
    Lumi = []
    PU = []
    JEC = []
    JER = []
    leptonSF = []
    nISR = []
    wPt = []
    BTag_l = []
    BTag_b = []
    f = ROOT.TFile.Open('File/RegionPlot_SR_'+sname[proc]+'.root')
    h = f.Get('h_reg_'+sname[proc])
    for b in range(1, h.GetNbinsX() + 1):
        rate.append(h.GetBinContent(b))
        stat.append(h.GetBinError(b))
        Lumi.append(1.025)
        PU.append(1.01)
        JEC.append(1.01)
        JER.append(1.01)
        leptonSF.append(1.01)
        nISR.append(1.002 if 'ttbar' in proc else -1)
        wPt.append(1.05 if 'WJet' in proc else -1)
        BTag_l.append(1.001)
        BTag_b.append(1.00)
    oname = 'File/'+proc+'.txt'
    with open(oname,'w') as ofile:
        ofile.write('rate,'+','.join(list(str(r) for r in rate))+'\n')
        ofile.write('stat,'+','.join(list(str(r) for r in stat))+'\n')
        ofile.write('Lumi,'+','.join(list(str(r) for r in Lumi))+'\n')
        ofile.write('PU,'+','.join(list(str(r) for r in PU))+'\n')
        ofile.write('JEC,'+','.join(list(str(r) for r in JEC))+'\n')
        ofile.write('JER,'+','.join(list(str(r) for r in JER))+'\n')
        ofile.write('leptonSF,'+','.join(list(str(r) for r in leptonSF))+'\n')
        ofile.write('nISR,'+','.join(list(str(r) for r in nISR))+'\n')
        ofile.write('wPt,'+','.join(list(str(r) for r in wPt))+'\n')
        ofile.write('BTag_l,'+','.join(list(str(r) for r in BTag_l))+'\n')
        ofile.write('BTag_b,'+','.join(list(str(r) for r in BTag_b))+'\n')
