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
gROOT.ProcessLineSync(".x /work/nchernya/setTDRStyle.C")
gROOT.ForceStyle()
gStyle.SetPadTopMargin(0.06)
gStyle.SetPadRightMargin(0.04)
#gStyle.SetPadLeftMargin(0.19)
gStyle.SetPadLeftMargin(0.20)


right,top   = gStyle.GetPadRightMargin(),gStyle.GetPadTopMargin()
left,bottom = gStyle.GetPadLeftMargin(),gStyle.GetPadBottomMargin()

padd = ROOT.TPaveText(left*1.1,1.-top*4.,0.4,1.-top*3.8,"NDC") 
padd.SetTextFont(42)
padd.AddText("70 < p_{T} < 100 GeV")
padd.SetTextSize(top*0.75)
padd.SetTextAlign(12)
padd.SetFillStyle(-1)
padd.SetBorderSize(0)



pCMS1 = ROOT.TPaveText(left*1.1,1.-top*4,0.4,1.,"NDC") #without Preliminary
#pCMS1 = ROOT.TPaveText(left*1.1,1.-top*3.85,0.4,1.,"NDC") #with Preliminary
pCMS1.SetTextFont(62)
pCMS1.AddText("CMS")


pCMS12 = ROOT.TPaveText(left*1.1+0.1,1.-top*4,0.57,1.,"NDC")
pCMS12.SetTextFont(52)
pCMS12.AddText("Simulation")
#pCMS12.AddText("Simulation Preliminary")

pCMS2 = ROOT.TPaveText(0.5,1.-top,1.-right*0.5,1.,"NDC")
pCMS2.SetTextFont(42)
pCMS2.AddText("(13 TeV)")

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
    make_option("--inp-dir",type='string',dest="inp_dir",default='/work/nchernya/HHbbgg_ETH_devel/bregression/output_files/NN_psi_training/paper/'),
    make_option("--sample-name",type='string',dest="samplename",default='ttbar'),
    make_option("--labels",type='string',dest="labels",default=''),
    make_option("--where",type='string',dest="where",default=''),
])

## parse options
(options, args) = parser.parse_args()
input_trainings = options.training.split(',')
input_files = options.inp_file.split(',')


now = str(datetime.datetime.now()).split(' ')[0]
savetag='April01_2020_CSBS'
#scratch_plots ='/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/2017JECv32/June05/'   #for studies
scratch_plots ='/work/nchernya/HHbbgg_ETH_devel/bregression/plots/paper/April01_2020/'  #for paper
#dirs=['',input_trainings[0],options.samplename]
dirs=['',options.samplename]
for i in range(len(dirs)):
  scratch_plots=scratch_plots+'/'+dirs[i]+'/'
  if not os.path.exists(scratch_plots):
    os.mkdir(scratch_plots)


print(options.where)
whats = ['p_T (GeV)','\eta','\\rho (GeV)']
#whats_root = ['p_{T} (GeV)','#eta','#rho (GeV)']
whats_root = ['p_{T}^{gen} (GeV)','|#eta|','#rho (GeV)'] 
#whats_root = ['p_{T}^{gen smeared} (GeV)','#eta','#rho (GeV)'] #for D.H. test
#ranges = [[30,400],[-2.5,2.5],[0,50]]
#binning =[50,10,20] #[50,20]
#ranges = [[30,400],[0,2.5],[0,50]]
#binning =[10,10,10] #[50,20]
#ranges = [[0,400],[0,2.5],[0,50]]
ranges = [[0,400],[0,2.5],[0,50]]
#ranges = [[30,400],[0,2.5],[0,50]] # D.H.
#ranges = [[20,700],[0,2.5],[0,50]] # D.H.
#binning =[7,10,20] #[50,20]
binning =[7,10,15] #[50,20]
linestyles = ['-.', '--','-', ':','-']
colors=['green','red','blue','cyan','magenta','blueviolet','orange','lime','brown','blue','blue']
markers=['s','o','^','h','>','<','s','o','o','o','o']
labels=options.labels.split(',')
bins_same = []

#for i in range(0,3):
for i in range(1,2):  #for some reason code crashes if running all 3 together, I ran 0-2, 2-3
 sigma_mu_array = []
 sigma_array = []
 mu_array = []
 for ifile in range(len(input_files)):
    # ## Read test data and model
  # load data
    #data = io.read_data('%s%s'%(options.inp_dir,input_files[ifile]),columns=None).query("Jet_pt>20")
    #data = io.read_data('%s%s'%(options.inp_dir,input_files[ifile]),columns=None).query("(Jet_pt>70) and (Jet_pt<100)")
    #data = io.read_data('%s%s'%(options.inp_dir,input_files[ifile]),columns=None).query("(Jet_mcPt>70) and (Jet_mcPt<100)")
    #data = io.read_data('%s%s'%(options.inp_dir,input_files[ifile]),columns=None).query("(Jet_pt>20) and (abs(Jet_eta)<0.5)")
    data = io.read_data('%s%s'%(options.inp_dir,input_files[ifile]),columns=None).query("(Jet_mcPt>70) and (Jet_mcPt<100)and (abs(Jet_eta)<0.5)")
    if options.where!='' : data = data.query(options.where)
    data.describe()

    #Regions of pt and eta 
    file_regions = open('..//scripts/regionsPtEta.json')
    regions_summary = json.loads(file_regions.read())
    region_names = regions_summary['pt_regions']+regions_summary['eta_region_names']

    data.loc[data['Jet_resolution_NN_%s'%input_trainings[ifile]] <= 0., 'Jet_resolution_NN_%s'%input_trainings[ifile] ] = 0.2

    data['Jet_resolution_NN_%s'%input_trainings[ifile]]*=1.4826
    res  =data['Jet_resolution_NN_%s'%input_trainings[ifile]]
    data['Jet_res_random'] = np.random.normal(1., res)

    #print data['Jet_res_random']

    y_gen = (data['Jet_mcPt']/(data['Jet_pt_raw']*data['Jet_corr_JEC'])).values.reshape(-1,1)
    y = (data['Jet_mcPt']/(data['Jet_pt_raw']*data['Jet_corr_JEC'])).values.reshape(-1,1)
    y_reco_gen = ((data['Jet_pt_raw']*data['Jet_corr_JEC'])/data['Jet_mcPt']).values.reshape(-1,1)
 #   X_pt = (data['Jet_pt_raw']).values.reshape(-1,1)
 #   X_pt = (data['Jet_pt_raw']*data['Jet_corr_JEC']).values.reshape(-1,1)
    X_pt = (data['Jet_mcPt']).values.reshape(-1,1) #
 #   X_pt  = (data['Jet_mcPt']*data['Jet_res_random']).values.reshape(-1,1) #for D.H. gen smeared


    X_eta = (abs(data['Jet_eta'])).values.reshape(-1,1)
    X_rho = (data['rho']).values.reshape(-1,1)
    y_pred = (data['Jet_pt_reg_NN_%s'%input_trainings[ifile]]) #bad name because it is actually a correction
    y_corr = (y_gen[:,0]/y_pred).values.reshape(-1,1)
    y_corr_reco_gen = (1./(y_gen[:,0]/y_pred)).values.reshape(-1,1)

    print 'Average pT : ',np.average(data['Jet_mcPt'])

    if i==0 : X = X_pt
    elif i==1 : X = X_eta
    elif i==2 : X = X_rho

 
 bins=100
 xmin=0
 xmax=2
 hist = ROOT.TH1F("hist","hist",bins,xmin,xmax)
 hist2 = ROOT.TH1F("hist2","hist2",bins,xmin,xmax)
 
 quantiles=np.array([0.25,0.40,0.5,0.75])
 inclusive_corr = np.percentile(y,quantiles*100.,axis=0).reshape(-1,1) 
 sigma_mu_corr_inclusive = np.array(0.5*(inclusive_corr[3]-inclusive_corr[0]))/np.array(inclusive_corr[1])
 
 inclusive_corr_reco_gen = np.percentile(y_reco_gen,quantiles*100.,axis=0).reshape(-1,1) 
 sigma_mu_corr_inclusive_reco_gen = np.array(0.5*(inclusive_corr_reco_gen[3]-inclusive_corr_reco_gen[0]))/np.array(inclusive_corr_reco_gen[1])
 ##############################################
 hist.FillN(len(y_reco_gen), array('d',y_reco_gen),array('d',np.ones(len(y_reco_gen)) ))
 hist2.FillN(len(y), array('d',y), array('d',np.ones(len(y)) ))
 
 hist.Scale(1./hist.Integral())
 hist2.Scale(1./hist2.Integral())
 
 hist.SetLineWidth(2)
 hist.SetLineColor(42)
 hist.SetFillColor(42)
 hist.SetFillStyle(4050)

 hist2.SetLineWidth(2)
 hist2.SetLineStyle(2)
 hist2.SetLineColor(1)
 
 #func = ROOT.TF1("func","gaus",0.98,1.6)
 #func = ROOT.TF1("func","gaus",0.94,1.16)
 func = ROOT.TF1("func","gaus",0.92,1.114)
 func.SetLineColor(ROOT.kRed)
 func.SetLineWidth(3)
 hist.Fit(func,"R")
 print "Reco/GEN"
 print 'q40/IQR : sigma/mu reco/gen : %.3f'%sigma_mu_corr_inclusive_reco_gen
 print 'fit : sigma/mu reco/gen : %.3f'%(func.GetParameter(2)/func.GetParameter(1))
 print "#mu=%0.2f#pm%.2f"%(func.GetParameter(1),func.GetParError(1))
 print "#sigma=%0.2f#pm%.2f"%(func.GetParameter(2),func.GetParError(2))
 
 #func2 = ROOT.TF1("func","gaus",0.75,1.05)
 #func2 = ROOT.TF1("func","gaus",0.84,1.05)
 func2 = ROOT.TF1("func","gaus",0.88,1.06)
 func2.SetLineColor(ROOT.kOrange-3)
 func2.SetLineWidth(3)
 hist2.Fit(func2,"R")
 print "GEN/Reco"
 print 'q40/IQR : sigma/mu gen/reco : %.3f'%sigma_mu_corr_inclusive
 print 'fit : sigma/mu gen/reco : %.3f'%(func2.GetParameter(2)/func2.GetParameter(1))
 print "#mu=%0.2f#pm%.2f"%(func2.GetParameter(1),func2.GetParError(1))
 print "#sigma=%0.2f#pm%.2f"%(func2.GetParameter(2),func2.GetParError(2))
  
 cnew = ROOT.TCanvas("cnewe","cnew",900,900)
 #cnew.SetLogy()
 framenew = ROOT.TH1F("hframenew", "hframenew", 1000, xmin,xmax)
 framenew.SetStats(0)
 framenew.GetXaxis().SetLabelSize(0.04)
 #framenew.GetXaxis().SetTitle("p_{T}^{gen} / p_{T}^{reco}")
 #framenew.GetXaxis().SetTitle("p_{T}^{reco} / p_{T}^{gen}")
 framenew.GetXaxis().SetTitle("ratio")
 framenew.GetYaxis().SetTitle("A.U.")
 framenew.GetYaxis().SetLabelSize(0.04)
 
 
 framenew.GetYaxis().SetRangeUser(1e-03,hist.GetMaximum()*1.2) #target norm with preliminary
 framenew.Draw()
 ROOT.gPad.Update()
 
 leg = ROOT.TLegend(0.7,0.5,0.9,0.8)
 leg.AddEntry(hist,"p_{T}^{reco} / p_{T}^{gen}","LF")
 leg.AddEntry(hist,"#bar{s} : %.2f"%sigma_mu_corr_inclusive_reco_gen,"")
 leg.AddEntry(hist,"Fit #sigma/#mu : %.2f "%(func.GetParameter(2)/func.GetParameter(1)),"")
 leg.AddEntry(hist2,"p_{T}^{gen} / p_{T}^{reco}","LF")
 leg.AddEntry(hist,"#bar{s} : %.2f"%sigma_mu_corr_inclusive,"")
 leg.AddEntry(hist,"Fit #sigma/#mu : %.2f "%(func2.GetParameter(2)/func2.GetParameter(1)),"")
 leg.SetFillStyle(-1)
 leg.SetBorderSize(0)
 leg.SetTextFont(42)
 leg.SetTextSize(0.03)
 leg.Draw()
 
 hist.Draw("HISTsame")
 hist2.Draw("HISTsame")
 func.Draw("same")
 func2.Draw("same")
 ROOT.gPad.Update()
 cnew.SaveAs('ratio_test_nocorr.pdf')
