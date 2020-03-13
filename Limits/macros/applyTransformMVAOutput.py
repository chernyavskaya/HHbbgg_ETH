import sys, types, os
from optparse import OptionParser, make_option
from  pprint import pprint
from array import array

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

### Reweight to match S/B for 2016 since 2016 is the best year. Take as bkg diphoton(cleaned from overlap)+diphoton+bjets. 
  #  newWeight2016 = 1.   
  #  newWeight2017 = 0.816
  #  newWeight2018 = 0.864  

    lumi2016=35.92
    lumi2017=41.53
    lumi2018=59.74
      

    ## setTDRStyle()
    ROOT.gStyle.SetOptStat(0)
        
    fin_graph = ROOT.TFile.Open(options.graphfile)
    cumulativeGraph = fin_graph.Get("cumulativeGraph")

    processes = [
        "reducedTree" ,
      #  "reducedTree_sig" #,
      #  "reducedTree_bkg_TTTo2L2Nu",
      #  "reducedTree_bkg_ttH",
      #  "reducedTree_bkg_TTGJets",
      #  "reducedTree_bkg_TTGG_0Jets",
      #  "reducedTree_bkg_GJet_Pt_40toInf",
      #  "reducedTree_bkg_GJet_Pt_20to40",
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
             #   mva = mva/(mva*(1.-newWeight2016)+newWeight2016)
                transfMVA[0] = cumulativeGraph.Eval(mva)
                lumi[0] = lumi2016
            elif '2017' in options.file:
                transfMVA[0] = cumulativeGraph.Eval(mva)
                lumi[0] = lumi2017
            elif '2018' in options.file:
              #  mva = mva/(mva*(1.-newWeight2018)+newWeight2018)
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
        
