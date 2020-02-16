import sys, types, os
from optparse import OptionParser, make_option
from  pprint import pprint
from array import array

# -----------------------------------------------------------------------------------------------------------
def main(options,args):

    lumi2016=35.92
    lumi2017=41.53
    lumi2018=59.74

    ## setTDRStyle()
    ROOT.gStyle.SetOptStat(0)
        
    fin = ROOT.TFile.Open(options.file)

    fin.cd()

    processes = [
        "reducedTree_sig",
        "reducedTree_bkg_DiPhotonJetsBox_",
			"reducedTree_bkg_DiPhotonJetsBox1BJet",
			"reducedTree_bkg_DiPhotonJetsBox2BJets",
			"reducedTree_bkg_GJet_Pt_20to40",
	 		"reducedTree_bkg_GJet_Pt_40toInf" ,
		   "reducedTree_bkg_tth"
	#		"reducedTree_bkg_TTGJets",
#			"reducedTree_bkg_TTTo2L2Nu",
#			"reducedTree_bkg_TTGG_0Jets"
        ]

  #  for i in range(2,14): #15 13+box
   #     processes.append("reducedTree_sig_node_"+str(i))

  #  for i in range(0,8):
  #  for i in range(0,5):
  #      if i == 1: continue #gJets are combined in one, i==2
  #      processes.append("reducedTree_bkg_"+str(i))



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

        lumi = array( 'f', [ 0. ] )
        lumiBranch = copyTree.Branch("lumi",lumi,"lumi/F");
        dummyList = []
        
        for i,event in enumerate(copyTree):
            if i>tree.GetEntries():break
            if '2016' in options.file:
                lumi[0] = lumi2016
            elif '2017' in options.file:
                lumi[0] = lumi2017
            elif '2018' in options.file:
                lumi[0] = lumi2018
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
            ]
                          )

    (options, args) = parser.parse_args()
    sys.argv.append("-b")

    
    pprint(options.__dict__)

    import ROOT
    
    main(options,args)
       
