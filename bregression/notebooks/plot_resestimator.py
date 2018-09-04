import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT
#from ROOT import TCanvas, TH1F

matplotlib.rc_file('/users/nchernya/jupyter/bregression/matplotlibrc_LHCb')


file = 'applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5'
training ='2018-04-06_job23_2016'
path = '/users/nchernya/HHbbgg_ETH/bregression/output_root/paper/'
sample_name = 'ttbar'


data = pd.read_hdf('%s%s'%(path,file))
res = (data['Jet_resolution_NN_%s'%training])
res=np.array(res)
plt.hist(res,bins=200,normed=1,histtype='stepfilled')
axes = plt.gca()
axes.set_xlim(0,0.3)
#plt.grid(alpha=0.2,linestyle='--',markevery=2)
ymin, ymax = (axes).get_ylim()
xmin, xmax = (axes).get_xlim()
samplename='$t\\bar{t}$'
plt.text(xmax*0.8,ymax*0.85,r'%s'%samplename)
plt.xlabel(r'$\hat{\sigma}$',ha='right', x=1)
plt.ylabel('A.U.',ha='right', y=1)
plt.minorticks_on()
plt.text(0.1,11,r'\textbf{CMS} \textit{Work in Progress}',fontsize=14)
plt.text(0.1,13, '   ', {'size': 28})
savename='resolution_%s'%sample_name
path2='/users/nchernya/HHbbgg_ETH/bregression/plots/paper_rootstyle/%s/'%sample_name
plt.savefig(path2+savename+'.pdf')
plt.savefig(path2+savename+'.png')


#####Plot with ROOT#####
#Rhist = TH1F('res','res',200,0,0.30)
#for i in res:
#   Rhist.Fill(i)

