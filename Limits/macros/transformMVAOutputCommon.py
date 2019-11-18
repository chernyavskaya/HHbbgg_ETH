import sys, types, os
from optparse import OptionParser, make_option
from  pprint import pprint
from array import array

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

    ## setTDRStyle()
    ROOT.gStyle.SetOptStat(0)
       

    files = options.file.split(',') 
    fin2016 = ROOT.TFile.Open(files[0])
    fin2017 = ROOT.TFile.Open(files[1])
    fin2018 = ROOT.TFile.Open(files[2])
    tree2016 = fin2016.Get("reducedTree") #2016
    tree2017 = fin2017.Get("reducedTree") #2017
    tree2018 = fin2018.Get("reducedTree") #2017

    for nameTagPos,s in enumerate(files[0].split("/")):
        print nameTagPos, s
        if "outfil" in s:
            nameTagPos += 1 
            break

    print nameTagPos
    name = options.file.split("/")[nameTagPos]



    #$HOME
    fout = ROOT.TFile.Open("/shome/nchernya/HHbbgg_ETH_devel/Limits/macros/plots/cumulatives/cumulativeTransformation_"+name+".root","recreate")

    nbins = 80000
    xlow = 0.
    xup = 1.
### Reweight to match S/B for 2017 since 2017 is the best year. Take as bkg diphoton(cleaned from overlap)+diphoton+bjets. We did not take gJets here because in 2016 and 2018 right now we have ~8k events which is too small to estimate properly the bkg. 
    newWeight2016 = 1.089  #(B_2017/S_2017)/(B_2016/S_2016) = (9.69362182617187500e+02/4.18241828651538472e-01)/(8.29695556640625000e+02/0.39000478) 
    newWeight2017 = 1.
    newWeight2018 = 1.024  #(B_2017/S_2017)/(B_2018/S_2018) = (9.69362182617187500e+02/4.18241828651538472e-01)/(9.25812927246093750e+02/4.08981237703397726e-01)
    histoMVA = ROOT.TH1F("histoMVA","histoMVA",nbins,xlow,xup)
    MVAname = 'MVAOutput'   ###BE CAREFUL, Make sure you use the corerct name
  #  MVAname = 'HHbbggMVA'
    tree2016.Draw("%s/(%s*(1-%.5f)+%.5f)>>histoMVA"%(MVAname,MVAname,newWeight2016,newWeight2016),ROOT.TCut("weight*35.92/41.53"))
    tree2017.Draw("%s>>+histoMVA"%MVAname,ROOT.TCut("weight"))
    tree2018.Draw("%s/(%s*(1-%.5f)+%.5f)>>+histoMVA"%(MVAname,MVAname,newWeight2018,newWeight2018),ROOT.TCut("weight*59.74/41.53"))
    print 'entries of hist = ',histoMVA.GetEntries()

    cumulativeHisto = histoMVA.GetCumulative()
    cumulativeHisto.Scale(1./histoMVA.Integral())
    cumulativeGraph = ROOT.TGraph(cumulativeHisto)
    cumulativeGraph.SetTitle("cumulativeGraph")
    cumulativeGraph.SetName("cumulativeGraph")

    evalCumulatives = ROOT.TH1F("eval","eval",nbins,0,1)

    x , y = array( 'd' ), array( 'd' )
    step = (xup-xlow)/nbins
    for i in range(1,nbins):
#        xvalue = ROOT.gRandom.Gaus()
        xvalue = ROOT.TH1.GetRandom(histoMVA)
        evalCumulatives.Fill(cumulativeGraph.Eval(xvalue))
    evalCumulatives.Sumw2()
    evalCumulatives.Scale(1./evalCumulatives.Integral())
    evalCumulatives.GetYaxis().SetRangeUser(0,2./evalCumulatives.GetNbinsX())

    c = ROOT.TCanvas()
    histoMVA.SetLineColor(ROOT.kRed)
    histoMVA.Draw()


    print name

    formats = [".png",".pdf"]

    for format in formats:
        c.SaveAs("/shome/nchernya/HHbbgg_ETH_devel/Limits/macros/plots/cumulatives/"+name+"_func"+format)

    cumulativeGraph.Draw("AP")
    for format in formats:
        c.SaveAs("/shome/nchernya/HHbbgg_ETH_devel/Limits/macros/plots/cumulatives/"+name+"_cum"+format)

    evalCumulatives.Draw("EP")
    for format in formats:
        c.SaveAs("/shome/nchernya/HHbbgg_ETH_devel/Limits/macros/plots/cumulatives/"+name+"_evalx"+format)
    

    cumulativeGraph.Write()
    fout.Write()
    fout.Close()


if __name__ == "__main__":

    parser = OptionParser(option_list=[
            make_option("-i", "--infile",
                        action="store", type="string", dest="file",
                        default="",
                        help="input file",
                        ),
            ]
                          )

    (options, args) = parser.parse_args()
    sys.argv.append("-b")

    
    pprint(options.__dict__)

    import ROOT
    
    main(options,args)
        
