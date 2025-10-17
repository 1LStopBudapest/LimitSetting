import os, sys

sys.path.append('../')
from Config import *


signals = Signals[Era]
cq = len(signals)

print('total noo of jobs: ',cq)


bashline = []
bashline.append("#!/bin/bash\n")
bashline.append("\n")
bashline.append("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
bashline.append("\n")
bashline.append("tar -zxvf CMSSW_14_1_0_pre4.tar.gz\n")
bashline.append("cd CMSSW_14_1_0_pre4/src/\n")
bashline.append("scram b ProjectRename\n")
bashline.append("eval `scramv1 runtime -sh`\n")
bashline.append("scram b\n")
bashline.append("\n")
bashline.append("jobid=$2\n")
bashline.append("\n")
bashline.append("cd LimitSetting\n")
bashline.append("python3 DataCardScript_condor.py --sidx $jobid\n")
bashline.append("\n")
bashline.append("python3 LimitRunScript_condor.py --sidx $jobid\n")
bashline.append("\n")
bashline.append("mv *.root ../../../")
bashline.append("\n")
bashline.append("cd ../../../")
fsh = open("CombineFilesCondor.sh", "w")
fsh.write(''.join(bashline))
fsh.close()


subline = []
subline.append('executable              = CombineFilesCondor.sh\n')
subline.append('Universe                = vanilla\n')
subline.append('+JobFlavour             = "tomorrow"\n')
subline.append('output                  = CombineFilesCondor.$(ClusterId).$(ProcId).out\n')
subline.append('error                   = CombineFilesCondor.$(ClusterId).$(ProcId).err\n')
subline.append('log                     = CombineFilesCondor.$(ClusterId).$(ProcId).log\n')
subline.append('getenv                  = True\n')
subline.append('should_transfer_files   = YES\n')
subline.append('when_to_transfer_output = ON_EXIT\n')
subline.append('transfer_output_files   = higgsCombine_T2tt_$(ProcId).AsymptoticLimits.mH120.root\n')
subline.append('\n\n')
subline.append('Transfer_Input_Files    = CombineFilesCondor.sh, CMSSW_14_1_0_pre4.tar.gz\n')
subline.append('arguments               = $(ClusterId) $(ProcId)\n')
subline.append('queue %i\n'%cq)

fs = open("CombineFilesCondor.sub", "w")
fs.write(''.join(subline))
fs.close()
os.system('condor_submit CombineFilesCondor.sub')

