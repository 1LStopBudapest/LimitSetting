This works within CMSSW environment. So please log in to your lxplus account.
The following setup works in el9 on lxplus (latest one). Now its python3


Set up a CMSSW area

```
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v10.0.2

cd $CMSSW_BASE/src
scramv1 b clean
scramv1 b

git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
cd CombineHarvester
git checkout v3.0.0
cd $CMSSW_BASE/src
scram b

```

Get the limit directory

```
git clone -b ExpectedLimitMC git@github.com:1LStopBudapest/LimitSetting.git

cd LimitSetting
mkdir DataCard

```

Now we calculate the expected limit with MC events with the usual systematics included.


For now we only consider the expected yield from MC in search regions (SR) and also associated systemaics. So to get that we need to make region histograms for the signal and background processes.


One can make those by using CountDCHistScript.py and CountDCHistJECScript.py in NanoTuplePlot. Please check the link, https://github.com/1LStopBudapest/NanoTuplePlot
The above part can be done in local computer or in higgs machine.
While running CountDCHistScript.py and CountDCHistJECScript.py, use --region 'SR' option


Now copy those root files to the File directory

Go to where you produce these root files and use the following command to copy those into lxplus working directory
```
scp path-to-the-files/CountDCHist_SR*.root username@lxplus.cern.ch:path-to-your-working-dir/CMSSW_14_1_0_pre4/src/LimitSetting/File/

```


Now back to lxplus working directory

```
cd CMSSW_14_1_0_pre4/src/
cmsenv
cd LimitSetting

```

Fist check Config.py to set the number of bins, processes, signal points etc. The bins (SR) should be compatible with the Region histograms bins.


Make text files

Inside LimitSetting direcotry run the following command to make the text files from which datacard will be made.

```
python3 MakeTextFileScript.py

```

Make datacard

Inside LimitSetting direcotry run the following command to make the datacard and combine the cards

```
python3 DataCardScript.py

```

Run Limit

```
python3 LimitRunScript.py

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


To run with new BK composition


Inside Config.py, a variable namely BKmode is set to 'old' by default, one need to change it to 'new' to have new BK composition. Also, it is necessary to have the region histogram in that new BK format. One can get the new root files from the root files prduced by CountDCHistScript.py and CountDCHistJECScript.py. Assuming one already produced files by CountDCHistScript.py and CountDCHistJECScript.py, new format root files can be obtained by running 'BKDivision.py' which is provided inside Helper directory. The above part can be done in local computer or in higgs machine where Helper is already checked out.


To run with Prompt normalization from CR bins


There is another flag inside Config.py called 'PromptNorm' set to default valuse as False so that the limit is calculated with only the expected yield from BKs. If you want to scale the yield of prompt BKs with the normalization from CR, then set the 'PromptNorm' to True.


First, you need to rerun the CountDCHistScript.py and CountDCHistJECScript.py with --region option as 'SR+CR' in local computer or in higgs machine to produce the root files used to make the datacard.


Also, please change the input root files names from 'CountDCHist_SR_'('CountDCHistJEC_SR_') to CountDCHist_SR+CR_'(CountDCHistJEC_SR+CR_) in MakeTextFile.py