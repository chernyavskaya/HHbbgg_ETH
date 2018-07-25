import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file = 'applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5'
training ='2018-04-06_job23_2016'
path = '/users/nchernya/HHbbgg_ETH/bregression/output_root/paper/'
sample_name = 'ttbar'

data = pd.read_hdf('%s%s'%(path,file))
res = (data['Jet_resolution_NN_%s'%training])
res=np.array(res)
plt.hist(res,bins=200,normed=1)
axes = plt.gca()
axes.set_xlim(0,0.3)
plt.grid(alpha=0.2,linestyle='--',markevery=2)
ymin, ymax = (axes).get_ylim()
xmin, xmax = (axes).get_xlim()
samplename='$t\\bar{t}$'
plt.text(xmax*0.8,ymax*0.85,r'%s'%samplename, fontsize=30)
plt.xlabel(r'$\hat{\sigma}$',fontsize=30)
plt.ylabel('A.U.',fontsize=30)
savename='resolution_%s'%sample_name
path2='/users/nchernya/HHbbgg_ETH/bregression/plots/paper/%s/'%sample_name
plt.savefig(path2+savename+'.pdf')
plt.savefig(path2+savename+'.png')
