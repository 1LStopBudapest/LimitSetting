from __future__ import absolute_import

#import HiggsAnalysis.CombinedLimit.util.plotting as plot
import ROOT

from Config import *

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

#plot.ModTDRStyle()

bins = CRBins
binLabel = CRBinLabelList

hWJets = ROOT.TH1F('hWJets', 'hWJets', bins, 0, bins)
httbar = ROOT.TH1F('httbar', 'ttbar', bins, 0, bins)
hSingleTop = ROOT.TH1F('hSingleTop', 'hSingleTop', bins, 0, bins)
hDY = ROOT.TH1F('hDY', 'hDY', bins, 0, bins)
hTTX = ROOT.TH1F('hTTX', 'hTTX', bins, 0, bins)
hVV = ROOT.TH1F('hVV', 'hVV', bins, 0, bins)
hQCD = ROOT.TH1F('hQCD', 'hQCD', bins, 0, bins)
hZinv = ROOT.TH1F('hZinv', 'hZinv', bins, 0, bins)
hdata = ROOT.TH1F('hdata', 'hdata', bins, 0, bins)
for b in range(bins):
    hWJets.GetXaxis().SetBinLabel(b+1, binLabel[b])
    httbar.GetXaxis().SetBinLabel(b+1, binLabel[b])
    hSingleTop.GetXaxis().SetBinLabel(b+1, binLabel[b])
    hDY.GetXaxis().SetBinLabel(b+1, binLabel[b])
    hTTX.GetXaxis().SetBinLabel(b+1, binLabel[b])
    hVV.GetXaxis().SetBinLabel(b+1, binLabel[b])
    hQCD.GetXaxis().SetBinLabel(b+1, binLabel[b])
    hZinv.GetXaxis().SetBinLabel(b+1, binLabel[b])
    hdata.GetXaxis().SetBinLabel(b+1, binLabel[b])

fin = ROOT.TFile("fitDiagnosticsTest.root")
first_dir = "shapes_fit_b"

for b in range(bins):
    
    second_dir = "ch1_"+binLabel[b]
    
    h_WJets = fin.Get(first_dir + "/" + second_dir + "/WJets")
    h_ttbar = fin.Get(first_dir + "/" + second_dir + "/ttbar")
    h_SingleTop = fin.Get(first_dir + "/" + second_dir + "/SingleTop")
    h_DY = fin.Get(first_dir + "/" + second_dir + "/DY")
    h_TTX = fin.Get(first_dir + "/" + second_dir + "/TTX")
    h_VV = fin.Get(first_dir + "/" + second_dir + "/VV")
    h_QCD = fin.Get(first_dir + "/" + second_dir + "/QCD")
    h_Zinv = fin.Get(first_dir + "/" + second_dir + "/Zinv")

    h_dat = fin.Get(first_dir + "/" + second_dir + "/data")  # This is a TGraphAsymmErrors, not a TH1F

    if h_dat:
        hdata.SetBinContent(b+1, h_dat.GetY()[0])
        hdata.SetBinError(b+1, (h_dat.GetEYhigh()[0] + h_dat.GetEYlow()[0])/2)
    else:
        hdata.SetBinContent(b+1, 0)
        
    if h_WJets:
        hWJets.SetBinContent(b+1, h_WJets.GetBinContent(1)) 
        hWJets.SetBinError(b+1, h_WJets.GetBinError(1)) 
    else:
        hWJets.SetBinContent(b+1, 0)
    if h_ttbar:
        httbar.SetBinContent(b+1, h_ttbar.GetBinContent(1)) 
        httbar.SetBinError(b+1, h_ttbar.GetBinError(1)) 
    else:
        httbar.SetBinContent(b+1, 0)
    if h_SingleTop:
        hSingleTop.SetBinContent(b+1, h_SingleTop.GetBinContent(1)) 
        hSingleTop.SetBinError(b+1, h_SingleTop.GetBinError(1)) 
    else:
        hSingleTop.SetBinContent(b+1, 0)
    if h_DY:
        hDY.SetBinContent(b+1, h_DY.GetBinContent(1)) 
        hDY.SetBinError(b+1, h_DY.GetBinError(1)) 
    else:
        hDY.SetBinContent(b+1, 0)
    if h_TTX:
        hTTX.SetBinContent(b+1, h_TTX.GetBinContent(1)) 
        hTTX.SetBinError(b+1, h_TTX.GetBinError(1)) 
    else:
        hTTX.SetBinContent(b+1, 0)
    if h_VV:
        hVV.SetBinContent(b+1, h_VV.GetBinContent(1)) 
        hVV.SetBinError(b+1, h_VV.GetBinError(1)) 
    else:
        hVV.SetBinContent(b+1, 0)
    if h_QCD:
        hQCD.SetBinContent(b+1, h_QCD.GetBinContent(1)) 
        hQCD.SetBinError(b+1, h_QCD.GetBinError(1)) 
    else:
        hQCD.SetBinContent(b+1, 0)
    if h_Zinv:
        hZinv.SetBinContent(b+1, h_Zinv.GetBinContent(1)) 
        hZinv.SetBinError(b+1, h_Zinv.GetBinError(1)) 
    else:
        hZinv.SetBinContent(b+1, 0)

        

legend = ROOT.TLegend(0.40, 0.60, 0.90, 0.9)
legend.SetNColumns(3)

hStack_MC = ROOT.THStack("hStack_MC","hStack_MC")
hMC = hZinv.Clone("TotalMC")
hStack_MC.Add(hZinv)
hZinv.SetFillColor(ROOT.kOrange-3)
hZinv.SetLineColor(ROOT.kOrange-3)
legend.AddEntry(hZinv, "Zinv"+" ("+str(round(hZinv.Integral(), 2))+")", "F")
hStack_MC.Add(hQCD)
hMC.Add(hQCD)
hQCD.SetFillColor(ROOT.kMagenta+3)
hQCD.SetLineColor(ROOT.kMagenta+3)
legend.AddEntry(hQCD, "QCD"+" ("+str(round(hQCD.Integral(), 2))+")", "F")
hStack_MC.Add(hVV)
hMC.Add(hVV)
hVV.SetFillColor(ROOT.kOrange)
hVV.SetLineColor(ROOT.kOrange)
legend.AddEntry(hVV, "VV"+" ("+str(round(hVV.Integral(), 2))+")", "F")
hStack_MC.Add(hTTX)
hMC.Add(hTTX)
hTTX.SetFillColor(ROOT.kAzure-7)
hTTX.SetLineColor(ROOT.kAzure-7)
legend.AddEntry(hTTX, "TTX"+" ("+str(round(hTTX.Integral(), 2))+")", "F")
hStack_MC.Add(hDY)
hMC.Add(hDY)
hDY.SetFillColor(ROOT.kMagenta-6)
hDY.SetLineColor(ROOT.kMagenta-6)
legend.AddEntry(hDY, "DY"+" ("+str(round(hDY.Integral(), 2))+")", "F")
hStack_MC.Add(hSingleTop)
hMC.Add(hSingleTop)
hSingleTop.SetFillColor(7)
hSingleTop.SetLineColor(7)
legend.AddEntry(hSingleTop, "SingleTop"+" ("+str(round(hSingleTop.Integral(), 2))+")", "F")
hStack_MC.Add(httbar)
hMC.Add(httbar)
httbar.SetFillColor(5)
httbar.SetLineColor(5)
legend.AddEntry(httbar, "ttbar"+" ("+str(round(httbar.Integral(), 2))+")", "F")
hStack_MC.Add(hWJets)
hMC.Add(hWJets)
hWJets.SetFillColor(8)
hWJets.SetLineColor(8)
legend.AddEntry(hWJets, "WJets"+" ("+str(round(hWJets.Integral(), 2))+")", "F")
legend.AddEntry(hdata, "Data"+" ("+str(round(hdata.Integral(), 2))+")", "PE")

hRatio = hdata.Clone("Ratio")
hRatio.Divide(hMC)
hRatio.GetYaxis().SetTitle('Data/MC')
hRatio.GetYaxis().SetRangeUser(0,2)
hRatio.SetTitle("")
hRatio.SetStats(0)
hRatio.SetLineColor(ROOT.kRed)
hRatio.SetLineWidth(2)
hRatio.SetMarkerStyle(20)
hRatio.SetMarkerSize(0.6)
hRatio.GetXaxis().SetTitleSize(0.1)
hRatio.GetXaxis().SetTitleOffset(0.9)
hRatio.GetXaxis().SetLabelSize(0.07)
hRatio.GetYaxis().SetTitleSize(0.08)
hRatio.GetYaxis().SetTitleOffset(0.5)
hRatio.GetYaxis().SetLabelSize(0.07)
hRatioFrame = hRatio.Clone("RatioFrame")
for b in range(1, hRatioFrame.GetNbinsX() + 1):
    hRatioFrame.SetBinContent(b, 1.0)
hRatioFrame.SetLineColor(ROOT.kGreen)

hdata.SetTitle("")
hdata.GetYaxis().SetTitle("Events")
hdata.GetYaxis().SetTitleSize(0.035)
hdata.GetYaxis().SetTitleOffset(1.2)
hdata.GetYaxis().SetLabelSize(0.03)
hdata.SetLineColor(ROOT.kBlack)
hdata.SetLineWidth(2)
hdata.SetMarkerStyle(20)
hdata.SetMarkerColor(ROOT.kBlack)
hdata.SetMarkerSize(0.5)
hdata.SetStats(0)
hdata.GetYaxis().SetRangeUser(0.1, hdata.GetMaximum() * 100 * 1.5)

c = ROOT.TCanvas('c', '', 600, 800)
p1 = ROOT.TPad("p1", "p1", 0, 0.3, 1, 1.0)
p1.SetBottomMargin(0)
p1.Draw()
p1.cd()
hdata.Draw("PE")
hStack_MC.Draw("histsame")
hdata.DrawCopy("PESAME")
legend.Draw()
ROOT.gPad.SetLogy()
c.cd()
p2 = ROOT.TPad("p2", "p2", 0, 0.01, 1, 0.3)
p2.SetTopMargin(0)
p2.SetBottomMargin(0.2)
p2.Draw()
p2.cd()
hRatio.Draw("PE")
hRatioFrame.Draw("HISTsame")
c.SaveAs("PromptBKVal2_postfitplot_CR.png")
c.Close()
