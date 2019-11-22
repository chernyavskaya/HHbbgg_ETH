from optparse import OptionParser, make_option
from  pprint import pprint

import os
import sys; sys.path.append("/shome/nchernya/HHbbgg_ETH_devel/Training/python") # to load packages
import training_utils as utils
import numpy as np
import preprocessing_utils as preprocessing
import plotting_utils as plotting
import optimization_utils as optimization
import postprocessing_utils as postprocessing

import pandas as pd
import root_pandas as rpd
import json

treeDir = 'tagsDumper/trees/'
#samples = ["GluGluToHHTo2B2G","DiPhotonJetsBox_","DiPhotonJetsBox2BJets_","DiPhotonJetsBox1BJet_"]#
samples = ["GluGluToHHTo2B2G","DiPhotonJetsBox_","DiPhotonJetsBox2BJets_","DiPhotonJetsBox1BJet_","ttH"]#
#samples = ["GluGluToHHTo2B2G","ttH"]#
#samples = ["GluGluToHHTo2B2G","DiPhotonJetsBox_"]#
signal_name = "GluGluToHHTo2B2G"
cleanOverlap = True   # Do not forget to change it 
#treeTag="_2017"
treeTag=""

NodesNormalizationFile = '/work/nchernya/HHbbgg_ETH_devel/root_files/ntuples_20190209/reweighting_normalization_19_09_2019.json'
useMixOfNodes = True
#whichNodes = list(np.arange(0,12,1))   #all nodes are used to train. 
#whichNodes = [3,'box','SM'] #nodes similar to SM in shape of MX, used for categories optimization, considered as signal for the category optimization
whichNodes = ['SM']  #used to create cumulative on SM only
signalMixOfNodesNormalizations = json.loads(open(NodesNormalizationFile).read())

#just a list of all nodes to add weight branches in the trees
nodes_branches = list(np.arange(0,12,1))   #all nodes are used to train. 
nodes_branches.append('SM')
nodes_branches.append('box')

def addSamples():#define here the samples you want to process
    ntuples = options.ntup
    year = options.year
    if options.ldata is not "":
        print("loading files from: "+options.ldata)
        utils.IO.ldata=options.ldata
    
    files= os.listdir(utils.IO.ldata+ntuples)

   # for iSample in samples:
    for num,iSample in enumerate(samples):
        process  = [s for s in files if iSample in s]
        if (iSample == "GluGluToHHTo2B2G") and (useMixOfNodes==False):
            utils.IO.add_signal(ntuples,process,1,treeDir+signal_name+'_13TeV_DoubleHTag_0',year)
        elif (iSample == "GluGluToHHTo2B2G") and (useMixOfNodes==True) :
            utils.IO.use_signal_nodes(useMixOfNodes,whichNodes,signalMixOfNodesNormalizations)
            utils.IO.add_signal(ntuples,process,1,treeDir+signal_name+'_13TeV_DoubleHTag_0',year)
        else :
            print 'adding bkg with process num : ',process[0],"  ",-num
            utils.IO.add_background(ntuples,process,-num,treeDir+process[0][process[0].find('output_')+7:process[0].find('.root')].replace('-','_')+'_13TeV_DoubleHTag_0',year)  

    

    nBkg = len(utils.IO.backgroundName)
    print 'bkgs : ',utils.IO.backgroundName
 
    Data= [s for s in files if "DoubleEG" in s]
    #utils.IO.add_data(ntuples,Data,-10,'tree')
    dataTreeName = 'Data_13TeV_DoubleHTag_0'
    utils.IO.add_data(ntuples,Data,-10,treeDir+dataTreeName)
    
    #add all nodes : old, now we do reweiting inside
    nodes = []
    nodesTreeNames = []
    if options.addnodes:
        for i in range(2,14): #+ ['box']:
            nodes.append([s for s in files if "GluGluToHHTo2B2G_reweighted_node_"+str(i) in s])
            nodesTreeNames.append("GluGluToHHTo2B2G_node_"+str(i)+'_13TeV_madgraph_13TeV_DoubleHTag_0')
    if options.addrew:
        for i in range(2,14): #+ ['box']:                   
            nodes.append([s for s in files if "GluGluToHHTo2B2G_reweighted_nodes" in s])
            nodesTreeNames.append("GluGluToHHTo2B2G_reweighted_node_"+str(i))
    for i in range(nBkg,nBkg+len(nodes)):
        if "reweighted_nodes" not in  str(nodes[i-nBkg]):
            utils.IO.add_background(ntuples,nodes[i-nBkg],-i,treeDir+nodesTreeNames[i-nBkg])
        else:
            utils.IO.add_background(ntuples,nodes[i-nBkg],-i,nodesTreeNames[i-nBkg])

    for i in range(utils.IO.nBkg):        
        print "using background file n."+str(i)+": "+utils.IO.backgroundName[i]
    for i in range(utils.IO.nSig):    
        print "using signal file n."+str(i)+": "+utils.IO.signalName[i]
    print "using data file: "+ utils.IO.dataName[0]
    


def main(options,args):
    

    print options.addnodes
    addSamples()
    
    #branch_names = 'Mjj,leadingJet_DeepFlavour,subleadingJet_DeepFlavour,absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,PhoJetMinDr'.split(",") #set of variables March 2017 but regressed
    branch_names = 'leadingJet_DeepFlavour,subleadingJet_DeepFlavour,absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,PhoJetMinDr'.split(",") #set of variables March 2017 but regressed
    branch_names +=['rho']
    branch_names += 'noexpand:(leadingJet_bRegNNResolution*1.4826),noexpand:(subleadingJet_bRegNNResolution*1.4826),noexpand:(sigmaMJets*1.4826)'.split(",")
    additionalCut_names = 'CMS_hgg_mass,Mjj,MX,ttHScore'.split(',')
 #   additionalCut_names = 'CMS_hgg_mass,Mjj,MX'.split(',')
  #  if options.addHHTagger:
    additionalCut_names += 'HHbbggMVA'.split(",")
    signal_trainedOn = ['noexpand:(event%2!=0)']   #if 1 the event is trained on, if 0 -> should be used only for limit extraction
    bkg_trainedOn = ['noexpand:(event%1==0)'] #to accept all events
    overlap = ['overlapSave']
    if not options.addData:
        branch_cuts = 'leadingJet_pt,subleadingJet_pt,leadingJet_bRegNNCorr,subleadingJet_bRegNNCorr,noexpand:(leadingJet_pt/leadingJet_bRegNNCorr),noexpand:(subleadingJet_pt/subleadingJet_bRegNNCorr)'.split(',')
        event_branches = ['event','weight','leadingJet_hflav','leadingJet_pflav','subleadingJet_hflav','subleadingJet_pflav']
    else:
        branch_cuts = []
        event_branches = ['event','weight']
 #   cuts = 'leadingJet_pt>20 & subleadingJet_pt> 20 & (leadingJet_pt/leadingJet_bRegNNCorr>20) & (subleadingJet_pt/subleadingJet_bRegNNCorr>20) '
    if not options.addData:
        cuts = 'leadingJet_pt>0 '
    else:
        cuts = 'rho>0'#just because with data we don't save the raw pt (we should)  -->>What  ? (Nadya)
######################
################################################################


    branch_names = [c.strip() for c in branch_names]
    print "using following variables for MVA: " 
    print branch_names
    
    
    # no need to shuffle here, we just count events
    nodesWeightBranches=[]
    if utils.IO.signalMixOfNodes : nodesWeightBranches=[ 'benchmark_reweight_%s'%i for i in nodes_branches ] 
    preprocessing.set_signals(branch_names+branch_cuts+event_branches+additionalCut_names+signal_trainedOn+nodesWeightBranches,False,cuts) 
    preprocessing.set_backgrounds(branch_names+branch_cuts+event_branches+additionalCut_names+bkg_trainedOn,False,cuts) 
   # X_bkg,y_bkg,weights_bkg,X_sig,y_sig,weights_sig=preprocessing.set_variables(branch_names+['year'])  
    X_bkg,y_bkg,weights_bkg,X_sig,y_sig,weights_sig=preprocessing.set_variables(branch_names)  
 
    data_branches = ["HHbbggMVA","MX","ttHScore","Mjj","event","rho","weight","CMS_hgg_mass"]
    if options.addData:
       # preprocessing.set_data(branch_names+branch_cuts+event_branches,cuts)
       # X_data,y_data,weights_data = preprocessing.set_variables_data(branch_names)
        preprocessing.set_data(data_branches,cuts)
        X_data,y_data,weights_data = preprocessing.set_variables_data(data_branches)
        X_data,y_data,weights_data = preprocessing.clean_signal_events_single_dataset(X_data,y_data,weights_data)
    
    #bbggTrees have by default signal and CR events, let's be sure that we clean it
    if y_bkg.shape[1]==1 : 
        X_bkg,y_bkg,weights_bkg = preprocessing.clean_signal_events_single_dataset(X_bkg,y_bkg,weights_bkg)
        X_sig,y_sig,weights_sig = preprocessing.clean_signal_events_single_dataset(X_sig,y_sig,weights_sig)
    else : 
        X_bkg,y_bkg,weights_bkg,X_sig,y_sig,weights_sig=preprocessing.clean_signal_events(X_bkg,y_bkg,weights_bkg,X_sig,y_sig,weights_sig)
    
    
    # load the model from disk
    from sklearn.externals import joblib
    
    bkg = []
    for i in range(0,len(utils.IO.backgroundName)): 
        bkg.append(X_bkg[y_bkg ==utils.IO.bkgProc[i]])
        print utils.IO.backgroundName[i],'with proc num : ',utils.IO.bkgProc[i]
    
    print 'add Tagger' ,options.addHHTagger 
    #compute the MVA
    Y_pred_bkg = []
    if not options.addHHTagger:
        print 'Adding tagger output'
        loaded_model = joblib.load(os.path.expanduser(options.trainingDir+options.trainingVersion+'.pkl'))
        loaded_model._Booster.set_param('nthread', 10)
        print "loading"+options.trainingDir+options.trainingVersion+'.pkl'
#        print(loaded_model.get_xgb_params)
        if options.addData:
            Y_pred_data = loaded_model.predict_proba(X_data)[:,loaded_model.n_classes_-1].astype(np.float64)
            #print Y_pred_data 
        #for i in range(0,len(utils.IO.backgroundName)):  
        for i in range(0,0):   #not to apply MVA on bkg
            print 'evaluating MVA for bkg : ',str(i)
            Y_pred_bkg.append(loaded_model.predict_proba(bkg[i])[:,loaded_model.n_classes_-1].astype(np.float64))
        Y_pred_sig = loaded_model.predict_proba(X_sig)[:,loaded_model.n_classes_-1].astype(np.float64)
    
    
    
    #define MVA cut and additional variables needed
   # additionalCut_names = 'noexpand:diphotonCandidate.M(),noexpand:dijetCandidate.M(),MX,isSignal,event,noexpand:dijetCandidateCorr.M(),noexpand:(event%2!=0),subleadingJet_genHadronFlavourb,leadingJet_genHadronFlavourb'.split(",")
  #  additionalCut_names = 'CMS_hgg_mass,Mjj,noexpand:(event%2!=0),noexpand:(event%5!=0)'.split(',')
  #  additionalCut_names = 'CMS_hgg_mass,Mjj,MX'.split(',')
    #mva output
    outTag = options.outTag
   # outDir=os.path.expanduser("/t3home/micheli/HHbbgg_ETH_20190128/HHbbgg_ETH/Training/output_files/"+outTag)
    outDir=os.path.expanduser("/shome/nchernya/HHbbgg_ETH_devel/outfiles/"+outTag)
    if not os.path.exists(outDir):
        os.mkdir(outDir)
    
    branch_names+=branch_cuts
    branch_names+=event_branches
   

###########################  data  block starts  ################################################################ 
    if options.addData:   
      #  data_count_df = (rpd.read_root(utils.IO.dataName[0],utils.IO.dataTreeName[0], columns = branch_names+additionalCut_names+bkg_trainedOn)).query(cuts)
      #  nTot,dictVar = postprocessing.stackFeatures(data_count_df,branch_names+additionalCut_names,isData=1)
        data_count_df = (rpd.read_root(utils.IO.dataName[0],utils.IO.dataTreeName[0], columns = data_branches)).query(cuts)
        nTot,dictVar = postprocessing.stackFeatures(data_count_df,data_branches,isData=1)
    #apply isSignal cleaning
        nCleaned = nTot[np.where(nTot[:,dictVar['weight']]!=0),:][0]
        print "nCleaned"
        print nCleaned.shape
  
  #save preselection data
        processPath=os.path.expanduser(options.outputFileDir)+outTag+'/'+utils.IO.dataName[0].split("/")[len(utils.IO.dataName[0].split("/"))-1].replace("output_","").replace(".root","")+"_preselection"+".root"
        if not options.addHHTagger:        
            postprocessing.saveTree(processPath,dictVar,nCleaned,Y_pred_data)
        else:
            postprocessing.saveTree(processPath,dictVar,nCleaned)
 
        processPath=os.path.expanduser(options.outputFileDir)+outTag+'/'+utils.IO.dataName[0].split("/")[len(utils.IO.dataName[0].split("/"))-1].replace("output_","").replace(".root","")+"_preselection_diffNaming"+".root"
        if not options.addHHTagger:        
            postprocessing.saveTree(processPath,dictVar,nCleaned,Y_pred_data,nameTree="reducedTree_data%s"%treeTag)
        else:
            postprocessing.saveTree(processPath,dictVar,nCleaned,nameTree="reducedTree_data%s"%treeTag)
###########################   data  block  ends  ##############################################################

 
###########################  signal  block starts  ################################################################ 
    sig_count_df = utils.IO.signal_df[0]
    preprocessing.define_process_weight(sig_count_df,utils.IO.sigProc[0],utils.IO.signalName[0],utils.IO.signalTreeName[0],cleanSignal=True,cleanOverlap=cleanOverlap)

 
    #nTot is a multidim vector with all additional variables, dictVar is a dictionary associating a name of the variable
    #to a position in the vector
    nTot,dictVar = postprocessing.stackFeatures(sig_count_df,branch_names+additionalCut_names+signal_trainedOn+overlap+nodesWeightBranches)
    #apply isSignal cleaning
 #   nCleaned = nTot[np.where(nTot[:,dictVar['weight']]!=0),:][0]
    nCleaned = nTot 
    
    processPath=os.path.expanduser(options.outputFileDir)+outTag+'/'+utils.IO.signalName[0].split("/")[len(utils.IO.signalName[0].split("/"))-1].replace("output_","").replace(".root","")+"_preselection"+".root"


    if not options.addHHTagger:
        postprocessing.saveTree(processPath,dictVar,nCleaned,Y_pred_sig)
    else:
        postprocessing.saveTree(processPath,dictVar,nCleaned)        
    
    processPath=os.path.expanduser(options.outputFileDir)+outTag+'/'+utils.IO.signalName[0].split("/")[len(utils.IO.signalName[0].split("/"))-1].replace("output_","").replace(".root","")+"_preselection_diffNaming"+".root"

    if not options.addHHTagger:
        postprocessing.saveTree(processPath,dictVar,nCleaned,Y_pred_sig,nameTree="reducedTree_sig%s"%treeTag)
    else:    
        postprocessing.saveTree(processPath,dictVar,nCleaned,nameTree="reducedTree_sig%s"%treeTag)
   
###########################  signal  block ends  ################################################################ 
    
   # for iProcess in range(0,len(utils.IO.backgroundName)):
    for iProcess in range(0,0):  #not to run on bkg
        
        print "Processing sample: "+str(iProcess)
        bkg_count_df = utils.IO.background_df[iProcess]
        preprocessing.define_process_weight(bkg_count_df,utils.IO.bkgProc[iProcess],utils.IO.backgroundName[iProcess],utils.IO.bkgTreeName[iProcess],cleanSignal=True,cleanOverlap=cleanOverlap)
    
        crazySF=1.
        nTot,dictVar = postprocessing.stackFeatures(bkg_count_df,branch_names+additionalCut_names+bkg_trainedOn+overlap,SF=crazySF)
        nCleaned = nTot
        print "nCleaned"
        print nCleaned.shape
    
        bkgName_idx = len(samples)-1  #how many bkg we have
        print 'bkg Index : ',bkgName_idx 
        print 'predictd bkg len and size of each bkg sample: ',len(Y_pred_bkg),Y_pred_bkg

        processPath=os.path.expanduser(options.outputFileDir)+outTag+'/'+utils.IO.backgroundName[iProcess].split("/")[len(utils.IO.backgroundName[iProcess].split("/"))-1].replace("output_","").replace(".root","")+"_preselection"+".root"
        if not options.addHHTagger:
            postprocessing.saveTree(processPath,dictVar,nCleaned,Y_pred_bkg[iProcess])
        else:
            postprocessing.saveTree(processPath,dictVar,nCleaned)
        
        processPath=os.path.expanduser(options.outputFileDir)+outTag+'/'+utils.IO.backgroundName[iProcess].split("/")[len(utils.IO.backgroundName[iProcess].split("/"))-1].replace("output_","").replace(".root","")+"_preselection_diffNaming"+".root"
        if options.addrew and "reweighted_nodes"in processPath:
            processPath = processPath.replace("reweighted_nodes_","reweighted_node_"+str(iProcess-(len(samples)-3)))
        if "GluGluToHHTo2B2G_reweighted_node"in processPath and options.addrew:
         #   treeName = "reducedTree_sig_node_"+str(iProcess-7)
            treeName = "reducedTree_sig_node_"+str(iProcess-(bkgName_idx))+treeTag
        else:
            treeName = "reducedTree_bkg_"+str(iProcess)+treeTag

        if not options.addHHTagger:        
            postprocessing.saveTree(processPath,dictVar,nCleaned,Y_pred_bkg[iProcess],nameTree=treeName)
        else:
            postprocessing.saveTree(processPath,dictVar,nCleaned,nameTree=treeName)    
    
    
    os.system('hadd '+ os.path.expanduser(options.outputFileDir)+outTag+'/'+'Total_preselection_diffNaming.root '+ os.path.expanduser(options.outputFileDir)+outTag+'/'+'*diffNaming.root')

    


if __name__ == "__main__":

    parser = OptionParser(option_list=[
            make_option("-n", "--ntuples",
                        action="store", type="string", dest="ntup",
                        default="20170620",
                        help="ntuples location",
                        ),
            make_option("-a","--addMVAOutput",
                        action="store_true",dest="addHHTagger",default=False,
                        help="add MVAOutput to outTree",
                        ),
            make_option("-t","--training",
                        action="store", type="string",dest="trainingVersion",
                        default="allMC_resWeighting_F_noDR_minDRGJet",
                        help="MVA version to apply",
                        ),
            make_option("-x","--trainingDir",
                        action="store",type="string",dest="trainingDir",default="/work/nchernya/HHbbgg_ETH_devel/Training/output_files/",
                        help="directory from where to load pklfile",
                        ),
            make_option("-o", "--out",
                        action="store", type="string", dest="outTag",
                        default="20180108_test",
                        help="output folder name",
                        ),
            make_option("-k","--nodes",
                        action="store_false",dest="addnodes",default=False,
                        help="add or not nodes",
                        ),
            make_option("-w","--reweightednodes",
                        action="store_true",dest="addrew",default=False,
                        help="add or not reweighted nodes",
                        ),
            make_option("-y","--year",
                        action="store",type=int,dest="year",default=0,
                        help="which year : 2016-0,2017-1,2018-2",
                        ),
            make_option("-l","--ldata",
                        action="store",type="string",dest="ldata",default="",
                        help="directory from where to load data (if different from default one)",
                        ),
            make_option("-d","--adddata",
                        action="store_true",dest="addData",default=False,
                        help="decide if you want to process or not data",
                        ),
            make_option("-f","--outputFileDir",
                        action="store",type="string",dest="outputFileDir",default="/shome/nchernya/HHbbgg_ETH_devel/outfiles/",
                        help="directory where to save output trees",
                        ),
            ]
                          )

    (options, args) = parser.parse_args()
    sys.argv.append("-b")

    
    pprint(options.__dict__)

    import ROOT
    
    main(options,args)
        
