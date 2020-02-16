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

    year = options.year
    files= os.listdir(options.indir)
    input_files = []
    print files
    for f in options.inp_proc.split(','):
       process  = [s for s in files if (f in s) and ('diffNaming' in s)]
       print process,f
       input_files.append(process[0].replace('_preselection_diffNaming.root','').replace('output_','')) 
    target_names = []
    for num,f in enumerate(input_files):
       p = (options.inp_proc.split(','))[num]
       print p
       if ('qqh' in p) or ('ggh' in p) or ('vh' in p) or ('tth' in p)  :
          target_names.append(p+'%s_13TeV_125_13TeV'%year)
       elif ('hh' in p)   :
          target_names.append('hh%s_13TeV_125_13TeV'%year)
       elif ('DoubleEG' in p)   :
          target_names.append('Data_13TeV')
       else :
          target_names.append(f.replace('-','_') +'_13TeV')
       input_files[num] =  f 

    for num,file in enumerate(input_files): 
        fin = ROOT.TFile.Open(options.indir+file+'_preselection_diffNaming.root')

        fTransformed = ROOT.TFile.Open(options.indir+file.replace(".root","")+"_transformedMVA.root","recreate")


        proc = target_names[num]+'_DoubleHTag_0'
        print proc
        tree = fin.Get(proc)
        copyTree = tree.CopyTree("")
        copyTree.SetName(proc)
        copyTree.SetTitle(proc)

        transfMVA = array( 'f', [ 0. ] )
        transfBranch = copyTree.Branch("MVAOutputTransformed",transfMVA,"MVAOutputTransformed/F");
        dummyList = []
      
        print tree.GetEntries(), copyTree.GetEntries() 

        loopTotal = 0
        nEntries = copyTree.GetEntries()
        for i in range(0, nEntries):
          copyTree.GetEntry(i)
          mva = copyTree.MVAOutput
          transfMVA[0] = cumulativeGraph.Eval(mva)
          transfBranch.Fill()
          loopTotal += 1
        print 'looped over ',loopTotal
    
    
        fTransformed.Write()
        fTransformed.Close()

        
if __name__ == "__main__":

    parser = OptionParser(option_list=[
            make_option("-i", "--indir",
                        action="store", type="string", dest="indir",
                        default="",
                        help="input file",
                        ),
            #make_option("--inp-proc",type='string',dest='inp_proc',default='DiPhotonJetsBox_,DiPhotonJetsBox1BJet,DiPhotonJetsBox2BJets,GJet_Pt-20to40_,GJet_Pt-40toInf_,ggh,vh,tth,qqh,hh,DoubleEG'), 
            #make_option("--inp-proc",type='string',dest='inp_proc',default='DiPhotonJetsBox_,DiPhotonJetsBox1BJet,DiPhotonJetsBox2BJets,GJet_Pt-20to40_,GJet_Pt-40toInf_,ggh,vh,tth,qqh,hh'), 
            make_option("--inp-proc",type='string',dest='inp_proc',default='ggh'), 
           # make_option("--inp-proc",type='string',dest='inp_proc',default='GJet_Pt-20to40_'), 
            #make_option("--inp-proc",type='string',dest='inp_proc',default='DoubleEG'), 
            make_option("-y","--year",type='string',dest='year',default='2016'), 
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
        
