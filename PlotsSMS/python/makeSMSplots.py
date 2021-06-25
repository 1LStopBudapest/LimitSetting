import sys
from inputFile import *
from smsPlotXSEC import *
from smsPlotCONT import *
from smsPlotBrazil import *

if __name__ == '__main__':
    # read input arguments
    filename = sys.argv[1]
    modelname = sys.argv[1].split("/")[-1].split("_")[0] + '_' + sys.argv[1].split("/")[-1].split("_")[1]
    analysisLabel = sys.argv[1].split("/")[-1].split("_")[2]
    outputname = sys.argv[2]
    print 'config filename: ', filename, ' modelname: ', modelname, ' analysisLabel: ', analysisLabel, ' outputname: ', outputname
    # read the config file
    fileIN = inputFile(filename)
    
    # classic temperature histogra
    xsecPlot = smsPlotXSEC(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
    xsecPlot.Draw()
    xsecPlot.Save("%sXSEC" %outputname)

    # only lines
    #contPlot = smsPlotCONT(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
    #contPlot.Draw()
    #contPlot.Save("%sCONT" %outputname)

    # brazilian flag (show only 1 sigma)
    #brazilPlot = smsPlotBrazil(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
    #brazilPlot.Draw()
    #brazilPlot.Save("%sBAND" %outputname)
