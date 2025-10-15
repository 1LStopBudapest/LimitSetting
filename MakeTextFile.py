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

year = Era
signals = Signals[year]
if PromptNorm:
    bins = SRBins + CRbins
else:
    bins = SRBins

isSignal = True if 'T2tt' in proc else False
isData = True if 'Data' in proc else False

if isSignal:
    for p in signals:
        rate = []
        stat = []
        Lumi = []
        Lumi_cor = []
	Lumi_1718 = []
        PU = []
        JEC = []
        JER = []
        leptonSF = []
        nISR = []
        wPt = []
        BTag_l = []
        BTag_b = []
        BTag_l_cor = []
        BTag_b_cor = []
        L1prefire = []
        softbSF = []
        Xsec = []
        if 'T2tt_'+p!= proc: continue
        f = ROOT.TFile.Open('File/CountDCHist_SR_T2tt_'+p+'.root')
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
        hL1Prefire = f.Get('h_L1Prefire_'+proc)
        hL1Prefireu = f.Get('h_L1PrefireUp_'+proc)
        hL1Prefired = f.Get('h_L1PrefireDown_'+proc)
        hXsec = f.Get('h_XsecUp_'+proc)
        fjec = ROOT.TFile.Open('File/CountDCHistJEC_SR_T2tt_'+p+'.root')
        hNom = fjec.Get('h_rate_'+proc)
        hJECu = fjec.Get('h_JECUp_'+proc)
        hJECd = fjec.Get('h_JECDown_'+proc)
        hJERu = fjec.Get('h_JERUp_'+proc)
        hJERd = fjec.Get('h_JERDown_'+proc)
        for b in range(1, bins + 1):
            rate.append(h.GetBinContent(b))
            stat.append(h.GetBinError(b))
            Lumi.append(1.00 + LumiUnc[year])
            Lumi_cor.append(1.00 + CorLumiUnc[year])
            Lumi_1718.append(1.00 + Cor1718LumiUnc[year])
            nISR.append(1.00 + ISRUnc)
            PU.append(1.00 + abs((hPUd.GetBinContent(b)-hPUu.GetBinContent(b))/(2 * hPU.GetBinContent(b))) if hPU.GetBinContent(b)!=0 else -1)
            leptonSF.append(1.00 + abs((hLeptonSFd.GetBinContent(b)-hLeptonSFu.GetBinContent(b))/(2 * hLeptonSF.GetBinContent(b))) if hLeptonSF.GetBinContent(b)!=0 else -1)
            BTag_b.append(1.00 + abs((hBTagSFbd.GetBinContent(b)-hBTagSFbu.GetBinContent(b))/(2 * hBTagSF.GetBinContent(b))) if hBTagSF.GetBinContent(b)!=0 else -1)
            BTag_l.append(1.00 + abs((hBTagSFld.GetBinContent(b)-hBTagSFlu.GetBinContent(b))/(2 * hBTagSF.GetBinContent(b))) if hBTagSF.GetBinContent(b)!=0 else -1)
            BTag_l_cor.append(1.00)
            BTag_b_cor.append(1.00)
            wPt.append(-1)
            L1prefire.append(1.00 + abs((hL1Prefired.GetBinContent(b)-hL1Prefireu.GetBinContent(b))/(2 * hL1Prefire.GetBinContent(b))) if hL1Prefire.GetBinContent(b)!=0 else -1)
            softbSF.append(1.00)
            Xsec.append(hXsec.GetBinContent(b)/h.GetBinContent(b) if h.GetBinContent(b)!=0 else -1)
            JEC.append(1.00 + abs((hJECd.GetBinContent(b)-hJECu.GetBinContent(b))/(2 * hNom.GetBinContent(b))) if hNom.GetBinContent(b)!=0 else -1)
            JER.append(1.00 + abs((hJERd.GetBinContent(b)-hJERu.GetBinContent(b))/(2 * hNom.GetBinContent(b))) if hNom.GetBinContent(b)!=0 else -1)
        
                
        oname = 'File/'+proc+'.txt'
        with open(oname,'w') as ofile:
            ofile.write('rate,'+','.join(list(str(r) for r in rate))+'\n')
            ofile.write('stat,'+','.join(list(str(r) for r in stat))+'\n')
            ofile.write('Lumi,'+','.join(list(str(r) for r in Lumi))+'\n')
            ofile.write('LumiCor,'+','.join(list(str(r) for r in Lumi_cor))+'\n')
            ofile.write('LumiCor1718,'+','.join(list(str(r) for r in Lumi_1718))+'\n')
            ofile.write('PU,'+','.join(list(str(r) for r in PU))+'\n')
            ofile.write('JEC,'+','.join(list(str(r) for r in JEC))+'\n')
            ofile.write('JER,'+','.join(list(str(r) for r in JER))+'\n')
            ofile.write('leptonSF,'+','.join(list(str(r) for r in leptonSF))+'\n')
            ofile.write('nISR,'+','.join(list(str(r) for r in nISR))+'\n')
            ofile.write('wPt,'+','.join(list(str(r) for r in wPt))+'\n')
            ofile.write('BTag_l,'+','.join(list(str(r) for r in BTag_l))+'\n')
            ofile.write('BTag_b,'+','.join(list(str(r) for r in BTag_b))+'\n')
            ofile.write('BTag_l_cor,'+','.join(list(str(r) for r in BTag_l_cor))+'\n')
            ofile.write('BTag_b_cor,'+','.join(list(str(r) for r in BTag_b_cor))+'\n')
            ofile.write('L1prefire,'+','.join(list(str(r) for r in L1prefire))+'\n')
            ofile.write('softbSF,'+','.join(list(str(r) for r in softbSF))+'\n')
            ofile.write('Xsec,'+','.join(list(str(r) for r in Xsec))+'\n')

elif isData:
    rate = []
    f = ROOT.TFile.Open('File/CountDCHist_SR_'+sname[proc]+'.root')
    h = f.Get('h_rate_'+sname[proc])
    for b in range(1, bins + 1):
        rate.append(h.GetBinContent(b))
    
    oname = 'File/'+proc+'.txt'
    with open(oname,'w') as ofile:
        ofile.write('rate,'+','.join(list(str(r) for r in rate))+'\n')
else:
    rate = []
    stat = []
    Lumi = []
    Lumi_cor = []
    Lumi_1718 = []
    PU = []
    JEC = []
    JER = []
    leptonSF = []
    nISR = []
    wPt = []
    BTag_l = []
    BTag_b = []
    BTag_l_cor = []
    BTag_b_cor = []
    L1prefire = []
    softbSF = []
    Xsec = []
    f = ROOT.TFile.Open('File/CountDCHist_SR_'+sname[proc]+'.root')
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
    hL1Prefire = f.Get('h_L1Prefire_'+sname[proc])
    hL1Prefireu = f.Get('h_L1PrefireUp_'+sname[proc])
    hL1Prefired = f.Get('h_L1PrefireDown_'+sname[proc])
    hXsec = f.Get('h_XsecUp_'+sname[proc])
    fjec = ROOT.TFile.Open('File/CountDCHistJEC_SR_'+sname[proc]+'.root')
    hNom = fjec.Get('h_rate_'+sname[proc])
    hJECu = fjec.Get('h_JECUp_'+sname[proc])
    hJECd = fjec.Get('h_JECDown_'+sname[proc])
    hJERu = fjec.Get('h_JERUp_'+sname[proc])
    hJERd = fjec.Get('h_JERDown_'+sname[proc])
    for b in range(1, bins + 1):
        rate.append(h.GetBinContent(b))
        stat.append(h.GetBinError(b))
        Lumi.append(1.00 + LumiUnc[year])
        Lumi_cor.append(1.00 + CorLumiUnc[year])
        Lumi_1718.append(1.00 + Cor1718LumiUnc[year])
        nISR.append(1.00 + ISRUnc if 'ttbar' in proc else -1)
        PU.append(1.00 + abs((hPUd.GetBinContent(b)-hPUu.GetBinContent(b))/(2 * hPU.GetBinContent(b))) if hPU.GetBinContent(b)!=0 else -1)
        leptonSF.append(1.00 + abs((hLeptonSFd.GetBinContent(b)-hLeptonSFu.GetBinContent(b))/(2 * hLeptonSF.GetBinContent(b))) if hLeptonSF.GetBinContent(b)!=0 else -1)
        BTag_b.append(1.00 + abs((hBTagSFbd.GetBinContent(b)-hBTagSFbu.GetBinContent(b))/(2 * hBTagSF.GetBinContent(b))) if hBTagSF.GetBinContent(b)!=0 else -1)
        BTag_l.append(1.00 + abs((hBTagSFld.GetBinContent(b)-hBTagSFlu.GetBinContent(b))/(2 * hBTagSF.GetBinContent(b))) if hBTagSF.GetBinContent(b)!=0 else -1)
        BTag_l_cor.append(1.00)
        BTag_b_cor.append(1.00)
        L1prefire.append(1.00 + abs((hL1Prefired.GetBinContent(b)-hL1Prefireu.GetBinContent(b))/(2 * hL1Prefire.GetBinContent(b))) if hL1Prefire.GetBinContent(b)!=0 else -1)
        softbSF.append(1.00)
        wPt.append((1.00 + abs((hWPtd.GetBinContent(b)-hWPtu.GetBinContent(b))/(2 * hWPt.GetBinContent(b))) if hWPt.GetBinContent(b)!=0 else -1) if 'WJet' in proc else -1)
        Xsec.append(hXsec.GetBinContent(b)/h.GetBinContent(b) if h.GetBinContent(b)!=0 else -1)
        JEC.append(1.00 + abs((hJECd.GetBinContent(b)-hJECu.GetBinContent(b))/(2 * hNom.GetBinContent(b))) if hNom.GetBinContent(b)!=0 else -1)
        JER.append(1.00 + abs((hJERd.GetBinContent(b)-hJERu.GetBinContent(b))/(2 * hNom.GetBinContent(b))) if hNom.GetBinContent(b)!=0 else -1)
        
    oname = 'File/'+proc+'.txt'
    with open(oname,'w') as ofile:
        ofile.write('rate,'+','.join(list(str(r) for r in rate))+'\n')
        ofile.write('stat,'+','.join(list(str(r) for r in stat))+'\n')
        ofile.write('Lumi,'+','.join(list(str(r) for r in Lumi))+'\n')
        ofile.write('LumiCor,'+','.join(list(str(r) for r in Lumi_cor))+'\n')
        ofile.write('LumiCor1718,'+','.join(list(str(r) for r in Lumi_1718))+'\n')
        ofile.write('PU,'+','.join(list(str(r) for r in PU))+'\n')
        ofile.write('JEC,'+','.join(list(str(r) for r in JEC))+'\n')
        ofile.write('JER,'+','.join(list(str(r) for r in JER))+'\n')
        ofile.write('leptonSF,'+','.join(list(str(r) for r in leptonSF))+'\n')
        ofile.write('nISR,'+','.join(list(str(r) for r in nISR))+'\n')
        ofile.write('wPt,'+','.join(list(str(r) for r in wPt))+'\n')
        ofile.write('BTag_l,'+','.join(list(str(r) for r in BTag_l))+'\n')
        ofile.write('BTag_b,'+','.join(list(str(r) for r in BTag_b))+'\n')
        ofile.write('BTag_l_cor,'+','.join(list(str(r) for r in BTag_l_cor))+'\n')
        ofile.write('BTag_b_cor,'+','.join(list(str(r) for r in BTag_b_cor))+'\n')
        ofile.write('L1prefire,'+','.join(list(str(r) for r in L1prefire))+'\n')
        ofile.write('softbSF,'+','.join(list(str(r) for r in softbSF))+'\n')
        ofile.write('Xsec,'+','.join(list(str(r) for r in Xsec))+'\n')
