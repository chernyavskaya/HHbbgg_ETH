#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import sys; sys.path.append("~/HHbbgg_ETH_devel/Training/python") # to load packages
import training_utils as utils
import numpy as np
reload(utils)
import preprocessing_utils_VBFHH as preprocessing
reload(preprocessing)
import plotting_utils as plotting
reload(plotting)
import optimization_utils as optimization
reload(optimization)
import postprocessing_utils as postprocessing
reload(postprocessing)
import pandas as pd
import root_pandas as rpd
import matplotlib.pyplot as plt
import json
import copy
from ROOT import TLorentzVector
import uproot


# In[ ]:


year='FullRunII'

training = 'lt' #greater or less than
 
indir='/work/nchernya/HHbbgg_ETH_devel/root_files/soumya_MX500_training/'

#file_in = 'Total_preselection_diffNaming_transformedMVA_MX_%s_500_ttH_0p26.root'%training
#file_in = 'Total_preselection_diffNaming_transformedMVA_MX_C2V0_ttH_0p26.root'
file_in = 'Total_preselection_diffNaming_transformedMVA_qqHH_doublecat_MX_%s_500_14_05_2020.root'%training
#file_in = 'Total_preselection_diffNaming_transformedMVA_14_05_2020.root'

process_VBFHH = 'reducedTree_sig'
#process_ggHH_LO ='reducedTree_bkg_GluGluToHHTo2B2G_node_all'# reducedTree_bkg_hh_LO'
process_ggHH_LO ='reducedTree_bkg_hh_LO'
process_diphoton = 'reducedTree_bkg_DiPhotonJetsBox_'
process_diphoton1b = 'reducedTree_bkg_DiPhotonJetsBox1BJet_'
process_diphoton2b = 'reducedTree_bkg_DiPhotonJetsBox2BJets_'


cuts='(ttHScore>0.26)'

features='weight,ttHScore,CMS_hgg_mass,MX,Mjj,event,lumi,overlapSave,MVAOutput,MVAOutputTransformed'.split(',')
out_dir = indir+'plots_MVAprob_%s_500/'%training

df_VBFHH = load_data_rpd(indir+file_in, features, process_VBFHH,'',cuts) 
df_ggHH_LO = load_data_rpd(indir+file_in, features, process_ggHH_LO,'',cuts) 
df_diphoton = load_data_rpd(indir+file_in, features, process_diphoton,'',cuts) 
df_diphoton1b = load_data_rpd(indir+file_in, features, process_diphoton1b,'',cuts) 
df_diphoton2b = load_data_rpd(indir+file_in, features, process_diphoton2b,'',cuts) 

utils.IO.plotFolder = indir


# In[ ]:


df_VBFHH['weight'] = df_VBFHH['weight']*df_VBFHH['lumi']*0.5
df_ggHH_LO['weight'] = df_ggHH_LO['weight']*df_ggHH_LO['lumi']*0.008
df_diphoton['weight'] = df_diphoton['weight']*df_diphoton['lumi']*2.9
df_diphoton1b['weight'] = df_diphoton1b['weight']*df_diphoton1b['lumi']*2.9
df_diphoton2b['weight'] = df_diphoton2b['weight']*df_diphoton2b['lumi']*2.9
#df_tth['weight'] = df_tth['weight']*df_tth['lumi']

df_diphoton['weight'] = df_diphoton['weight']*df_diphoton['overlapSave']
df_diphoton = pd.concat([df_diphoton,df_diphoton1b,df_diphoton2b],ignore_index=True)


# In[ ]:


Y_pred_sig_train = df_VBFHH.query('event%2==0')['MVAOutput']
weights_sig_train = df_VBFHH.query('event%2==0')['weight']
Y_pred_bkg_train = df_diphoton.query('event%2==0')['MVAOutput']
weights_bkg_train = df_diphoton.query('event%2==0')['weight']
Y_pred_sig_test = df_VBFHH.query('event%2!=0')['MVAOutput']
weights_sig_test = df_VBFHH.query('event%2!=0')['weight']
Y_pred_bkg_test =  df_diphoton.query('event%2!=0')['MVAOutput']
weights_bkg_test =  df_diphoton.query('event%2!=0')['weight']
outstr='DiPhoton'
plot_classifier = plotting.plot_classifier_output_on_top(Y_pred_sig_train,Y_pred_bkg_train,Y_pred_sig_test,Y_pred_bkg_test,weights_sig_train,weights_bkg_train,weights_sig_test,weights_bkg_test,outString=outstr)


# In[ ]:


Y_pred_bkg_train = df_ggHH_LO.query('event%2==0')['MVAOutput']
weights_bkg_train = df_ggHH_LO.query('event%2==0')['weight']
Y_pred_bkg_test =  df_ggHH_LO.query('event%2!=0')['MVAOutput']
weights_bkg_test =  df_ggHH_LO.query('event%2!=0')['weight']
outstr='ggHH'
plot_classifier_gghh = plotting.plot_classifier_output_on_top(Y_pred_sig_train,Y_pred_bkg_train,Y_pred_sig_test,Y_pred_bkg_test,weights_sig_train,weights_bkg_train,weights_sig_test,weights_bkg_test,outString=outstr) 

