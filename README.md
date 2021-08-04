This works within CMSSW environment. So please log in to your lxplus account.

Set up a CMSSW area

```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.1.0

cd $CMSSW_BASE/src
scramv1 b clean
scramv1 b

git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b

```

Get the limit directory

```
git clone git@github.com:1LStopBudapest/LimitSetting.git

cd LimitSetting
mkdir DataCard
mkdir File
cd File
wget https://github.com/1LStopBudapest/AuxFiles/blob/main/xSec.root
cd ..
```

Now we calculate the expected limit with MC events. More script will be added to calculate both expected and and observed limit using predicted SM backgrounds from control regions (CR).

For now we only consider the expected yield from MC in search regions (SR). So to get that we need to make region histograms for the signal and background processes.
One can make that by using MakeRegionHistScripy.py in NanoTuplePlot. Please check the link, https://github.com/1LStopBudapest/NanoTuplePlot
The above part can be done in local computer or in higgs machine.

Then the important step is to copy those region root files to the File directory

Go to where you produce these root files and use the following command to copy those into lxplus working directory
```
scp path-to-the-files/RegionPlot_SR*.root username@lxplus7.cern.ch:path-to-your-working-dir/CMSSW_10_2_13/src/LimitSetting/File/

```
Now back to lxplus working directory

```
cd CMSSW_10_2_13/src/
cmsenv
cd LimitSetting

```

Make text files

Inside LimitSetting direcotry run the following command to make the text files from which datacard will be made.

```
python MakeTextFileScript.py

```

Make datacard

Inside LimitSetting direcotry run the following command to make the datacard and combine the cards

```
python DataCardScript.py

```

Run Limit

```
python LimitRunScript.py

```

This will create the limit output root file for each signal. Now we need to make the exlusion limit plot. Here we use the package from https://github.com/CMS-SUS-XPAG/PlotsSMS  and modify it according to our purpose.

But we first need to make the root file from which this plotting package make the limit plot.

Run the following command

```
python SMSRootFileScript.py

```
Now go to PlotsSMS dir.

```
cd PlotsSMS

```

Run the following command to make the temperature plot

```
python python/makeSMSplots.py config/T2tt_dm_SUS.cfg T2tt

```