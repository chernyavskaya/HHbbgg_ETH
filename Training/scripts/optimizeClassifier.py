# coding: utf-8

import os
#import sys; sys.path.append("/t3home/micheli/HHbbgg_ETH_20190128/HHbbgg_ETH/Training/python") # to load packages
import sys; sys.path.append("~/HHbbgg_ETH_devel/Training/python") # to load packages
import training_utils as utils
reload(utils)
import preprocessing_utils as preprocessing
reload(preprocessing)
import optimization_utils as optimization
reload(optimization)
import numpy as np
import time
import datetime
start_time = time.time()

import commands

now = str(datetime.datetime.now()).split(' ')[0]
print(now)
outstr = now+"20190201_test50iter"
#outputFolder = '/t3home/micheli/HHbbgg_ETH_20190128/HHbbgg_ETH/Training/output_files/%s/'%outstr
outputFolder = '/shome/nchernya/HHbbgg_ETH_devel/Training/output_files/%s/'%outstr
if not os.path.exists(outputFolder):
    print outputFolder, "doesn't exist, creating it..."
    os.makedirs(outputFolder)


year=0
dirs = ['ntuples_2016_20181210','ntuples_2017_20181210']
ntuples = dirs[year]
get_ipython().magic(u'env data=$utils.IO.ldata$ntuples')
status,files = commands.getstatusoutput('! ls $data | sort -t_ -k 3 -n')

files=files.split('\n')

print("files:")
print(type(files))

if (year==0) : signal = [s for s in files if "SM_plus_reweighted_nodes_" in s ]
else : signal = [s for s in files if "SM_plus_nodes_" in s ]
diphotonJets = [s for s in files if "DiPhotonJetsBox_" in s]
#diphotonJets_1B = [s for s in files if "DiPhotonJetsBox1B" in s] # will use for limits
#diphotonJets_2B = [s for s in files if "DiPhotonJetsBox2B" in s] # will use for limits
gJets_lowPt = [s for s in files if "GJet_Pt-20to40" in s]
gJets_highPt = [s for s in files if "GJet_Pt-40" in s]

print signal
print("dipho")
print diphotonJets

utils.IO.add_signal(ntuples,signal,1,'nodesCombined',year)
#background should be merged in one class since it doesn't support multiclass optimization
utils.IO.add_background(ntuples,diphotonJets,-1,'tagsDumper/trees/'+diphotonJets[0][diphotonJets[0].find('output_')+7:diphotonJets[0].find('.root')].replace('-','_')+'_13TeV_DoubleHTag_0',year)
utils.IO.add_background(ntuples,gJets_lowPt,-1,'tagsDumper/trees/'+gJets_lowPt[0][gJets_lowPt[0].find('output_')+7:gJets_lowPt[0].find('.root')].replace('-','_')+'_13TeV_DoubleHTag_0',year)                            
utils.IO.add_background(ntuples,gJets_highPt,-1,'tagsDumper/trees/'+gJets_highPt[0][gJets_highPt[0].find('output_')+7:gJets_highPt[0].find('.root')].replace('-','_')+'_13TeV_DoubleHTag_0',year)                           


for i in range(len(utils.IO.backgroundName)):        
    print "using background file n."+str(i)+": "+utils.IO.backgroundName[i]
for i in range(len(utils.IO.signalName)):    
    print "using signal file n."+str(i)+": "+utils.IO.signalName[i]


random_seed = 555


# In[10]:

#use noexpand for root expressions, it needs this file https://github.com/ibab/root_pandas/blob/master/root_pandas/readwrite.py
#branch_names = 'leadingJet_bDis,subleadingJet_bDis,noexpand:fabs(CosThetaStar_CS),noexpand:fabs(CosTheta_bb),noexpand:fabs(CosTheta_gg),noexpand:diphotonCandidate.Pt()/diHiggsCandidate.M(),noexpand:dijetCandidate.Pt()/diHiggsCandidate.M(),customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverMDecorr,DiJetDiPho_DR'.split(",")
#branch_names = 'leadingJet_bDis,subleadingJet_bDis,noexpand:fabs(CosThetaStar_CS),noexpand:fabs(CosTheta_bb),noexpand:fabs(CosTheta_gg),noexpand:diphotonCandidate.Pt()/diHiggsCandidate.M(),noexpand:dijetCandidate.Pt()/diHiggsCandidate.M()'.split(",")
branch_names = 'leadingJetCorr_bDis,subleadingJetCorr_bDis,noexpand:fabs(CosThetaStar_CS),noexpand:fabs(CosTheta_bb),noexpand:fabs(CosTheta_gg),noexpand:diphotonCandidate.Pt()/diHiggsCandidateCorr.M(),noexpand:dijetCandidateCorr.Pt()/diHiggsCandidateCorr.M(),customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,PhoJetMinDr'.split(",") #set of variables March 2017 but regressed
b_reg_branches = 'leadingJet_bRegNNResolution,subleadingJet_bRegNNResolution,dijetSigmaMOverM'.split(",")
branch_names = branch_names+b_reg_branches
resolution_weighting = 'ggbb' # None, gg or ggbb
branch_names = [c.strip() for c in branch_names]
print branch_names

import pandas as pd
import root_pandas as rpd

#utils.IO.get_cross_sections('jsons/datasets80X_Moriond.json')
#utils.IO.w_sig.append(utils.IO.get_weight('signal','nrSM',0))
#utils.IO.w_bkg(utils.IO.get_weight('background','DiPhoJets',0))
#utils.IO.w_bkg(utils.IO.get_weight('background','GJets',0))
#utils.IO.w_bkg(utils.IO.get_weight('background','GJets',1))
from ROOT import TLorentzVector

#use noexpand for root expressions, it needs this file https://github.com/ibab/root_pandas/blob/master/root_pandas/readwrite.py
########################new code branches############################
#branch_names = 'leadingJet_bDis,subleadingJet_bDis,absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverMDecorr,PhoJetMinDr'.split(",") #set of variables March 2017 but regressed

#fra: adding Mjj to the training
branch_names = 'Mjj,leadingJet_DeepCSV,subleadingJet_DeepCSV,absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,PhoJetMinDr'.split(",") #set of variables March 2017 but regressed
b_reg_branches = 'noexpand:(leadingJet_bRegNNResolution*1.4826),noexpand:(subleadingJet_bRegNNResolution*1.4826),noexpand:(sigmaMJets*1.4826)'.split(",")
branch_cuts = 'leadingJet_pt,subleadingJet_pt,leadingJet_bRegNNCorr,subleadingJet_bRegNNCorr,noexpand:(leadingJet_pt/leadingJet_bRegNNCorr),noexpand:(subleadingJet_pt/subleadingJet_bRegNNCorr)'.split(',')
cuts = 'leadingJet_pt>0'
#cuts = 'subleadingJet_pt>25'
######################

#event_branches = ['event','sigmaMOverM','noexpand:(dijetSigmaMOverM*1.4826)']
event_branches = ['event','weight','MX','leadingJet_hflav','leadingJet_pflav','subleadingJet_hflav','subleadingJet_pflav']

branch_names = branch_names + ['rho']
branch_names = branch_names+b_reg_branches
resolution_weighting = 'ggbb' # None, gg or ggbb
doOverlapRemoval=False   #diphotons overlap removal if using b-enriched samples


branch_names = [c.strip() for c in branch_names]
print branch_names

event_bkg,event_sig = None,None
if (year==1 and doReweight2017 == True):
    preprocessing.set_signals(branch_names+event_branches+branch_cuts+['genMhh'],True,cuts)
    preprocessing.set_backgrounds(branch_names+event_branches+branch_cuts,True,cuts)
else :
    preprocessing.set_signals_and_backgrounds(branch_names+event_branches+branch_cuts,True,cuts)


if 'gg' in resolution_weighting : 
    preprocessing.weight_signal_with_resolution_all(branch='sigmaMOverM')
if 'bb' in resolution_weighting : 
    preprocessing.weight_signal_with_resolution_all(branch='(sigmaMJets*1.4826)')

if doOverlapRemoval == True:    
    for i in range(utils.IO.nBkg):
        if 'DiPhotonJetsBox_MGG' in utils.IO.bkgTreeName[i] : preprocessing.cleanOverlapDiphotons(utils.IO.bkgTreeName[i],utils.IO.background_df[i])        

if (year==1 and doReweight2017 == True):
    preprocessing.reweight_gen_mhh('mhh',genFrame2016,genFrame2017,utils.IO.signal_df[0],'genMhh')
                    
        
X_bkg,y_bkg,weights_bkg,event_bkg,X_sig,y_sig,weights_sig,event_sig=preprocessing.set_variables(branch_names,use_event_num=True)

#utils.IO.plotFolder = '/t3home/micheli/HHbbgg_ETH_20190128/HHbbgg_ETH/Training/plots/%s/'%outstr
#utils.IO.plotFolder = '/t3home/micheli/HHbbgg_ETH_20190128/HHbbgg_ETH/Training/output_files/%s'%outstr
utils.IO.plotFolder = '/shome/nchernya/HHbbgg_ETH_devel/outfiles/%s'%outstr
info_file = open(utils.IO.plotFolder+"info_%s.txt"%outstr,"w") 
info_file.write("\n".join(branch_names))
info_file.write("Resolution weighting : %s\n"%resolution_weighting)
info_file.write("Cuts : %s\n"%cuts)
info_file.close()



X_bkg,y_bkg,weights_bkg,event_bkg = preprocessing.randomize(X_bkg,y_bkg,weights_bkg,event_num = np.asarray(event_bkg))
X_sig,y_sig,weights_sig,event_sig = preprocessing.randomize(X_sig,y_sig,weights_sig,event_num = np.asarray(event_sig))


#Get training and test samples based on event number : even/odd or set in the function for now
y_total_train = preprocessing.get_total_training_sample_event_num(y_sig.reshape(-1,1),y_bkg,event_sig.reshape(-1,1),event_bkg).ravel()
X_total_train = preprocessing.get_total_training_sample_event_num(X_sig,X_bkg,event_sig.reshape(-1,),event_bkg.reshape(-1,))

y_total_test = preprocessing.get_total_test_sample_event_num(y_sig.reshape(-1,1),y_bkg,event_sig.reshape(-1,1),event_bkg).ravel()
X_total_test = preprocessing.get_total_test_sample_event_num(X_sig,X_bkg,event_sig.reshape(-1,),event_bkg.reshape(-1,))

w_total_train = preprocessing.get_total_training_sample_event_num(weights_sig.reshape(-1,1),weights_bkg.reshape(-1,1),event_sig.reshape(-1,1),event_bkg).ravel()
w_total_test = preprocessing.get_total_test_sample_event_num(weights_sig.reshape(-1,1),weights_bkg.reshape(-1,1),event_sig.reshape(-1,1),event_bkg).ravel()


##########Normalize weights for training and testing. Sum(signal)=Sum(bkg)=1. But keep relative normalization
# between bkg classes
w_total_train = preprocessing.normalize_process_weights_split_all(w_total_train,y_total_train)
w_total_test = preprocessing.normalize_process_weights_split_all(w_total_test,y_total_test)


# In[11]:
from sklearn.externals import joblib

import xgboost as xgb
clf = xgb.XGBClassifier(base_score=0.5, colsample_bylevel=1, colsample_bytree=1,
       gamma=0, learning_rate=0.1, max_delta_step=0, max_depth=5,
					min_child_weight=1e-05, missing=None, n_estimators=1500, nthread=9,#4 the same as in the engine scipt smp 4
       objective='binary:logistic', reg_alpha=0, reg_lambda=0.1,
       scale_pos_weight=1, seed=0, silent=True, subsample=1)


# In[27]:

reload(utils)
param_grid = {'n_estimators': [500,1000,1500,2000],
              'max_depth': [3,5, 10,15], 
              'gamma' : [0,0.15,0.3], 
              'learning_rate': [0.01,0.1, 0.2,0.3],    
              'reg_alpha':[0., 0.01, 0.1],
              'reg_lambda':[1e-2, 5e-2, 0.1, 0.3],
              'min_child_weight':[1e-06,1e-05,1e-04]
              }
#for a small test
#param_grid = {'n_estimators': [500],
 #             'max_depth': [3,5],
#}


#optimization.setupJoblib("gcc49_5gb_smp1_all") # create all.q (> 6 hours) with  1 cpu core. 50 jobs, but wait for them to run

clf = optimization.optimize_parameters_randomizedCV(clf,X_total_train,y_total_train,param_grid,cvOpt=3,nIter=50,nJobs=21,weights=w_total_train)
#clf = optimization.optimize_parameters_randomizedCV(clf,X_total_train,y_total_train,param_grid,cvOpt=5,nIter=50,nJobs=1,weights=w_total_train) #local
joblib.dump(clf, os.path.expanduser(outputFolder+'optimizedTraining_'+outstr+'.pkl'), compress=9)

writeInFile=outputFolder+'best_parameters_%s.txt'%outstr
if writeInFile!=None:
    print writeInFile
    outFile = open(writeInFile,"w")
    outFile.write("Best parameter set found on development set:\n")
    outFile.write("%s\n"%clf.best_estimator_)
    outFile.write("Grid scores on a subset of the development set:\n")   
    for params, mean_score, scores in clf.grid_scores_:
        print "%0.4f (+/-%0.04f) for %r"%(mean_score, scores.std(), params)
        outFile.write("%0.4f (+/-%0.04f) for %r"%(mean_score, scores.std(), params))   
    outFile.close() 

print 'It took', time.time()-start_time, 'seconds.'



