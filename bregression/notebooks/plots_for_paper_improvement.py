import pandas as pd
import numpy as np
import keras.models
import os
import bregnn.io as io
import bregnn.utils as utils
import matplotlib.pyplot as plt
import sys
import json
from optparse import OptionParser, make_option
sys.path.insert(0, '/users/nchernya/HHbbgg_ETH/bregression/python/')
import datetime
import math
from matplotlib import gridspec
from array import array
import ROOT
from ROOT import TCanvas, TH1F, TGraph, TLegend
from ROOT import gROOT
from ROOT import gStyle

gROOT.SetBatch(True)
gROOT.ProcessLineSync(".x /mnt/t3nfs01/data01/shome/nchernya/setTDRStyle.C")
gROOT.ForceStyle()
gStyle.SetPadTopMargin(0.06)
gStyle.SetPadRightMargin(0.04)
gStyle.SetPadLeftMargin(0.19)


right,top   = gStyle.GetPadRightMargin(),gStyle.GetPadTopMargin()
left,bottom = gStyle.GetPadLeftMargin(),gStyle.GetPadBottomMargin()

pCMS1 = ROOT.TPaveText(left*1.1,1.-top*4,0.4,1.,"NDC")
pCMS1.SetTextFont(62)
pCMS1.AddText("CMS")


pCMS12 = ROOT.TPaveText(left*1.1+0.1,1.-top*4,0.57,1.,"NDC")
pCMS12.SetTextFont(52)
pCMS12.AddText("Simulation")

pCMS2 = ROOT.TPaveText(0.5,1.-top,1.-right*0.5,1.,"NDC")
pCMS2.SetTextFont(42)
pCMS2.AddText("13 TeV")

pCMSt = ROOT.TPaveText(0.5,1.-top*4,0.6,1.,"NDC")
pCMSt.SetTextFont(42)
pCMSt.AddText("t#bar{t}")

for item in [pCMSt,pCMS2,pCMS12,pCMS1]:
	item.SetTextSize(top*0.75)
	item.SetTextAlign(12)
	item.SetFillStyle(-1)
	item.SetBorderSize(0)

for item in [pCMS2]:
	item.SetTextAlign(32)

## parse options

parser = OptionParser(option_list=[
    make_option("--training",type='string',dest="training",default='2018-04-06_job23_2016'),
    make_option("--inp-file",type='string',dest='inp_file',default='applied_res_ttbar_RegressionPerJet_heppy_energyRings3_forTesting.hd5'),
    make_option("--inp-dir",type='string',dest="inp_dir",default='/scratch/nchernya/HHbbgg/paper/output_root/'),
    make_option("--sample-name",type='string',dest="samplename",default='ttbar'),
    make_option("--labels",type='string',dest="labels",default=''),
    make_option("--where",type='string',dest="where",default=''),
])

## parse options
(options, args) = parser.parse_args()
input_trainings = options.training.split(',')
input_files = options.inp_file.split(',')


now = str(datetime.datetime.now()).split(' ')[0]
scratch_plots ='/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/paper/November20/'
#dirs=['',input_trainings[0],options.samplename]
dirs=['',options.samplename]
for i in range(len(dirs)):
  scratch_plots=scratch_plots+'/'+dirs[i]+'/'
  if not os.path.exists(scratch_plots):
    os.mkdir(scratch_plots)
savetag='Nov20'


print(options.where)
whats = ['p_T (GeV)','\eta','\\rho (GeV)']
whats_root = ['p_{T} (GeV)','#eta','#rho (GeV)']
#ranges = [[30,400],[-2.5,2.5],[0,50]]
#binning =[50,10,20] #[50,20]
#ranges = [[30,400],[0,2.5],[0,50]]
#binning =[10,10,10] #[50,20]
ranges = [[0,400],[0,2.5],[0,50]]
binning =[7,10,20] #[50,20]
linestyles = ['-.', '--','-', ':','-']
colors=['green','red','blue','cyan','magenta','blueviolet','orange','lime','brown','blue','blue']
markers=['s','o','^','h','>','<','s','o','o','o','o']
labels=options.labels.split(',')
bins_same = []

#for i in range(0,1):
for i in range(0,3):
 sigma_mu_array = []
 sigma_array = []
 mu_array = []
 for ifile in range(len(input_files)):
    # ## Read test data and model
  # load data
    data = io.read_data('%s%s'%(options.inp_dir,input_files[ifile]),columns=None)
    if options.where!='' : data = data.query(options.where)
    data.describe()

    #Regions of pt and eta 
    file_regions = open('..//scripts/regionsPtEta.json')
    regions_summary = json.loads(file_regions.read())
    region_names = regions_summary['pt_regions']+regions_summary['eta_region_names']

    y = (data['Jet_mcPt']/(data['Jet_pt_raw']*data['Jet_corr_JEC'])).values.reshape(-1,1)
    X_pt = (data['Jet_pt_raw']).values.reshape(-1,1)
    X_pt_jec = (data['Jet_pt']).values.reshape(-1,1) # temp
    X_eta = (abs(data['Jet_eta'])).values.reshape(-1,1)
    X_rho = (data['rho']).values.reshape(-1,1)
    res = (data['Jet_resolution_NN_%s'%input_trainings[ifile]])
    y_pred = (data['Jet_pt_reg_NN_%s'%input_trainings[ifile]]) #bad name because it is actually a correction
    y_corr = (y[:,0]/y_pred).values.reshape(-1,1)


    if i==0 : X = X_pt
    elif i==1 : X = X_eta
    elif i==2 : X = X_rho

 
    if (ifile==0) : bins=np.linspace(ranges[i][0],ranges[i][1],binning[i])
    if ifile==0 and i==0 :  bins = np.array([0,20,40,60,80,100,150,200,250,300,400]) #ttbar
   ## if ifile==0 and i==0 :   bins = np.array([0,20,40,60,80,100,150,200]) #ZHbbll
 
    if ifile==0 :
       _, y_corr_mean_pt, y_corr_std_pt, y_corr_qt_pt = utils.profile(y_corr,X,bins=bins,quantiles=np.array([0.25,0.4,0.5,0.75])) 
    #   bins, y_corr_mean_pt, y_corr_std_pt, y_corr_qt_pt = utils.profile(y_corr,X,range=ranges[i],bins=bins,quantiles=np.array([0.25,0.4,0.5,0.75])) 
       bins_same.append(bins)
    else :  
       bins = bins_same[i]
       _, y_corr_mean_pt, y_corr_std_pt, y_corr_qt_pt = utils.profile(y_corr,X,bins=bins,quantiles=np.array([0.25,0.4,0.5,0.75])) 

    y_corr_median_pt = y_corr_qt_pt[2]
    y_corr_25_pt,y_corr_40_pt,y_corr_75_pt = y_corr_qt_pt[0],y_corr_qt_pt[1],y_corr_qt_pt[3]
    y_corr_iqr2_pt =  y_corr_qt_pt[0],y_corr_qt_pt[3]
    err_corr_iqr2 =  0.5*(y_corr_qt_pt[3]-y_corr_qt_pt[0])
    sigma_mu_corr = np.array(err_corr_iqr2)/np.array(y_corr_40_pt)
    sigma_mu_array.append(sigma_mu_corr)
    sigma_array.append(err_corr_iqr2)
    mu_array.append(y_corr_40_pt)
########################inclusive#############
    quantiles=np.array([0.25,0.40,0.5,0.75])
    inclusive_corr = np.percentile(y_corr,quantiles*100.,axis=0).reshape(-1,1) 
    sigma_mu_corr_inclusive = np.array(0.5*(inclusive_corr[3]-inclusive_corr[0]))/np.array(inclusive_corr[1])
##############################################





    _, y_mean_pt, y_std_pt, y_qt_pt = utils.profile(y,X,bins=bins,quantiles=np.array([0.25,0.4,0.5,0.75])) 
    y_25_pt,y_40_pt,y_75_pt = y_qt_pt[0],y_qt_pt[1],y_qt_pt[3]
    y_iqr2_pt =  y_qt_pt[0],y_qt_pt[3]
    err_jec_iqr2 =  0.5*(y_qt_pt[3]-y_qt_pt[0])
    sigma_mu_jec = np.array(err_jec_iqr2)/np.array(y_40_pt)
    sigma_jec = np.array(err_jec_iqr2)
    mu_jec = np.array(y_40_pt)
########################inclusive#############
    inclusive = np.percentile(y,quantiles*100.,axis=0).reshape(-1,1) 
    sigma_mu_inclusive = np.array(0.5*(inclusive[3]-inclusive[0]))/np.array(inclusive[1])
##############################################
    improvement_inclusive = (np.array(sigma_mu_corr_inclusive[0])-np.array(sigma_mu_inclusive[0]))/(np.array(sigma_mu_inclusive[0]))
    print('inclusive improvement : ',improvement_inclusive)

    binc = 0.5*(bins[1:]+bins[:-1])

  #  print(binc.shape,bins.shape,sigma_mu_jec.shape,err_corr_iqr2.shape,y_corr_median_pt.shape) 
 
    ## Draw profile of sigma (0.72-0.25)/2 vs eta and pt
    fig = plt.figure(figsize=(12,15)) 
    gs = gridspec.GridSpec(2, 1, height_ratios=[3,1]) 
    ax0 = plt.subplot(gs[0])


    if (ifile==0) :  ax0.scatter(binc,sigma_mu_jec,color='black',marker='*',label='baseline')
    ax0.scatter(binc,sigma_mu_corr,color=colors[ifile],marker=markers[ifile],label='%s'%labels[ifile])

###########declaring TGraphs###############
    gr_baseline = TGraph(len(binc),array('d',binc),array('d',sigma_mu_jec))
    gr_corrected = TGraph(len(binc),array('d',binc),array('d',sigma_mu_corr))
    for item in [gr_baseline,gr_corrected]:
        item.SetMarkerSize(1.9)
    gr_corrected.SetMarkerStyle(21)
    gr_corrected.SetMarkerColor(ROOT.kSpring-6)
    gr_baseline.SetMarkerStyle(29)
    gr_baseline.SetMarkerSize(2.4)
    gr_baseline.SetMarkerColor(ROOT.kBlack)
##########################################


 ax0.grid(alpha=0.2,linestyle='--',markevery=2)
 axes = plt.gca()
 if (i==0) : axes.set_ylim(0.02,0.3)
# if (i==1) : axes.set_ylim(0.06,0.15)
 if (i==1) : axes.set_ylim(0.08,0.16)
 if (i==2) : axes.set_ylim(0.08,0.17)
 axes.set_xlim(ranges[i][0],ranges[i][1])
 if (i==0) : axes.set_xlim(0,ranges[i][1])
 ymin, ymax = (axes).get_ylim()
 xmin, xmax = (axes).get_xlim()
 samplename=options.samplename
 if options.samplename=='ttbar' : samplename='$t\\bar{t}$'
 if options.samplename=='ZHbbll' : samplename='$Z(\\to{b\\bar{b}})H(\\to{l^+l^-})$'
 if  "HHbbgg" in options.samplename : samplename='$H(\\to{b\\bar{b}})H(\\to{\gamma\gamma}) %s'+ options.samplename[options.samplename.find('gg')+2:]
 lgd = ax0.legend(loc="upper left",fontsize=30)
 plt.ylabel(r'$\bar{\sigma}$',fontsize=30)

####################
##with ROOT 
 c2 = ROOT.TCanvas("canvas%d"%i,"canvas%d"%i,900,900)
 c2.cd()
 c2.SetGrid()
 frame = ROOT.TH1F("frame%d"%i,"",1,xmin,xmax)
 frame.SetStats(0)
 frame.GetXaxis().SetLabelSize(0.04)
 frame.GetYaxis().SetLabelSize(0.04)
 frame.GetYaxis().SetTitle("#bar{#sigma}")
 frame.GetYaxis().SetRangeUser(ymin,ymax)

 leg = TLegend()
 leg = ROOT.TLegend(0.75,0.75,0.9,0.9)
 leg.AddEntry(gr_baseline,"Baseline" ,"P")
 leg.AddEntry(gr_corrected,'%s'%labels[ifile] ,"P")
 leg.SetFillStyle(-1)
 leg.SetBorderSize(0)
 leg.SetTextFont(42)
 leg.SetTextSize(0.04)


 



# if 'p_T' not in whats[i] :
 if 'blablalbalbalbal'  in whats[i] :
    frame.GetYaxis().SetRangeUser(ymin,ymax*1.1)
    frame.GetXaxis().SetTitle(whats_root[i])
    frame.Draw()
    leg.Draw()
    pCMS1.Draw()
    pCMS12.Draw()
    pCMS2.Draw()
 #   pCMSt.Draw()
    gr_corrected.Draw("Psame")
    gr_baseline.Draw("Psame")

    plt.xlabel(r'$%s$'%whats[i],fontsize=30)
    ax0.text(xmax*0.8,ymax*0.95,r'%s'%samplename, fontsize=30)
 else :
    ax0.text(xmax*0.8,ymax*0.90,r'%s'%samplename, fontsize=30)
    ax1 = plt.subplot(gs[1])
    improvement = (np.array(sigma_mu_array[ifile])-np.array(sigma_mu_jec))/(np.array(sigma_mu_jec))
    ax1.scatter(binc,improvement,color=colors[ifile],marker=markers[ifile],label='%s'%labels[ifile])
    plt.xlabel(r'$%s$'%whats[i],fontsize=30)
    plt.ylabel(r'$\frac{(\bar{\sigma}_{DNN}-\bar{\sigma}_{baseline})}{\bar{\sigma}_{baseline}}$',fontsize=30)
    axes = plt.gca()
    axes.set_ylim(-0.12,0.)
    axes.set_xlim(0,ranges[i][1])
    ax1.grid(alpha=0.2,linestyle='--',markevery=1)


    c2.SetBottomMargin(0.3)
    frame.GetXaxis().SetTitleOffset(0.91);
    frame.GetXaxis().SetLabelSize(0)
    frame.Draw()
    leg.Draw()
    pCMS1.Draw()
    pCMS12.Draw()
    pCMS2.Draw()
  #  pCMSt.Draw()
    gr_baseline.Draw("Psame")
    gr_corrected.Draw("Psame")
	
    pad2 = ROOT.TPad("pad2", "pad2", 0., 0., 1., 1.)
    pad2.SetTopMargin(0.73)
    pad2.SetFillColor(0)
    pad2.SetFillStyle(0)
    pad2.Draw()
    pad2.cd()
 
    frame2 = ROOT.TH1F("frame_low_%d"%i,"",1,xmin,xmax)
    frame2.SetStats(0)
    frame2.GetXaxis().SetLabelSize(0.04)
    frame2.GetYaxis().SetTitleSize(0.04)
    frame2.GetYaxis().SetTitleOffset(2.0)
    frame2.GetYaxis().SetLabelSize(0.02)
    frame2.GetXaxis().SetTitle(whats_root[i])
    frame2.GetYaxis().CenterTitle(ROOT.kTRUE)
  #  frame2.GetYaxis().SetTitle("#frac{(#bar{#sigma}_{DNN}-#bar{#sigma}_{baseline})}{#bar{#sigma}_{baseline}}")	
    frame2.GetYaxis().SetTitle("#frac{#Delta#bar{#sigma}}{#bar{#sigma}_{baseline}}")	
    if i==0 : frame2.GetYaxis().SetRangeUser(-0.12,0.)
    else : frame2.GetYaxis().SetRangeUser(-0.30,0.)
    frame2.Draw()
    gr_improvement = TGraph(len(binc),array('d',binc),array('d',improvement))
    gr_improvement.SetMarkerSize(1.9)
    gr_improvement.SetMarkerStyle(21)
    gr_improvement.SetMarkerColor(ROOT.kSpring-6)
    gr_improvement.Draw("Psame") 

 where = (options.where).replace(' ','').replace('<','_').replace('>','_').replace('(','').replace(')','')
 savename='/IQR_compare_%s_%s%s%s'%(whats[i].replace('\\','').replace(' ','').replace('~',''),options.samplename,where,savetag)
# plt.savefig(scratch_plots+savename+'.pdf',bbox_extra_artists=(lgd,), bbox_inches='tight')
# plt.savefig(scratch_plots+savename+'.png',bbox_extra_artists=(lgd,), bbox_inches='tight')
 plt.clf()

 ROOT.gPad.Update()
 ROOT.gPad.RedrawAxis()
 c2.SaveAs(scratch_plots+savename+savetag+"_root.png"  )
 c2.SaveAs(scratch_plots+savename+savetag+"_root.pdf"  )

#########
# difference = 2*(np.array(sigma_mu_array[0])-np.array(sigma_mu_array[1]))/(np.array(sigma_mu_array[0])+np.array(sigma_mu_array[1]))
# difference = [round(a,4) for a in difference]
# data_csv = pd.DataFrame(np.array(difference).reshape(1,binc.shape[0]), columns=(binc))
 data_csv = pd.DataFrame({whats[i].replace('\\',''):binc})
 data_csv['onlyJEC'] = sigma_mu_jec
 data_csv['sigma_onlyJEC'] = sigma_jec
 for ifile in range(len(input_files)):
     data_csv['%s'%labels[ifile]] = sigma_mu_array[ifile]
     data_csv['sigma_%s'%labels[ifile]] = sigma_array[ifile]
     data_csv['mu_%s'%labels[ifile]] = mu_array[ifile]
   #  data_csv['delta_%s_JEC'%labels[ifile]] = 2*(np.array(sigma_mu_array[ifile])-np.array(sigma_mu_jec))/(np.array(sigma_mu_array[ifile])+np.array(sigma_mu_jec))
     data_csv['delta_%s_JEC_rel'%labels[ifile]] = (np.array(sigma_mu_array[ifile])-np.array(sigma_mu_jec))/(np.array(sigma_mu_jec))
     data_csv['delta_sigma_%s_JEC_rel'%labels[ifile]] = (np.array(sigma_array[ifile])-np.array(sigma_jec))/(np.array(sigma_jec))
     data_csv['delta_mu_%s_JEC_rel'%labels[ifile]] = (np.array(mu_array[ifile])-np.array(mu_jec))/(np.array(mu_jec))
     data_csv['inclusive_improvement_%s_JEC_rel'%labels[ifile]] = improvement_inclusive
     for jfile in range(ifile+1,len(input_files)):
         data_csv['delta_%s_%s'%(labels[ifile],labels[jfile])] = 2*(np.array(sigma_mu_array[ifile])-np.array(sigma_mu_array[jfile]))/(np.array(sigma_mu_array[ifile])+np.array(sigma_mu_array[jfile]))
         data_csv['delta_sigma_%s_%s'%(labels[ifile],labels[jfile])] = 2*(np.array(sigma_array[ifile])-np.array(sigma_array[jfile]))/(np.array(sigma_array[ifile])+np.array(sigma_array[jfile]))
              
 savename='/data_IQR_compare_%s_%s%s%s.csv'%(whats[i].replace('\\',''),options.samplename,where,savetag)
 data_csv.to_csv(scratch_plots+savename)
