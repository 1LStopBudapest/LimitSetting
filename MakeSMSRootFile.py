#! /usr/bin/python
import os
import sys
import math
import ROOT
from Config import *



def getLimit(rootFile):
    file = ROOT.TFile(rootFile)
    output = ''
    limits={}
    tree = ROOT.TChain('limit')
    tree.Add(rootFile)
    for entry in tree:
        if entry.quantileExpected < 0:
            output += 'Observed : r < %4.2f \n' % (entry.limit)
        else:
            output += 'Expected %4.2f %% : r < %4.2f \n' % (
                    (100.0 * entry.quantileExpected), entry.limit)
        if entry.quantileExpected < 0:
            limits['obs'] = entry.limit
        if 0.1 < entry.quantileExpected < 0.2:
            limits['-1'] = entry.limit
        elif 0.4 < entry.quantileExpected < 0.6:
            limits['0'] = entry.limit
        elif 0.8 < entry.quantileExpected < 0.9:
            limits['+1'] = entry.limit
    return (output, limits)


def fillAsymptoticLimits(signals, limfilename, excfilename, interpolate):
    limits = []
    currentDir = os.getcwd()
    xsecfilename = ('File/xSec.root')
    outfile = ROOT.TFile(limfilename, 'RECREATE')
    maxmstop = 0.0
    minmstop = 0.0
    maxmlsp = 0.0
    minmlsp = 0.0
    mstop_step = 1
    mlsp_step = 2
    for signal in signals:
        mstop = int(signal.split('_')[0])
        mlsp = int(signal.split('_')[1])
        if mstop > maxmstop: maxmstop = mstop
        if mlsp > maxmlsp: maxmlsp = mlsp
        if minmstop == 0.0 or mstop < minmstop: minmstop = mstop
        if mlsp < minmlsp: minmlsp = mlsp
    nbinsx = int((maxmstop - minmstop) / mstop_step)
    nbinsy = int((maxmlsp - minmlsp) / mlsp_step)
    minmstop -= 0.5*mstop_step
    maxmstop -= 0.5*mstop_step
    print 'XMin: %4.2f, XMax: %4.2f, YMin: %4.2f, YMax: %4.2f, NXBins: %d, NYBins: %d' % (minmstop, maxmstop, minmlsp, maxmlsp, nbinsx, nbinsy)


    hexp = ROOT.TH2D('hexp', '', nbinsx, minmstop, maxmstop, nbinsy, minmlsp, maxmlsp)
    hexpup = ROOT.TH2D('hexpup', '', nbinsx, minmstop, maxmstop, nbinsy, minmlsp, maxmlsp)
    hexpdown = ROOT.TH2D('hexpdown', '', nbinsx, minmstop, maxmstop, nbinsy, minmlsp, maxmlsp)
    hxsecexp = ROOT.TH2D('hxsecexp', '', nbinsx, minmstop, maxmstop, nbinsy, minmlsp, maxmlsp)
    hxsecobs = ROOT.TH2D('hxsecobs', '', nbinsx, minmstop, maxmstop, nbinsy, minmlsp, maxmlsp)
    hobs = ROOT.TH2D('hobs', '', nbinsx, minmstop, maxmstop, nbinsy, minmlsp, maxmlsp)
    hobsup = ROOT.TH2D('hobsup', '', nbinsx, minmstop, maxmstop, nbinsy, minmlsp, maxmlsp)
    hobsdown = ROOT.TH2D('hobsdown', '', nbinsx, minmstop, maxmstop, nbinsy, minmlsp, maxmlsp)

    xsecfile = ROOT.TFile(xsecfilename)
    xsechist = ROOT.TH1D()
    xsechist = xsecfile.Get("stop_xsection")
    for signal in signals:
        rootFile = 'higgsCombine_T2tt_'+signal+'.AsymptoticLimits.mH120.root'
        if rootFile == '':
            limits.append(signal + ': no limit found..')
        else:
            output = getLimit(rootFile)
            print signal, ':\n', output
            tempLimit = ''
            for line in output[0].split('\n'):
                if 'Observed' in line:
                    tempLimit = line.replace('Observed\t', signal + ' observed')
                if 'Expected 50' in line:
                    tempLimit += line.replace('Expected\t', signal + ' expected')
            limits.append(tempLimit)
            mstop = int(signal.split('_')[0])
            mlsp = int(signal.split('_')[1])
            limit = output[1]
            binIdx = xsechist.FindBin(float(mstop))
            xsec = xsechist.GetBinContent(binIdx)
            xsecup = xsec + xsechist.GetBinError(binIdx)
            xsecdown = xsec - xsechist.GetBinError(binIdx)
            if scalesigtoacc:
                xseclimit = limit['0']
                xsecobslimit = 0.0
                hexp.Fill(mstop, mlsp, limit['0'] / xsec)
                hexpdown.Fill(mstop, mlsp, limit['-1'] / xsec)
                hexpup.Fill(mstop, mlsp, limit['+1'] / xsec)
                if limit.has_key('obs'):
                    xsecobslimit = limit['obs']
                    hobs.Fill(mstop, mlsp, limit['obs'] / xsec)
                    hobsdown.Fill(mstop, mlsp, limit['obs'] / xsecup)
                    hobsup.Fill(mstop, mlsp, limit['obs'] / xsecdown)
                    print 'MStop: %d, MLSP: %d, XS: %4.2f, Exp Limit: %4.2f (+1 expt: %4.2f, -1 expt: %4.2f), Obs Limit: %4.2f (+1 theory: %4.2f, -1 theory: %4.2f), XS Limit: %4.2f exp, %4.2f obs' % (mstop, mlsp, xsec, limit['0'] / xsec, limit['+1'] / xsec, limit['-1'] / xsec, limit['obs'] / xsec, limit['obs'] / xsecdown, limit['obs'] / xsecup, xseclimit, xsecobslimit)
                else:
                    print 'MStop: %d, MLSP: %d, XS: %4.2f, Limit: %4.2f (+1: %4.2f, -1: %4.2f), XS Limit: %4.2f' % (mstop, mlsp, xsec, limit['0'] / xsec, limit['+1'] / xsec, limit['-1'] / xsec, xseclimit)
            else:
                xseclimit = limit['0'] * xsec
                xsecobslimit = 0.0
                hexp.Fill(mstop, mlsp, limit['0'])
                hexpdown.Fill(mstop, mlsp, limit['-1'])
                hexpup.Fill(mstop, mlsp, limit['+1'])
                if limit.has_key('obs'):
                    xsecobslimit = limit['obs'] * xsec
                    hobs.Fill(mstop, mlsp, limit['obs'])
                    hobsdown.Fill(mstop, mlsp, limit['obs'] * xsec / xsecup)
                    hobsup.Fill(mstop, mlsp, limit['obs'] * xsec / xsecdown)
                    print 'MStop: %d, MLSP: %d, XS: %4.2f, Exp Limit: %4.2f (+1 expt: %4.2f, -1 expt: %4.2f), Obs Limit: %4.2f (+1 theory: %4.2f, -1 theory: %4.2f), XS Limit: %4.2f exp, %4.2f obs' % (mstop, mlsp, xsec, limit['0'], limit['+1'], limit['-1'], limit['obs'], limit['obs'] * xsec / xsecdown, limit['obs'] * xsec / xsecup, xseclimit, xsecobslimit)
                else:
                    print 'MStop: %d, MLSP: %d, XS: %4.2f, Limit: %4.2f (+1: %4.2f, -1: %4.2f), XS Limit: %4.2f' % (mstop, mlsp, xsec, limit['0'], limit['+1'], limit['-1'], xseclimit)
            hxsecexp.Fill(mstop, mlsp, xseclimit)
            hxsecobs.Fill(mstop, mlsp, xsecobslimit)


    outfile.cd()
    hexp.Write()
    hexpdown.Write()
    hexpup.Write()
    hobs.Write()
    hobsdown.Write()
    hobsup.Write()
    hxsecexp.Write()
    hxsecobs.Write()
    outfile.Close()
    os.system('root -l -q -b makeScanPlots.C\\(\\"%s\\",\\"%s\\",%d,%d\\)' %(outfile, excfilename, expectedonly, interpolate))

    # print the results
    print '=' * 5, 'RESULTS', '(' + limitmethod + ')', '=' * 5
    print '\n'.join(limits)
    print '\n'

signals = signals
limitFile = 'results_T2tt.root'
exclusionFile = 'limit_scan_T2tt.root'
if fillAsymptoticLimits: fillAsymptoticLimits(signals, limitFile, exclusionFile, addInterpolation)

