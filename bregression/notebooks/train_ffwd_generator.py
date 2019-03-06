#!/usr/bin/env python

import numpy as np

import bregnn.ffwd as ffwd 
import bregnn.io as io

import os
import json

from pprint import pprint

from sklearn.model_selection import train_test_split,KFold

from optparse import OptionParser, make_option

##
raw_features = ['Jet_pt',
                    'Jet_eta',
                    'rho',
                    'Jet_mt',
                    'Jet_leadTrackPt',
                    'Jet_leptonPtRel',
                    'Jet_leptonDeltaR',
                    'Jet_neHEF',
                    'Jet_neEmEF',
                    'Jet_vtxPt',
                    'Jet_vtxMass',
                    'Jet_vtx3dL',
                    'Jet_vtxNtrk',
                    'Jet_vtx3deL',
                    'Jet_numDaughters_pt03']
rings=[
                    'Jet_energyRing_dR0_em',
                    'Jet_energyRing_dR1_em',
                    'Jet_energyRing_dR2_em',
                    'Jet_energyRing_dR3_em',
                    'Jet_energyRing_dR4_em',
                    'Jet_energyRing_dR0_neut',
                    'Jet_energyRing_dR1_neut',
                    'Jet_energyRing_dR2_neut',
                    'Jet_energyRing_dR3_neut',
                    'Jet_energyRing_dR4_neut',
                    'Jet_energyRing_dR0_ch',
                    'Jet_energyRing_dR1_ch',
                    'Jet_energyRing_dR2_ch',
                    'Jet_energyRing_dR3_ch',
                    'Jet_energyRing_dR4_ch',
                    'Jet_energyRing_dR0_mu',
                    'Jet_energyRing_dR1_mu',
                    'Jet_energyRing_dR2_mu',
                    'Jet_energyRing_dR3_mu',
                    'Jet_energyRing_dR4_mu']

features=raw_features
for ring in rings:
    features.append('%s_Jet_rawEnergy'%ring)

## command_line options
parser = OptionParser(option_list=[
    make_option("--inp-dir",type='string',dest="inp_dir",default='/scratch/nchernya/HHbbgg/ttbar_2016_legacy_JECv11/'),
    make_option("--out-dir",type='string',dest="out_dir",default='/scratch/nchernya/HHbbgg/bregression_training_psi/output/'),
    make_option("--inp-files",type='string',dest='inp_files',default='ttbar_unweighted_full80M_selected_train.hd5'),
    make_option("--inp-file-valid",type='string',dest='inp_file_valid',default='ttbar_unweighted_full80M_selected_train.hd5'),
    make_option("--features",type='string',dest='features',default=''),
    make_option("--normalize-target",action="store_true",dest="normalize_target",default=True),
    make_option("--no-normalize-target",action="store_false",dest="normalize_target"),
    make_option("--loss",type='string',dest="loss",default="HybridLoss"),
#    make_option("--valid-frac",type='float',dest='valid_frac',default=0.10),
    make_option("--batch-size",type='int',dest='batch_size',default=1024),
    make_option("--epochs",type='int',dest='epochs',default=20),
    make_option("--hparams",type='string',dest='hparams',default=None),
    make_option("--seed",type='int',dest='seed',default=98543),
    make_option("--x-val",action="store_true",dest='x_val',default=False),
    make_option("--nkfolds",type='int',dest='nkfolds',default=5),
])

## parse options
(options, args) = parser.parse_args()

if options.features == '':
    features = features
    options.features = ','.join(features)
else:
    features = options.features.split(',')

print(features)

inp_file_valid = options.inp_dir+'/'+options.inp_file_valid
inp_files=options.inp_files.split(',')
inp_files = [options.inp_dir+'/'+c.strip() for c in inp_files] 

hparams = {}
if options.hparams is not None:
    for fname in  options.hparams.split(','):
       with open(fname) as hf:
          pars = json.loads(hf.read())
          hparams.update(pars)    # if inside several files we change the same parameter, it will overwrite for the one in the last file    

## read json with unweighting information
#with open('/scratch/snx3000/nchernya/bregression/unweighting_data.json' ) as fin_unweight:
#     unweight_info = json.loads(fin_unweight.read())
#unweight_bins = unweight_info['bins']
#unweight_values = unweight_info['values']


    
## read data
#columns = features + ['Jet_mcPt'] + ['Jet_corr_JEC'] # + ['Jet_corr_JER']
data_valid = (io.read_data(inp_file_valid, columns = None))
df_list = [(io.read_data(inf,columns = None)) for inf in inp_files]
for data in df_list+[data_valid]:
  ###############Unweighting#################
  #  data['rdn'] = np.random.uniform(0,1,data.shape[0])
  #  data['unweight_value'] = [unweight_values[k-1] for k in np.digitize(data['Jet_pt'], unweight_bins)]
  #  data.drop(data[data.rdn > data.unweight_value].index, inplace=True) # if random number is greater then unweighting function, drop event
  ###########################################
    data['Jet_pt']=data['Jet_pt']*data['Jet_rawEnergy']/data['Jet_e']
    data['Jet_mt']=data['Jet_mt']*data['Jet_rawEnergy']/data['Jet_e']
    data['Jet_mass']=data['Jet_mass']*data['Jet_rawEnergy']/data['Jet_e']
    data['Jet_leptonPtRelInv']=data['Jet_leptonPtRelInv']*data['Jet_rawEnergy']/data['Jet_e']
    data['Jet_mcPt_Jet_pt']=data['Jet_mcPt']/(data['Jet_pt']*data['Jet_corr_JEC'])
   # data['Jet_mcPt_Jet_pt']=data['Jet_mcPt']/(data['Jet_pt'])


X_shape = (data_valid[features].values).shape[1:]
y_valid = (data_valid[['Jet_mcPt_Jet_pt','Jet_pt']])#.values#.reshape(-1,1)
X_valid = data_valid[features].values


mygen = ffwd.Generator(df_list,options.batch_size,features,['Jet_mcPt_Jet_pt','Jet_pt'])
mygen_call = mygen()

y_mean,y_std = mygen.compute_stats()
print(y_mean,y_std)
# normalize target in validation, for training it is done in the class
if options.normalize_target:
    y_valid['Jet_mcPt_Jet_pt'] -= y_mean
    y_valid['Jet_mcPt_Jet_pt'] /= y_std
    for data in df_list:
        data['Jet_mcPt_Jet_pt']-=y_mean
        data['Jet_mcPt_Jet_pt']/=y_std
 


# sort out model parameters
def get_kwargs(fn,**kwargs):
    params = set(fn.__code__.co_varnames[:fn.__code__.co_argcount]+tuple(kwargs.keys()))
    for par in params:
        if hasattr(options,par):
            kwargs[par] = getattr(options,par)
        if par in hparams:
            kwargs[par] = hparams.pop(par)
    return kwargs

loss_params=dict()
#if options.loss == 'QuantileLoss' : loss_params=dict(taus=[0.4,0.25,0.75])
init_kwargs = get_kwargs(ffwd.FFWDRegression.__init__,monitor_dir=options.out_dir,loss_params=loss_params)
#fit_kwargs = get_kwargs(ffwd.FFWDRegression.fit,batch_size=options.batch_size,epochs=options.epochs)
fit_kwargs = get_kwargs(ffwd.FFWDRegression.fit,epochs=options.epochs,steps_per_epoch=mygen.steps)

print(init_kwargs)
print(fit_kwargs)

reg = ffwd.FFWDRegression('ffwd',X_shape,**init_kwargs)

pprint(reg.get_params())

model = reg()

print(model.summary())
model_summary = str(model.to_json()) 

trainable_count = int(np.sum([ffwd.K.count_params(p) for p in set(model.trainable_weights)]))
non_trainable_count = int(np.sum([ffwd.K.count_params(p) for p in set(model.non_trainable_weights)]))

if not os.path.exists(options.out_dir):
    os.mkdir(options.out_dir)

with open(options.out_dir+'/model_summary.txt','w+') as fo:
    fo.write(model_summary)

store = dict( y_mean=float(y_mean), y_std=float(y_std),
              Trainable_params=trainable_count,
              Nontrainable_params=non_trainable_count,
              model_params = reg.get_params(),
              fit_kwargs = fit_kwargs,
              options = options.__dict__
              )
with open(options.out_dir+'/config.json','w+') as fo:
    fo.write( json.dumps( store, indent=4 ) )
    fo.close()

#if options.x_val==True:
#    kf = KFold(n_splits=int(1./options.valid_frac),shuffle=True,random_state=options.seed) 
#    kf_idx = iter(kf.split(X)) 
#    for kfold in range(options.nkfolds):
#        # split data
#        train_idx,valid_idx = next(kf_idx)
#        X_train, X_valid = X[train_idx], X[valid_idx]
#        y_train, y_valid = y[train_idx], y[valid_idx]
#        reg.fit(X_train,y_train,kfold=kfold, 
#            validation_data=(X_valid,y_valid),
#            **fit_kwargs)
#else :
if options.x_val==False:
    reg.fit_generator(mygen_call,kfold=-1,  ### here if you want to save hdf file after each better epoch, put -1
        validation_data=(X_valid,y_valid),
        **fit_kwargs)

