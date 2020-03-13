import ROOT
from ROOT import TFile, TTree
from sklearn.externals import joblib
import numpy as np


tree_path = '/work/nchernya/HHbbgg_ETH_devel/outfiles/test/' 
tree_name = 'output_GluGluToHHTo2B2G_node_12_13TeV-madgraph_spigazzi-Era2016_RR-17Jul2018_v2-legacyRun2FullV1-v0-RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2-0f39adba5dbc548d611578513f3de618_USER_numEvent1000.root'
tree_dir = 'tagsDumper/trees/hh2016_13TeV_125_13TeV_DoubleHTag_0'
#tree_path = '/work/nchernya/HHbbgg_ETH_devel/root_files/ntuples_20192401/ntuples_2016_20192401/' 
#tree_name = 'output_hh_2016.root'
#tree_dir = 'tagsDumper/trees/hh2016_13TeV_125_13TeV_DoubleHTag_0'

file = TFile(tree_path+tree_name)
tree = file.Get(tree_dir)
entries = tree.GetEntriesFast()

reader = ROOT.TMVA.Reader()

import array

names = 'leadingJet_DeepFlavour,subleadingJet_DeepFlavour,absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,(leadingPhoton_pt/CMS_hgg_mass),(subleadingPhoton_pt/CMS_hgg_mass),(leadingJet_pt/Mjj),(subleadingJet_pt/Mjj),rho,(leadingJet_bRegNNResolution*1.4826),(subleadingJet_bRegNNResolution*1.4826),(sigmaMJets*1.4826),PhoJetMinDr,PhoJetOtherDr'.split(",")


var_list = []

for num,name in enumerate(names):
	var_list.append(array.array('f',[0])) ; reader.AddVariable(name,var_list[num])

reader.BookMVA("BDT","/work/nchernya/HHbbgg_ETH_devel/outfiles/test/training_with_18_12_2019_wo_Mjj_training0.weights.xml")
loaded_model = joblib.load('/work/nchernya/HHbbgg_ETH_devel/Training/output_files/training_with_18_12_2019_wo_Mjj_training0.pkl')
loaded_model._Booster.set_param('nthread', 10)
print loaded_model.get_booster().feature_names

#for entry in range(0,entries) :
for entry in range(0,1) :
	jentry = tree.LoadTree(entry)
	nb = tree.GetEntry(jentry)

	for num,name in enumerate(names):
		if ('subleadingJet_bRegNNResolution' in name): 
			var_list[num][0] =  getattr(tree, 'subleadingJet_bRegNNResolution')*1.4826
		elif ('leadingJet_bRegNNResolution' in name) :
			var_list[num][0] =  getattr(tree, 'leadingJet_bRegNNResolution')*1.4826
		elif ('sigmaMJets' in name):
			var_list[num][0] =  getattr(tree, 'sigmaMJets')*1.4826
		elif ('/' in name) :
			new_name = name[1:len(name)-1]
			var_list[num][0] =  getattr(tree, '%s'%new_name.split('/')[0])/getattr(tree, '%s'%new_name.split('/')[1])
		else :
			var_list[num][0] =  getattr(tree, '%s'%name)
	
	print 'Event number : ',tree.event	
#	print var_list
	sig_ar = [round(el[0],5) for el in var_list]
	print sig_ar
	Y_pred_sig = loaded_model.predict_proba(sig_ar)[:,loaded_model.n_classes_-1].astype(np.float64)
#	for num in range(0,len(names)):
#		print "('%s'"%names[num],":",var_list[num][0],"),",
	print 'evaluate : '
	bdtOutput = reader.EvaluateMulticlass("BDT")
	print bdtOutput[0],bdtOutput[1],bdtOutput[2]
	print Y_pred_sig




