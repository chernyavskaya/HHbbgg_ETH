import sys, types, os
from optparse import OptionParser, make_option
from  pprint import pprint
from array import array

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

   # newWeight = 1.011026
    newWeight = 1.02309  ## (0.398279/1852.6094)*(1./(0.412699/1964.0142))  #with reweighted to SM  

    ## setTDRStyle()
    ROOT.gStyle.SetOptStat(0)
        
    fin_graph = ROOT.TFile.Open(options.graphfile)
    cumulativeGraph = fin_graph.Get("cumulativeGraph")

    processes = [
      #  "reducedTree" #,
      #  "reducedTree_sig" #,
        "reducedTree_sig_2017" #,
      #  "reducedTree_data"
        ]

   # for i in range(2,15): #15 13+box
   #     processes.append("reducedTree_sig_node_"+str(i))

  #  for i in range(0,8):
 #   for i in range(0,5):
    for i in range(0,1):
  #      if i == 1: continue #gJets are combined in one, i==2
      #  processes.append("reducedTree_bkg_"+str(i))
        processes.append("reducedTree_bkg_"+str(i)+"_2017")



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
        dummyList = []
        
        for i,event in enumerate(copyTree):
            if i>tree.GetEntries():break
           # mva = event.HHTagger2017
            mva = event.MVAOutput
           # mva = event.HHbbggMVA
            if '2017' in options.file:
                mva = mva/(mva*(1.-newWeight)+newWeight)
                transfMVA[0] = cumulativeGraph.Eval(mva)
            else :
                transfMVA[0] = cumulativeGraph.Eval(mva)
            transfBranch.Fill()
    
    
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
        
