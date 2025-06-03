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
git clone -b BKVal git@github.com:1LStopBudapest/LimitSetting.git

cd LimitSetting
mkdir DataCard

```

Now we check how good is the fit in the CR of the validation region. Then we calculate the normalization from the CR and apply the normalization to Wjets & ttba processin the SR and check how good total MC agrees with data.

The second part can be done in two ways:
First one is automatically done by combine tool through 'RateParam' implementation in the datacard. After running `FitDiagnostics`, prefit & postfit plots are drawn using `preFitPlot.py` & `postFitPlot.py` scripts respectively.


Second option would be running the combine for CR bins only and get the normalisation (bin-wise) from pre & post fit histograms and apply the norm to the prefit SR histograms and compare data MC agreement. This is done using `NormCal.py`


So we start with the region histograms and make the datacard with usual systematics included. We make region histograms for Wjets, ttbar and other SM  processes, also from the data. We make region histogram just for on signal point. Its for the placeholder in the datacard.

One can make that by using `PromptBKValScript.py` in NanoTuplePlot. Please check the link, https://github.com/1LStopBudapest/NanoTuplePlot
The above part can be done in local computer or in higgs machine.

Then the important step is to copy those region root files to the File directory

Go to where you produce these root files and use the following command to copy those into lxplus working directory
```
scp path-to-the-files/PromptBKVal1_SR+CR*.root username@lxplus7.cern.ch:path-to-your-working-dir/CMSSW_10_2_13/src/LimitSetting/File/

```
For val2, root file will appear as PromptBKVal2_SR+CR_#precess.root


Now back to lxplus working directory

```
cd CMSSW_14_1_0_pre4/src/
cmsenv
cd LimitSetting

```

Fist check Config.py to set the number of bins, processes, signal points etc. The bins (SR & CR) should be compatible with the Region histograms bins. Change the value of reg variable to Val1 & Val2 according to region of your choice.


Make text files

Inside LimitSetting direcotry run the following command to make the text files from which datacard will be made.

```
python3 MakeTextFileScript.py

```

Make datacard

Inside LimitSetting direcotry run the following command to make the datacard and combine the cards.
Make the datacard accrding to the choice of method as mentioned earlier

```
python3 DataCardScript.py

```

Now we run the fitdiagnostic 

```
combineCards.py DataCard/CCDataCard_T2tt_1000_920.txt -S > myshapecard.txt
combine -M FitDiagnostics myshapecard.txt --saveShapes --saveWithUncertainties
```
This will create the output root file, fitDiagnosticsTest.root. Using this root file, we can create data-MC plot using the scripts as mentioned earlier.

```
python3 preFitPlot.py
python3 postFitPlot.py
```