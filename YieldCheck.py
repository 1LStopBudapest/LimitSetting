import os, sys

def get_parser():
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser")
    argParser.add_argument('--lfile',           action='store',                     type=str,            default='ls.txt',         help="the list of all bins datacard file names" )
    return argParser

options = get_parser().parse_args()

fls = options.lfile

ZsigSRbins = []
ZsigCRbins = []
ZtBKSRbins = []
ZtBKCRbins = []
ZBKSRbins = []
ZBKCRbins = []
ZdataSRbins = []
ZdataCRbins = []

with open(fls,'r') as ifile:
    for line in ifile:
        binl = line.split('_')[1].split('.')[0]
        with open(line.rstrip('\n'),'r') as cardfile:
            for cline in cardfile:
                cline = cline.rstrip()
                clinesplit = cline.split(' ')
                if cline.startswith('rate'):
                    sig = float(clinesplit[1])
                    bk = sum(map(float, clinesplit[2:]))
                    bks = map(float, clinesplit[2:])
                    if 0.0 in bks:
                        if 'SR' in binl: ZBKSRbins.append(binl)
                        if 'CR' in binl: ZBKCRbins.append(binl)
                    if bk == 0.0 or bk < 0.0:
                        if 'SR' in binl: ZtBKSRbins.append(binl)
                        if 'CR' in binl: ZtBKCRbins.append(binl)
                    if sig == 0.0 or sig < 0.0:
                        if 'SR' in binl: ZsigSRbins.append(binl)
                        if 'CR' in binl: ZsigCRbins.append(binl)
                elif cline.startswith('observation'):
                    data = float(clinesplit[1])
                    if data == 0.0:
                        if 'SR' in binl: ZdataSRbins.append(binl)
                        if 'CR' in binl: ZdataCRbins.append(binl)

with open("SkippingBinsList.py", "w") as file:
    file.write("import os, sys\n\n")
    file.write(f"ZsigSRbins = {ZsigSRbins}\n")
    file.write(f"ZsigCRbins = {ZsigCRbins}\n")
    file.write(f"ZBKSRbins = {ZBKSRbins}\n")
    file.write(f"ZBKCRbins = {ZBKCRbins}\n")
    file.write(f"ZtBKSRbins = {ZtBKSRbins}\n")
    file.write(f"ZtBKCRbins = {ZtBKCRbins}\n")
    file.write(f"ZdataSRbins = {ZdataSRbins}\n")
    file.write(f"ZdataCRbins = {ZdataCRbins}\n")
