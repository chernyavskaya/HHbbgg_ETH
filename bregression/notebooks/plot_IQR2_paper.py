import keras.models
import os
import bregnn.io as io
import bregnn.utils as utils
import sys
import json
from optparse import OptionParser, make_option
sys.path.insert(0, '/users/nchernya/HHbbgg_ETH/bregression/python/')
import datetime

parser = OptionParser(option_list=[
    make_option("--training",type='string',dest="training",default='HybridLoss'),
    make_option("--inp-file",type='string',dest='inp_file',default='applied_res_ttbar_RegressionPerJet_heppy_energyRings3_forTesting.hd5'),
    make_option("--inp-dir",type='string',dest="inp_dir",default='/scratch/snx3000/nchernya/bregression/output_root/'),
    make_option("--sample-name",type='string',dest="samplename",default='ttbar'),
])

## parse options
(options, args) = parser.parse_args()
input_trainings = options.training.split(',')

now = str(datetime.datetime.now()).split(' ')[0]
scratch_plots ='/users/nchernya/HHbbgg_ETH/bregression/plots/paper/'
#dirs=['',input_trainings[0],options.samplename]
dirs=['',options.samplename]
for i in range(len(dirs)):
  scratch_plots=scratch_plots+'/'+dirs[i]+'/'
  if not os.path.exists(scratch_plots):
    os.mkdir(scratch_plots)
savetag='average'
 

# ## Read test data and model
# load data
data = io.read_data('%s%s'%(options.inp_dir,options.inp_file),columns=None)
data.describe()

data = data.query("isOther!=1")

#Regions of pt and eta 
file_regions = open('/users/nchernya/HHbbgg_ETH/bregression/scripts/regionsPtEta.json')
regions_summary = json.loads(file_regions.read())
region_names = regions_summary['pt_regions']+regions_summary['eta_region_names']

#y = (data['Jet_mcPt']/data['Jet_pt']).values.reshape(-1,1)
y = (data['Jet_mcPt']/(data['Jet_pt_raw']*data['Jet_corr_JEC'])).values.reshape(-1,1)
X_pt = (data['Jet_pt_raw']).values.reshape(-1,1)
X_pt_jec = (data['Jet_pt_raw']*data['Jet_corr_JEC']).values.reshape(-1,1)
X_pt_gen = (data['Jet_mcPt']).values.reshape(-1,1)
X_eta = (data['Jet_eta']).values.reshape(-1,1)
X_rho = (data['rho']).values.reshape(-1,1)
res = (data['Jet_resolution_NN_%s'%input_trainings[0]]).values.reshape(-1,1)
y_pred = (data['Jet_pt_reg_NN_%s'%input_trainings[0]]) #bad name because it is actually a correction
y_corr = (y[:,0]/y_pred).values.reshape(-1,1)
# errors vector
err = (y[:,0]-y_pred).values.reshape(-1,1)

linestyles = ['-.', '--','-', ':']

whats = ['p_T (GeV)','\eta','\\rho']
ranges = [[30,400],[-2.5,2.5],[0,50]]
binning =[50,10,20] #[50,20]
for i in range(0,3):
 if i==0 : X = X_pt
 elif i==1 : X = X_eta
 elif i==2 : X = X_rho
 print(i,X)
 
 bins=binning[i]
 if ('ggHHbbgg' in options.samplename) and ('p_T' in whats[i]) : bins=int(binning[i]/2.)
 if ('ZHbbll' in options.samplename) and ('eta' in whats[i]) : ranges[i]=[-2.45,2.45]
 bins, y_mean_pt, y_std_pt, y_qt_pt = utils.profile(y,X,range=ranges[i],bins=bins,uniform=False,quantiles=np.array([0.25,0.4,0.5,0.75]))
 y_median_pt = y_qt_pt[2]
 y_25_pt,y_40_pt,y_75_pt = y_qt_pt[0],y_qt_pt[1],y_qt_pt[3]
 y_iqr2_pt =  y_qt_pt[0],y_qt_pt[3]
 err_iqr2 =  0.5*(y_qt_pt[3]-y_qt_pt[0])
 
 _, y_corr_mean_pt, y_corr_std_pt, y_corr_qt_pt = utils.profile(y_corr,X,bins=bins,quantiles=np.array([0.25,0.4,0.5,0.75])) 
 y_corr_median_pt = y_corr_qt_pt[2]
 y_corr_25_pt,y_corr_40_pt,y_corr_75_pt = y_corr_qt_pt[0],y_corr_qt_pt[1],y_corr_qt_pt[3]
 y_corr_iqr2_pt =  y_corr_qt_pt[0],y_corr_qt_pt[3]
 err_corr_iqr2 =  0.5*(y_corr_qt_pt[3]-y_corr_qt_pt[0])

 binc = 0.5*(bins[1:]+bins[:-1])
####Calculate the improvement on IQR/2 ###
 iqr2_improvement = 2*(np.array(err_iqr2)-np.array(err_corr_iqr2))/(np.array(err_iqr2)+np.array(err_corr_iqr2))
 iqr2_rel_improvement = 2*(np.array(err_iqr2/y_40_pt)-np.array(err_corr_iqr2/y_corr_40_pt))/(np.array(err_iqr2/y_40_pt)+np.array(err_corr_iqr2/y_corr_40_pt))


 plt.plot(binc,y_25_pt,label='baseline',linestyle=linestyles[0],color='b')
 plt.plot(binc,y_corr_25_pt,label='DNN',linestyle=linestyles[2],color='r')
 plt.plot(binc,y_40_pt,linestyle=linestyles[0],color='b')
 plt.plot(binc,y_corr_40_pt,linestyle=linestyles[2],color='r')
 plt.plot(binc,y_median_pt,linestyle=linestyles[0],color='b')
 plt.plot(binc,y_corr_median_pt,linestyle=linestyles[2],color='r')
 plt.plot(binc,y_75_pt,linestyle=linestyles[0],color='b')
 plt.plot(binc,y_corr_75_pt,linestyle=linestyles[2],color='r')
 ymin, ymax = (plt.gca()).get_ylim()
 xmin, xmax = (plt.gca()).get_xlim()
# plt.text(xmin+abs(xmin)*0.05,ymax*0.98,'Quantiles : 0.25, 0.40, 0.50, 0.75', fontsize=30)

 samplename=options.samplename
 if options.samplename=='ttbar' : samplename='$t\\bar{t}$'
 if options.samplename=='ZHbbll' : samplename='$Z(\\to{b\\bar{b}})H(\\to{l^+l^-})$'
 if options.samplename=="HHbbgg700" : samplename='$H(\\to{b\\bar{b}})H(\\to{\gamma\gamma})'
 plt.text(xmin+abs(xmin)*0.05,ymax*0.96,'%s'%samplename, fontsize=30)
 
 plt.xlabel('$%s$'%whats[i], fontsize=30)
 plt.ylabel('$p_{T,jet}^{gen} / p_{T,jet}^{reco}$', fontsize=30)
 plt.legend(loc='upper right',fontsize=30)
 savename='/quantiles_col_%s_%s_%s'%(input_trainings[0],whats[i].replace('\\',''),options.samplename)
 plt.savefig(scratch_plots+savename+savetag+'.png')
 plt.savefig(scratch_plots+savename+savetag+'.pdf')
 plt.clf()
 
##########################################################
##Draw IQR/2 vs resolution estimator
res_bins_incl, err_qt_res_incl = utils.profile(err,res,bins=30,range=[0,0.3],moments=False,average=True) 
err_iqr2_incl =  0.5*(err_qt_res_incl[2]-err_qt_res_incl[0])
#plt.scatter(0.5*(res_bins_incl[1:]+res_bins_incl[:-1]),err_iqr2_incl,label='inclusive')
plt.scatter(res_bins_incl,err_iqr2_incl,label='inclusive')
plt.grid(alpha=0.2,linestyle='--',markevery=2)
axes = plt.gca()
axes.set_ylim(0,0.30)
axes.set_xlim(0,0.30)
ymin, ymax = axes.get_ylim()
xmin, xmax = (plt.gca()).get_xlim()
plt.text(0.01,ymax*0.85,r'%s'%samplename,fontsize=30)
plt.ylabel(r'$\bar{\sigma}$',fontsize=30)
plt.xlabel(r'$<\hat{\sigma}>$',fontsize=30)
savename='/IQR_sigma_pt_%s_%s'%(input_trainings[0],options.samplename)
plt.savefig(scratch_plots+savename+savetag+'.pdf')
plt.savefig(scratch_plots+savename+savetag+'.png')
plt.clf()
