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
    argParser.add_argument('--bins',           action='store',                     type=str,            default='0',         help="Which bin?" )
    argParser.add_argument('--sig',            action='store',                     type=str,            default='250_240',   help="Which signal sample point?" )
    return argParser

options = get_parser().parse_args()
                           
bins = options.bins
spoint = options.sig

sbin = int(bins)
binlabel = SRBinLabelList[sbin]
signame = 'T2tt'

sig = signame+'_'+spoint
procnames = [signame] + bkgs 
procs = [sig] + bkgs
nproc = len(procs)
nbkg =len(bkgs)


obs = 0
rate = []
syst = {}

for s in sys:
    syst[s] = s+' lnN '
    for proc in procs:
        infile = 'File/'+proc+'.txt'
        with open(infile,'r') as ifile:
            for line in ifile:
                line = line.rstrip()
                linesplit = line.split(',')
                if linesplit[0]==s:
                    si = linesplit[sbin+1] if linesplit[sbin+1]!='-1' else "-"
        syst[s] = syst[s] +si+' '
    

with open('File/Data.txt','r') as ifile:
        for line in ifile:
            line = line.rstrip()
            linesplit = line.split(',')
            if linesplit[0]=="rate":
                obs = int(float(linesplit[sbin+1]))

for proc in procs:
    infile = 'File/'+proc+'.txt'
    with open(infile,'r') as ifile:
        for line in ifile:
            line = line.rstrip()
            linesplit = line.split(',')
            if linesplit[0]=="rate":
                data = float(linesplit[sbin+1])
                rate.append(data)



oname = "datacard_Bin"+binlabel+".txt"
with open(oname,'w') as ofile:
    divider = 50
    ofile.write("imax 1 number of bins\n")
    ofile.write("jmax "+str(nbkg)+" number of backgrounds\n")
    ofile.write("kmax * number of nuisances\n")
    ofile.write('-'*divider+"\n")
    ofile.write("bin "+binlabel+"\n")
    ofile.write("observation {:0.0f}\n".format(obs))
    ofile.write('-'*divider+"\n")
    binlabel = binlabel+" "
    ofile.write("bin "+binlabel*nproc+"\n")
    ofile.write("process "+' '.join([proc for proc in procnames])+"\n")
    ofile.write("process "+' '.join([str(i) for i in xrange(len(procs))])+"\n")
    ofile.write("rate "+' '.join(["{:0.3f}".format(r) for r in rate])+"\n")
    ofile.write('-'*divider+"\n")
    for s in syst:
        ofile.write(syst[s]+"\n") 
