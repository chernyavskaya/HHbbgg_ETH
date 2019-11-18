import sys, types, os
from optparse import OptionParser, make_option
from  pprint import pprint
from array import array

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

### Reweight to match S/B for 2017 since 2017 is the best year. Take as bkg diphoton(cleaned from overlap)+diphoton+bjets. We did not take gJets here because in 2016 and 2018 right now we have ~8k events which is too small to estimate properly the bkg. 
    newWeight2016 = 1.089  #(B_2017/S_2017)/(B_2016/S_2016) = (9.69362182617187500e+02/4.18241828651538472e-01)/(8.29695556640625000e+02/0.39000478) 
    newWeight2017 = 1.
    newWeight2018 = 1.024  #(B_2017/S_2017)/(B_2018/S_2018) = (9.69362182617187500e+02/4.18241828651538472e-01)/(9.25812927246093750e+02/4.08981237703397726e-01)

    lumi2016=35.92
    lumi2017=41.53
    lumi2018=59.74
      

    ## setTDRStyle()
    ROOT.gStyle.SetOptStat(0)
        
    fin_graph = ROOT.TFile.Open(options.graphfile)
    cumulativeGraph = fin_graph.Get("cumulativeGraph")

    processes = [
        "reducedTree" #,
        #"reducedTree_sig" #,
      #  "reducedTree_sig_2017" #,
      #  "reducedTree_data"
        ]

   # for i in range(2,15): #15 13+box
   #     processes.append("reducedTree_sig_node_"+str(i))

  #  for i in range(0,8):
 #   for i in range(0,5):
    for i in range(0,0):
  #      if i == 1: continue #gJets are combined in one, i==2
        processes.append("reducedTree_bkg_"+str(i))
      #  processes.append("reducedTree_bkg_"+str(i)+"_2017")



    fin = ROOT.TFile.Open(options.file)

    fTransformed = ROOT.TFile.Open(options.file.replace(".root","")+"_transformedMVA.root","recreate")


    for proc in processes:
        print proc
        tree = fin.Get(proc)
        chain = ROOT.TChain(tree.GetName())
    
        chain.Add(options.file)
        copyTree = chain.CopyTree("")
        copyTree.SetName(proc)
        copyTree.SetTitle(proc)

        transfMVA = array( 'f', [ 0. ] )
        transfBranch = copyTree.Branch("MVAOutputTransformed",transfMVA,"MVAOutputTransformed/F");
        lumi = array( 'f', [ 0. ] )
        lumiBranch = copyTree.Branch("lumi",lumi,"lumi/F");
        dummyList = []
        
        for i,event in enumerate(copyTree):
            if i>tree.GetEntries():break
           # mva = event.HHTagger2017
            mva = event.MVAOutput
           # mva = event.HHbbggMVA
            if '2016' in options.file:
                mva = mva/(mva*(1.-newWeight2016)+newWeight2016)
                transfMVA[0] = cumulativeGraph.Eval(mva)
                lumi[0] = lumi2016
            elif '2017' in options.file:
                transfMVA[0] = cumulativeGraph.Eval(mva)
                lumi[0] = lumi2017
            elif '2018' in options.file:
                mva = mva/(mva*(1.-newWeight2018)+newWeight2018)
                transfMVA[0] = cumulativeGraph.Eval(mva)
                lumi[0] = lumi2018
            transfBranch.Fill()
            lumiBranch.Fill()
    
    
    fTransformed.Write()
    fTransformed.Close()

        
if __name__ == "__main__":

    parser = OptionParser(option_list=[
            make_option("-i", "--infile",
                        action="store", type="string", dest="file",
                        default="",
                        help="input file",
                        ),
            make_option("-g", "--graphfile",
                        action="store", type="string", dest="graphfile",
                        default="",
                        help="graph file",
                        ),
            ]
                          )

    (options, args) = parser.parse_args()
    sys.argv.append("-b")

    
    pprint(options.__dict__)

    import ROOT
    
    main(options,args)
        
