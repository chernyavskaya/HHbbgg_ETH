# # Characterize FFWD NN output
#load libs
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
import json
from optparse import OptionParser, make_option
#sys.path.insert(0, '/users/nchernya/HHbbgg_ETH/bregression/python/')
import plotting_utils as plotting
import pprint
import matplotlib.offsetbox as offsetbox 
import numpy as np

parser = OptionParser(option_list=[
    make_option("--training",type='string',dest="training",default='2018-02-03_17_57_53_job'),
    make_option("--njobs",type='int',dest="njobs",default=0),
    make_option("--inp-dir",type='string',dest="inp_dir",default='/work/nchernya/HHbbgg_ETH_devel/bregression/output_files/NN_psi_training/'),
    make_option("--inp-file",type='string',dest='inp_file',default='metrics'),
    #make_option("--out-dir",type='string',dest="out_dir",default='/users/nchernya//HHbbgg_ETH/bregression/plots/NN_epochs/'),
    make_option("--out-dir",type='string',dest="out_dir",default='/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/noJEC/March6/'), 
    make_option("--metrics",type='string',dest="metrics",default='loss,mae0,mse0'),
    make_option("--nxval",type='int',dest="nxval",default=1),
])

colors=['r','b','g','k','c','y']
## parse options
(options, args) = parser.parse_args()
input_trainings = options.training.split(',')
input_metrics = options.metrics.split(',')

nxval=options.nxval

#for each metric we plot it for train and validation sample vs epoch 
dictVar={}
all_means=[]
all_stds=[]
param_dicts=[]
for idx_nn,nn in enumerate(input_trainings): 
    j = json.load(open('%s/%s/config.json'%(options.inp_dir,nn)))
    param_dicts.append(dict(lr=j['model_params']['optimizer_params']['lr'],dropout=j['model_params']['dropout'],architecture=j['model_params']['layers'],loss=j['model_params']['loss']))
    data_frames=[]
    for xval in range(0,nxval):
       # load data from metrics.csv file
        if nxval>1 : tmp_data = pd.read_csv('%s/%s/%s_kfold%i.csv'%(options.inp_dir,nn,options.inp_file,xval))
        else : tmp_data = pd.read_csv('%s/%s/%s_kfold-1.csv'%(options.inp_dir,nn,options.inp_file))
        data_frames.append(tmp_data)
    if idx_nn==0 :  
        for i,column in enumerate(data_frames[0].columns.values.tolist()):
            dictVar[column] = i
    mean = np.mean( np.array( [ data_frames[i].as_matrix() for i in range(0,nxval)] ), axis=0 )
    mean2 = np.mean( np.array( [ data_frames[i].as_matrix() for i in range(0,nxval)] )**2, axis=0 )
    std = np.sqrt(mean2 - mean**2)
    all_means.append(mean)
    all_stds.append(std)
    #plot results
for idx,met in enumerate(input_metrics):
    for idx_nn,nn in enumerate(input_trainings): 
        mean = all_means[idx_nn]
        std = all_stds[idx_nn]
        plt.plot(mean[:,dictVar['epoch']],mean[:,dictVar['%s'%met]],linestyle='-',label='Training %s'%nn,color=colors[idx_nn])
     #   plt.scatter(mean[:,dictVar['epoch']],mean[:,dictVar['val_%s'%met]],color=colors[idx_nn])
      #  plt.fill_between(mean[:,dictVar['epoch']],mean[:,dictVar['val_%s'%met]]-std[:,dictVar['val_%s'%met]],mean[:,dictVar['val_%s'%met]]+std[:,dictVar['val_%s'%met]],alpha=0.2,color=colors[idx_nn])
        dataframe = pd.DataFrame()
        dataframe['mean_%i'%idx_nn] = mean[:,dictVar['val_%s'%met]]
        rolling_mean = dataframe['mean_%i'%idx_nn].rolling(window=5).mean()
        rolling_std = dataframe['mean_%i'%idx_nn].rolling(window=5).std()
        plt.plot(rolling_mean.index,rolling_mean,linestyle='--',label='',color=colors[idx_nn])
        plt.fill_between(rolling_std.index, rolling_mean-rolling_std, rolling_mean+rolling_std, color=colors[idx_nn], alpha=0.2)
     #   plt.plot(mean[:,dictVar['epoch']],mean[:,dictVar['val_%s'%met]],linestyle='-',label='Validation %s'%nn,color=colors[idx_nn])
    plt.xlabel('# epochs')
    plt.ylabel('%s'%met)
    axes = plt.gca()
   # axes.set_xlim(-1,30)
    axes.set_xlim(-1,60)
    ymin,ymax = axes.get_ylim()
    xmin,xmax=axes.get_xlim()
  #  current_dict = param_dicts[0]
  #  text0 = str(current_dict['architecture'])
   # text1 = str(current_dict['loss'])
   # text2= 'learning rate %s'%(current_dict['lr'])
   # textbox = text0+'\n'+text1+'\n'+text2
    plt.xlabel('# epochs')
    plt.ylabel('%s'%met)
    leg = plt.legend()
  #  txt=offsetbox.TextArea("%s"%textbox,textprops=dict(size=20)) 
  #  box = leg._legend_box 
  #  box.get_children().append(txt) 
  #  box.set_figure(box.figure)
    pltsavename = options.out_dir+'/dropout_loss_vs_epoch_%s'%(met)
    plt.savefig(pltsavename+'.png')
    plt.savefig(pltsavename+'.pdf')
    plt.clf()
  
