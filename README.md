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

Now we calculate the limit with the usual systematics included. Combine tool basically calculate the r value (signal strength) for each signal mass point. After this step, the task is to extract the exclusion contour and also plotting the exclusion limit.


The README in master or other branch explain how the limit script works. Here the workflow of the plotting script will be described.

Extraction and combining r value whole signal spectra.

This is done in MakeSMSRootFile_dm.py. The output root file from each signal has a tree called 'limit' which contains some branches of which two branches are usefull to us: quantileExpected and limit that corresponds to r value.

Inside MakeSMSRootFile_dm.py, getLimit() function extract the r value and assign it to observed, expected, expected+1sigma, expected-1sigma limit dictionary according to the value of quantileExpected.

Now inside fillAsymptoticLimits() function, 8 2D histograms are defined to store the limit values and then filled by calling getLimit() for each signal point. The Xaxis is mstop and Yaxis is dm (mstop, mLSP) since r value is measued for each mass point which is parametrized in mstop and dm.

hexp        stores nominal expected r value
hexpup      stores expected+1sigma r value
hexpdown    stores expected-1sigma r value
hobs        stores nominal observed r value
hobsup      stores observed + 1sigma(from theory) r value
hobsdown    stores observed - 1sigma(from theory) r value
hxsecexp    stores expected r value * theory Xsec
hxsecobs    stores observed r value * theory Xsec

theory Xsec is extracted from a given root file where theoretical Xsec and its error is stored in a histogram in the bin of mstop. Observed + 1sigma(from theory) r value means observed r value * theory Xsec/(theory Xsec + theory Xsec error) similarly observed - 1sigma(from theory) r value is observed r value * theory Xsec/(theory Xsec - theory Xsec error). If only the expected limit is calculated, i.e., no observed r value in the root file (from each signal), the obs 2D hostos will be empty.

These 2D histograms are stored in a root file called 'results_T2tt.root'. Now fillAsymptoticLimits() function calls a .C script namely makeScanPlots_dm.C where the exlusion contour is extracted and stored in a final root foot file called 'limit_scan_T2tt.root'. makeScanPlots_dm.C does the following: 
First define similar 8 2D histograms and assign it to the corresponding histograms from results_T2tt.root. The only modification is if the observed histograms in results_T2tt.root file are empty, here observed histograms (hobs, hobsup, hobsdown, hxsecobs) are assined to the corresponding expected hostograms so that no histogram is empty. Now we store the exp (& up, down), obs (& up, down), expxsec, obsxsec values and their corresponding mstop and dm values (from those 8 2d hisos) in vectors. Using these vectors we define 8 2D TGraphs.

glimexp from expxsec
glimobs from obsxsec
gexp, gexpup, gexpdown from exp (& up, down)
gobs, gobsup, gobsdown from obs (& up, down)

The range and binning are set and 2 2D histograms are extracted from TGraphs: hlimexp from glimexp and hlimobs from glimobs.
Now the important part: limit contour is extracted in DrawContours() function which takes 2D TGraph as input and extract the contour using following commands
```
TH2D* hist = g2.GetHistogram();
TVirtualHistPainter* histptr = hist->GetPainter();
TList *l = histptr->GetContourList(1.);
```
The contour is stored as 1D TGraph
```
TGraph *g = static_cast<TGraph*>(l->At(i));
```
DrawContours() funtion returns the 1D TGraph of contour. So now we have 1D contours: cexp (from gexp), cexpup (from gexpup), cexpdown (from gexpdown), cobs (from gobs), cobsup(from gobsup), cobsdown (from gobsdown). These 1D contour TGraphs are then stored in the output root file (limit_scan_T2tt.root) by the names with prefix "graph_smoothed" followed by "_Exp", "_Obs" and so on. 2D histograms hlimexp and hlimobs are also stored by the names "hXsec_exp_corr" and "hXsec_obs_corr" respectively. hxsecexp and hxsecobs are also stored by names "hXsec_exp" and "hXsec_obs".

Making temperature plot

This is done inside PlotsSMS directory. Here we provide the parameters like root file name (limit_scan_T2tt.root), base histograms (usually "hXsec_obs_corr" or "hXsec_exp_corr"), expected and observed exclusion contour specifications (like 1D contour graph name, color), and some other parameters like CMS text (Preliminary), LUMI and ENERGY by a config file named T2tt_dm_SUS.cfg which is inside config directory. Though LUMI and ENERGY values will be modified later by other python file.
All the python scripts are inside python directory. We run the script makeSMSplots.py which take config file, T2tt_dm_SUS.cfg as 1st argument and output name as 2nd argument (usually as T2tt). First, all the parameters are processed (like config file name, model name, analysis label and output) and objects (histograms, contour graphs etc) are accessed by the class inputFile() from inputFile.py.

1. Now smsPlotXSEC class is called from smsPlotXSEC.py. The temperature plot is drwn by this smsPlotXSEC class which is derived class of smsPlotABS() base class from smsPlotABS.py. Lets see what smsPlotXSEC class does. It takes the following aruguments: modelname, histo, obsLimits, expLimits, energy, lumi, preliminary, label. First it process all the parameters with the function standardDef() which is from smsPlotABS(). Then it define a canvas, a histo (the base 2D histogram) and also runs setStyle() which is from smsPlotABS() and runs setStyleCOLZ() which is for decorating Zaxis and Zaxis color palette.
Now lets see smsPlotABS() class does. It takes similar arguments as smsPlotXSEC(), first initialize standardDef() which processed the parameters as mention before, set some more plotting parameter (like decay mode, susy particle, axis range etc.) according to the modelname by calling sms() class from sms.py and also define an empty 2D histograms. In smsPlotABS.py, we have DrawText() function which draw CMS text like lumi using CMS_lumi() class from CMS_lumi.py. We need to set correct energy and lumi value inside CMS_lumi.py. next we have DrawLegend() which specify the legend text from expected and observed limit contours. then we have Save() function which save the temp plot in pdf and png format accosding to the model name provided. Finally we have DrawLines() function where contour lines are drawn.

2. next smsPlotXSEC.Draw() is called. Inside smsPlotXSEC.py Draw() function does following things:
Draw empty 2D histogram (empty histo from smsPlotABS())
Draw base 2D histogram
run DrawLines() (through smsPlotABS())
run DrawText()(through smsPlotABS())
run DrawLegend() (through smsPlotABS())
run DrawPaletteLabel() (set Z axis text)

3. finally smsPlotXSEC.Save() (through smsPlotABS())


Limit comparison scripts

Now since we already described how the temp limit plot is made starting from the output root file from each signal point. Here we add an extra set of scripts to make comparison limit plot inside PlotSMSExt directory. Presently, it compares two limits and the specification need to be provided in the config file namely T2tt_dm_SUSExt.cfg. Later more generic script can be added out of the existing scripts.