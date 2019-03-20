import sys, types, os
from optparse import OptionParser, make_option
from  pprint import pprint
from array import array

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

    ## setTDRStyle()
    ROOT.gStyle.SetOptStat(0)
       

    files = options.file.split(',') 
    fin = ROOT.TFile.Open(files[0])
    fin2 = ROOT.TFile.Open(files[1])
    tree = fin.Get("reducedTree_sig") #2016
    tree2 = fin2.Get("reducedTree_sig") #2017

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
    #newWeight = 1.011026  #with wrong generatd SM
    newWeight = 0.974801  ## (5.0652/1852.6094)*(1./(5.5086/1964.0142))  #with reweighted to SM  
    histoMVA = ROOT.TH1F("histoMVA","histoMVA",nbins,xlow,xup)
   # MVAname = 'MVAOutput'
    MVAname = 'HHbbggMVA'
    tree.Draw("%s>>histoMVA"%MVAname,ROOT.TCut("weight"))
    tree2.Draw("%s/(%s*(1-%.5f)+%.5f)>>+histoMVA"%(MVAname,MVAname,newWeight,newWeight),ROOT.TCut("weight*41.5/35.9"))
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
        
