import keras.models
import os
import bregnn.io as io
import bregnn.utils as utils
import sys
import json
from optparse import OptionParser, make_option
sys.path.insert(0, '/users/nchernya/HHbbgg_ETH/bregression/python/')
import plotting_utils as plotting
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
scratch_plots ='/scratch/snx3000/nchernya/bregression/plots/quantiles/%s/'%now
dirs=['',input_trainings[0],options.samplename]
for i in range(len(dirs)):
  scratch_plots=scratch_plots+'/'+dirs[i]+'/'
  if not os.path.exists(scratch_plots):
    os.mkdir(scratch_plots)
 

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
res = (data['Jet_resolution_NN_%s'%input_trainings[0]])
y_pred = (data['Jet_pt_reg_NN_%s'%input_trainings[0]]) #bad name because it is actually a correction
y_hbb = (data['Jet_mcPt']/data['Jet_pt_reg']).values.reshape(-1,1)
y_corr = (y[:,0]/y_pred).values.reshape(-1,1)
# errors vector
err = y[:,0]-y_pred

linestyles = ['-.', '--','-', ':']

whats = ['p_T','\eta','rho']
ranges = [[30,400],[-2.5,2.5],[0,50]]
binning =[50,10,20] #[50,20]
for i in range(0,1):
 if i==0 : X = X_pt
 if i==0 : X = X_pt_gen
# if i==0 : X = X_pt_jec
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


 _, y_hbb_mean_pt, y_hbb_std_pt, y_hbb_qt_pt = utils.profile(y_hbb,X,bins=bins,quantiles=np.array([0.25,0.4,0.5,0.75])) 
 y_hbb_iqr2_pt =  y_hbb_qt_pt[0],y_hbb_qt_pt[3]
 err_hbb_iqr2 =  0.5*(y_hbb_qt_pt[3]-y_hbb_qt_pt[0])
 
 binc = 0.5*(bins[1:]+bins[:-1])
 
####Calculate the improvement on IQR/2 ###
 iqr2_improvement = 2*(np.array(err_iqr2)-np.array(err_corr_iqr2))/(np.array(err_iqr2)+np.array(err_corr_iqr2))
 iqr2_rel_improvement = 2*(np.array(err_iqr2/y_40_pt)-np.array(err_corr_iqr2/y_corr_40_pt))/(np.array(err_iqr2/y_40_pt)+np.array(err_corr_iqr2/y_corr_40_pt))


 ##Plot raw and corrected mean with their stds on one plot
 plt.plot(binc,y_mean_pt,label='raw (mean)')
 plt.fill_between(binc,y_mean_pt-y_std_pt,y_mean_pt+y_std_pt,alpha=0.4,label='raw (RMS)')
 plt.plot(binc,y_corr_mean_pt,label='corrected (mean)')
 plt.fill_between(binc,y_corr_mean_pt-y_corr_std_pt,y_corr_mean_pt+y_corr_std_pt,alpha=0.4,label='corrected (RMS)')
 plt.plot(binc,y_median_pt,label='raw (median)')
 plt.fill_between(binc,*y_iqr2_pt,alpha=0.4,label='raw (IQR)')
 plt.plot(binc,y_corr_median_pt,label='corrected (median)')
 plt.fill_between(binc,*y_corr_iqr2_pt,alpha=0.4,label='corrected (IQR)')
 
# plt.xlabel('$p_T$')
 plt.xlabel('$%s$'%whats[i])
 plt.ylabel('$p_T^{true} / p_T^{reco}$')
 plt.legend()
 savename='/mean_median_%s_%s'%(whats[i].replace('\\',''),options.samplename)
# plt.savefig(scratch_plots+savename+'.png')
# plt.savefig(scratch_plots+savename+'.pdf')
 plt.clf()
 
 
 ## Draw several quantiles on one plot
# plt.plot(binc,y_25_pt,label='raw (0.25)',linestyle=linestyles[0],color='b')
# plt.plot(binc,y_corr_25_pt,label='corrected (0.25)',linestyle=linestyles[2],color='b')
# plt.plot(binc,y_40_pt,label='raw (0.40)',linestyle=linestyles[0],color='g')
# plt.plot(binc,y_corr_40_pt,label='corrected (0.40)',linestyle=linestyles[2],color='g')
# plt.plot(binc,y_median_pt,label='raw (0.50)',linestyle=linestyles[0],color='r')
# plt.plot(binc,y_corr_median_pt,label='corrected (0.50)',linestyle=linestyles[2],color='r')
# plt.plot(binc,y_75_pt,label='raw (0.75)',linestyle=linestyles[0],color='c')
# plt.plot(binc,y_corr_75_pt,label='corrected (0.75)',linestyle=linestyles[2],color='c')

 plt.plot(binc,y_25_pt,label='raw',linestyle=linestyles[0],color='b')
 plt.plot(binc,y_corr_25_pt,label='corrected',linestyle=linestyles[2],color='r')
 plt.plot(binc,y_40_pt,linestyle=linestyles[0],color='b')
 plt.plot(binc,y_corr_40_pt,linestyle=linestyles[2],color='r')
 plt.plot(binc,y_median_pt,linestyle=linestyles[0],color='b')
 plt.plot(binc,y_corr_median_pt,linestyle=linestyles[2],color='r')
 plt.plot(binc,y_75_pt,linestyle=linestyles[0],color='b')
 plt.plot(binc,y_corr_75_pt,linestyle=linestyles[2],color='r')
 ymin, ymax = (plt.gca()).get_ylim()
 xmin, xmax = (plt.gca()).get_xlim()
 plt.text(xmin+abs(xmin)*0.05,ymax*0.98,'Quantiles : 0.25,0.40,0.50,0.75', fontsize=15)
 plt.text(xmin+abs(xmin)*0.05,ymax*0.96,'%s'%options.samplename, fontsize=15)
 
 plt.xlabel('$%s$'%whats[i])
 plt.ylabel('$p_T^{true} / p_T^{reco}$')
 plt.legend(loc='upper right')
 savename='/quantiles_col_%s_%s_%s'%(input_trainings[0],whats[i].replace('\\',''),options.samplename)
 plt.savefig(scratch_plots+savename+'.png')
 plt.savefig(scratch_plots+savename+'.pdf')
 plt.clf()
 
  ## Draw profile of sigma (0.72-0.25)/2 vs eta and pt
 plt.scatter(binc,err_iqr2,color='red',marker='^',label='No Regression')
# plt.scatter(binc,err_hbb_iqr2,color='blue',marker='s',label='HIG-17-009')
 plt.scatter(binc,err_corr_iqr2,color='green',marker='o',label='NN %s'%input_trainings[0])
 plt.grid(alpha=0.2,linestyle='--',markevery=2)
 axes = plt.gca()
 if (i==0) : axes.set_ylim(0.02,0.20)
 if (i==1) : axes.set_ylim(0.02,0.15)
 axes.set_xlim(ranges[i][0],ranges[i][1])
 if (i==0) : axes.set_xlim(0,ranges[i][1])
 ymin, ymax = (plt.gca()).get_ylim()
 plt.text(xmin+abs(xmin)*0.05,ymax*0.95,'%s'%options.samplename, fontsize=20)
 lgd = plt.legend(loc="lower center",numpoints=1,ncol=2,bbox_to_anchor=(0.0,-0.202,1.,-.202),borderaxespad=0.,mode='expand')
 plt.xlabel('$%s$'%whats[i])
 plt.ylabel('IQR / 2')
 savename='/IQR_20bins_%s_%s_%s'%(input_trainings[0],whats[i].replace('\\',''),options.samplename)
 plt.savefig(scratch_plots+savename+'.pdf',bbox_extra_artists=(lgd,), bbox_inches='tight')
 plt.savefig(scratch_plots+savename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
 plt.clf()

### Draw improveemnt on sigma####
 plt.scatter(binc,iqr2_improvement,color='red',marker='o')
 plt.grid(alpha=0.2,linestyle='--',markevery=2)
 axes = plt.gca()
 axes.set_ylim(0.0,0.50)
 axes.set_xlim(ranges[i][0],ranges[i][1])
 ymin, ymax = axes.get_ylim()
 plt.text(xmin+abs(xmin)*0.05,ymax*0.95,'%s'%options.samplename, fontsize=20)
 plt.title('NN vs No regression')
 plt.xlabel('$%s$'%whats[i])
 plt.ylabel('IQR/2 rel. improvement $\sigma$')
 savename='/IQR_improvement_%s_%s_%s'%(input_trainings[0],whats[i].replace('\\',''),options.samplename)
 plt.savefig(scratch_plots+savename+'.pdf',bbox_extra_artists=(lgd,), bbox_inches='tight')
 plt.savefig(scratch_plots+savename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
 plt.clf()



### Draw improveemnt on sigma over mu ####
 plt.scatter(binc,iqr2_rel_improvement,color='red',marker='o')
 plt.grid(alpha=0.2,linestyle='--',markevery=2)
 axes = plt.gca()
 axes.set_ylim(0.00,0.25)
 axes.set_xlim(ranges[i][0],ranges[i][1])
 ymin, ymax = axes.get_ylim()
 plt.text(xmin+abs(xmin)*0.05,ymax*0.95,'%s'%options.samplename, fontsize=20)
 plt.title('NN vs No regression')
 plt.xlabel('$%s$'%whats[i])
 plt.ylabel('IQR/2 rel. improvement $\sigma/\mu$')
 savename='/IQR_improvement_sigma_mu_%s_%s_%s'%(input_trainings[0],whats[i].replace('\\',''),options.samplename)
 plt.savefig(scratch_plots+savename+'.pdf',bbox_extra_artists=(lgd,), bbox_inches='tight')
 plt.savefig(scratch_plots+savename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
 plt.clf()

##########################################################
##Draw IQR/2 vs resolution estimator
res_bins_incl, err_qt_res_incl = utils.profile(err,res,bins=30,range=[0,0.3],moments=False) 
err_iqr2_incl =  0.5*(err_qt_res_incl[2]-err_qt_res_incl[0])
#pt_bins=["(Jet_mcPt>=20 & Jet_mcPt<30)","(Jet_mcPt>=30 & Jet_mcPt<60)", "(Jet_mcPt>=60 & Jet_mcPt<100)", "(Jet_mcPt>=100 & Jet_mcPt<150)", "(Jet_mcPt>=150 & Jet_mcPt<200)"]
pt_bins=["(Jet_mcPt>=20 & Jet_mcPt<30)","(Jet_mcPt>=30 & Jet_mcPt<50)", "(Jet_mcPt>=50 & Jet_mcPt<70) ","(Jet_mcPt>=70 & Jet_mcPt<100)", "(Jet_mcPt>=100 & Jet_mcPt<120)","(Jet_mcPt>=120 & Jet_mcPt<150)", "(Jet_mcPt>=150 & Jet_mcPt<200)"]
pt_boundaries = [20,30,35,40,50,60,70,80,90,100,110,120,130,140,150,170,200]
pt_bins = ["Jet_mcPt>=%s & Jet_mcPt<%s"%(pt_boundaries[a],pt_boundaries[a+1]) for a in range(0,len(pt_boundaries)-1)]
for pt_bin in pt_bins:
    data_bin = data.query(pt_bin)
    y_bin = (data_bin['Jet_mcPt']/(data_bin['Jet_pt_raw']*data_bin['Jet_corr_JEC'])).values.reshape(-1,1)
    res_bin = (data_bin['Jet_resolution_NN_%s'%input_trainings[0]])
    y_pred_bin = (data_bin['Jet_pt_reg_NN_%s'%input_trainings[0]]) #bad name because it is actually a correction
    # errors vector
    err_bin = y_bin[:,0]-y_pred_bin

    ##Draw IQR/2 vs resolution estimator
    res_bins, err_qt_res = utils.profile(err_bin,res_bin,bins=30,range=[0,0.3],moments=False) 
    err_iqr2 =  0.5*(err_qt_res[2]-err_qt_res[0])

    plt.scatter(0.5*(res_bins_incl[1:]+res_bins_incl[:-1]),err_iqr2_incl,color='blue',label='inclusive')
    plt.scatter(0.5*(res_bins[1:]+res_bins[:-1]),err_iqr2,color='red',label='%s'%pt_bin)
    plt.fill_between(res_bins_incl[1:]+res_bins_incl[:-1],0.8*np.array(res_bins_incl[1:]+res_bins_incl[:-1]),1.2*np.array(res_bins_incl[1:]+res_bins_incl[:-1]),alpha=0.3,label='20% band',color='green')
    plt.grid(alpha=0.5,linestyle='--',markevery=2)
    axes = plt.gca()
    axes.set_ylim(0,0.30)
    axes.set_xlim(0,0.30)
    ymin, ymax = axes.get_ylim()
    xmin, xmax = (plt.gca()).get_xlim()
#    plt.text(xmin+abs(xmin)*0.05,ymax*0.80,'%s'%pt_bin, fontsize=20)
    plt.text(xmin+abs(xmin)*0.1,ymax*0.75,'%s'%options.samplename, fontsize=20)
    plt.xlabel('$\sigma(p_T)/p_T$')
    plt.ylabel('error vector IQR / 2')
    plt.legend()
    savename='/IQR_sigma_pt_%s_%s_%s'%(input_trainings[0],options.samplename,pt_bin)
    plt.savefig(scratch_plots+savename+'.pdf')
    plt.savefig(scratch_plots+savename+'.png')
    plt.clf()
