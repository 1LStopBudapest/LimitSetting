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
    argParser.add_argument('--year',           action='store',                     type=str,            default='2018',         help="Which year?" )
    return argParser

options = get_parser().parse_args()

proc = options.proc
year = options.year

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
        f = ROOT.TFile.Open('File/CountDCHist_SR+CR_T2tt_'+p+'.root')
        h = f.Get('h_rate_'+proc)
        hPU = f.Get('h_PU_'+proc)
        hPUu = f.Get('h_PUUp_'+proc)
        hPUd = f.Get('h_PUDown_'+proc)
        hLeptonSF = f.Get('h_LeptonSF_'+proc)
        hLeptonSFu = f.Get('h_LeptonSFUp_'+proc)
        hLeptonSFd = f.Get('h_LeptonSFDown_'+proc)
        hBTagSF = f.Get('h_BTagSF_'+proc)
        hBTagSFbu = f.Get('h_BTagSFbUp_'+proc)
        hBTagSFbd = f.Get('h_BTagSFbDown_'+proc)
        hBTagSFlu = f.Get('h_BTagSFlUp_'+proc)
        hBTagSFld = f.Get('h_BTagSFlDown_'+proc)
        hWPt = f.Get('h_WPt_'+proc)
        hWPtu = f.Get('h_WPtUp_'+proc)
        hWPtd = f.Get('h_WPtDown_'+proc)
        
        #for b in range(1, h.GetNbinsX() + 1):
        for b in range(1, 5 + 1):
            rate.append(h.GetBinContent(b))
            stat.append(h.GetBinError(b))
            Lumi.append(1.00 + LumiUnc[year])
            nISR.append(1.00 + ISRUnc)
            PU.append(1.00 + abs((hPUd.GetBinContent(b)-hPUu.GetBinContent(b))/(2 * hPU.GetBinContent(b))))
            leptonSF.append(1.00 + abs((hLeptonSFd.GetBinContent(b)-hLeptonSFu.GetBinContent(b))/(2 * hLeptonSF.GetBinContent(b))))
            BTag_b.append(1.00 + abs((hBTagSFbd.GetBinContent(b)-hBTagSFbu.GetBinContent(b))/(2 * hBTagSF.GetBinContent(b))))
            BTag_l.append(1.00 + abs((hBTagSFld.GetBinContent(b)-hBTagSFlu.GetBinContent(b))/(2 * hBTagSF.GetBinContent(b))))
            wPt.append(-1)
            JEC.append(1.01)
            JER.append(1.01)
        
        rate.append(h.GetBinContent(109))
        stat.append(h.GetBinError(109))
        Lumi.append(1.00 + LumiUnc[year])
        nISR.append(1.00 + ISRUnc)
        PU.append(1.00 + abs((hPUd.GetBinContent(109)-hPUu.GetBinContent(109))/(2 * hPU.GetBinContent(109))))
        leptonSF.append(1.00 + abs((hLeptonSFd.GetBinContent(109)-hLeptonSFu.GetBinContent(109))/(2 * hLeptonSF.GetBinContent(109))))
        BTag_b.append(1.00 + abs((hBTagSFbd.GetBinContent(109)-hBTagSFbu.GetBinContent(109))/(2 * hBTagSF.GetBinContent(109))))
        BTag_l.append(1.00 + abs((hBTagSFld.GetBinContent(109)-hBTagSFlu.GetBinContent(109))/(2 * hBTagSF.GetBinContent(109))))
        wPt.append(-1)
        JEC.append(1.01)
        JER.append(1.01)
        
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
    f = ROOT.TFile.Open('File/CountDCHist_SR+CR_'+sname[proc]+'.root')
    h = f.Get('h_rate_'+sname[proc])
    #for b in range(1, h.GetNbinsX() + 1):
    for b in range(1, 5 + 1):
        rate.append(h.GetBinContent(b))
    rate.append(h.GetBinContent(109))
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
    f = ROOT.TFile.Open('File/CountDCHist_SR+CR_'+sname[proc]+'.root')
    h = f.Get('h_rate_'+sname[proc])
    hPU = f.Get('h_PU_'+sname[proc])
    hPUu = f.Get('h_PUUp_'+sname[proc])
    hPUd = f.Get('h_PUDown_'+sname[proc])
    hLeptonSF = f.Get('h_LeptonSF_'+sname[proc])
    hLeptonSFu = f.Get('h_LeptonSFUp_'+sname[proc])
    hLeptonSFd = f.Get('h_LeptonSFDown_'+sname[proc])
    hBTagSF = f.Get('h_BTagSF_'+sname[proc])
    hBTagSFbu = f.Get('h_BTagSFbUp_'+sname[proc])
    hBTagSFbd = f.Get('h_BTagSFbDown_'+sname[proc])
    hBTagSFlu = f.Get('h_BTagSFlUp_'+sname[proc])
    hBTagSFld = f.Get('h_BTagSFlDown_'+sname[proc])
    hWPt = f.Get('h_WPt_'+sname[proc])
    hWPtu = f.Get('h_WPtUp_'+sname[proc])
    hWPtd = f.Get('h_WPtDown_'+sname[proc])
    #for b in range(1, h.GetNbinsX() + 1):
    for b in range(1, 5 + 1):
        rate.append(h.GetBinContent(b))
        stat.append(h.GetBinError(b))
        Lumi.append(1.00 + LumiUnc[year])
        nISR.append(1.00 + ISRUnc if 'ttbar' in proc else -1)
        PU.append(1.00 + abs((hPUd.GetBinContent(b)-hPUu.GetBinContent(b))/(2 * hPU.GetBinContent(b))) if hPU.GetBinContent(b)!=0 else -1)
        leptonSF.append(1.00 + abs((hLeptonSFd.GetBinContent(b)-hLeptonSFu.GetBinContent(b))/(2 * hLeptonSF.GetBinContent(b))) if hLeptonSF.GetBinContent(b)!=0 else -1)
        BTag_b.append(1.00 + abs((hBTagSFbd.GetBinContent(b)-hBTagSFbu.GetBinContent(b))/(2 * hBTagSF.GetBinContent(b))) if hBTagSF.GetBinContent(b)!=0 else -1)
        BTag_l.append(1.00 + abs((hBTagSFld.GetBinContent(b)-hBTagSFlu.GetBinContent(b))/(2 * hBTagSF.GetBinContent(b))) if hBTagSF.GetBinContent(b)!=0 else -1)
        wPt.append((1.00 + abs((hWPtd.GetBinContent(b)-hWPtu.GetBinContent(b))/(2 * hWPt.GetBinContent(b))) if hWPt.GetBinContent(b)!=0 else -1) if 'WJet' in proc else -1)
        JEC.append(1.01)
        JER.append(1.01)
            
    rate.append(h.GetBinContent(109))
    stat.append(h.GetBinError(109))
    Lumi.append(1.00 + LumiUnc[year])
    nISR.append(1.00 + ISRUnc if 'ttbar' in proc else -1)
    PU.append(1.00 + abs((hPUd.GetBinContent(109)-hPUu.GetBinContent(109))/(2 * hPU.GetBinContent(109))) if hPU.GetBinContent(109)!=0 else -1)
    leptonSF.append(1.00 + abs((hLeptonSFd.GetBinContent(109)-hLeptonSFu.GetBinContent(109))/(2 * hLeptonSF.GetBinContent(109))) if hLeptonSF.GetBinContent(109)!=0 else -1)
    BTag_b.append(1.00 + abs((hBTagSFbd.GetBinContent(109)-hBTagSFbu.GetBinContent(109))/(2 * hBTagSF.GetBinContent(109))) if hBTagSF.GetBinContent(109)!=0 else -1)
    BTag_l.append(1.00 + abs((hBTagSFld.GetBinContent(109)-hBTagSFlu.GetBinContent(109))/(2 * hBTagSF.GetBinContent(109))) if hBTagSF.GetBinContent(109)!=0 else -1)
    wPt.append((1.00 + abs((hWPtd.GetBinContent(109)-hWPtu.GetBinContent(109))/(2 * hWPt.GetBinContent(109))) if hWPt.GetBinContent(109)!=0 else -1) if 'WJet' in proc else -1)
    JEC.append(1.01)
    JER.append(1.01)
    
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
