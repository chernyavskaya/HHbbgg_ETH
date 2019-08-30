import numpy as np
import keras.models
import os
import bregnn.io as io
import bregnn.utils as utils
import sys
import json
import matplotlib.pyplot as plt
from optparse import OptionParser, make_option
sys.path.insert(0, '/users/nchernya/HHbbgg_ETH/bregression/python/')
import datetime
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


pName = ROOT.TPaveText(left*1.1,1.-top*6,0.6,1.,"NDC")
pName.SetTextFont(42)

pCMS2 = ROOT.TPaveText(0.5,1.-top,1.-right*0.5,1.,"NDC")
pCMS2.SetTextFont(42)
pCMS2.AddText("(13 TeV)")

pCMSt = ROOT.TPaveText(0.5,1.-top*4,0.6,1.,"NDC")
pCMSt.SetTextFont(42)
pCMSt.AddText("t#bar{t}")

for item in [pCMSt,pCMS2,pCMS12,pCMS1,pName]:
	item.SetTextSize(top*0.75)
	item.SetTextAlign(12)
	item.SetFillStyle(-1)
	item.SetBorderSize(0)

for item in [pCMS2]:
	item.SetTextAlign(32)


parser = OptionParser(option_list=[
    make_option("--training",type='string',dest="training",default='2018-04-06_job23_2016'),
    make_option("--inp-file",type='string',dest='inp_file',default='applied_res_ttbar_RegressionPerJet_heppy_energyRings3_forTesting.hd5'),
    make_option("--inp-dir",type='string',dest="inp_dir",default='/scratch/nchernya/HHbbgg/paper/output_root/'),
    make_option("--sample-name",type='string',dest="samplename",default='ttbar'),
    make_option("--where",type='string',dest="where",default=''),
])

## parse options
(options, args) = parser.parse_args()
input_trainings = options.training.split(',')

now = str(datetime.datetime.now()).split(' ')[0]
scratch_plots ='/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/paper/August30_2019/'
#dirs=['',input_trainings[0],options.samplename]
dirs=['',options.samplename]
for i in range(len(dirs)):
  scratch_plots=scratch_plots+'/'+dirs[i]+'/'
  if not os.path.exists(scratch_plots):
    os.mkdir(scratch_plots)
savetag='Feb25'
 

# ## Read test data and model
# load data
data = io.read_data('%s%s'%(options.inp_dir,options.inp_file),columns=None).query('Jet_mcPt>30')
data.describe()
if options.where!='' : data = data.query(options.where)

#Regions of pt and eta 
file_regions = open('..//scripts/regionsPtEta.json')
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
where = (options.where).replace(' ','').replace('<','_').replace('>','_').replace('(','').replace(')','')



##########################################################
##Draw IQR/2 vs resolution estimator
res_bins_incl, err_qt_res_incl = utils.profile(err,res,bins=30,range=[0,0.3],moments=False,average=True) 
err_iqr2_incl =  0.5*(err_qt_res_incl[2]-err_qt_res_incl[0])
res_bins_incl_array = array('d',res_bins_incl)
err_iqr2_incl_array = array('d',err_iqr2_incl)
gr = TGraph(len(res_bins_incl),res_bins_incl_array,err_iqr2_incl_array)
gr.SetMarkerStyle(20)
gr.SetMarkerSize(1.8)
gr.SetMarkerColor(ROOT.kBlue)
func = ROOT.TF1("func","pol1",0.,0.4)
gr.Fit("func","0")
#gr.Fit("func")
par0 = func.GetParameter(0)
par1 = func.GetParameter(1)
#par0=0
#par1=1.
colors=[ROOT.kRed,ROOT.kOrange-3,ROOT.kSpring+9,3,4,5,6]
markers=[29,33,34,21,22,23,24]


n_points = 200
resolution_array = array('d',np.linspace(0,0.40,n_points))
err_iqr2_incl_array_up = array('d',map(lambda x: 1.2*(par0+par1*x), resolution_array))
err_iqr2_incl_array_down = array('d',map(lambda x: 0.8*(par0+par1*x), resolution_array))


gr_up = TGraph(2*n_points)
for i in range(n_points):
	gr_up.SetPoint(i,resolution_array[i],err_iqr2_incl_array_up[i])
	gr_up.SetPoint(n_points+i,resolution_array[n_points-i-1],err_iqr2_incl_array_down[n_points-i-1])
gr_up.SetLineColor(ROOT.kCyan-10)
gr_up.SetFillColor(ROOT.kCyan-10)

#pt_bins=["(Jet_mcPt>=60 & Jet_mcPt<70) ","(Jet_mcPt>=80 & Jet_mcPt<90)", "(Jet_mcPt>=100 & Jet_mcPt<110)"]
#pt_bins=["(Jet_mcPt>=30 & Jet_mcPt<50)", "(Jet_mcPt>=50 & Jet_mcPt<70) ","(Jet_mcPt>=70 & Jet_mcPt<100)"]
#pt_bins_names=["30 < p_{T} < 50 GeV ","50 < p_{T} < 70 GeV", "70 < p_{T} < 100 GeV"]
pt_bins=["(Jet_mcPt>=30 & Jet_mcPt<50)", "(Jet_mcPt>=50 & Jet_mcPt<70) ","(Jet_mcPt>=110 & Jet_mcPt<120)"]
pt_bins_names=["30 < p_{T} < 50 GeV ","50 < p_{T} < 70 GeV", "110 < p_{T} < 120 GeV"]
#pt_bins=["(Jet_mcPt>=25 & Jet_mcPt<30)","(Jet_mcPt>=25 & Jet_mcPt<50)","(Jet_mcPt>=30 & Jet_mcPt<50)", "(Jet_mcPt>=50 & Jet_mcPt<70) ","(Jet_mcPt>=70 & Jet_mcPt<100)"]
#pt_bins_names=["25 < p_{T} < 30 GeV","25 < p_{T} < 50 GeV","30 < p_{T} < 50 GeV","50 < p_{T} < 70 GeV", "70 < p_{T} < 100 GeV"]
ymin, ymax = 0.,0.30 
xmin, xmax = 0.,0.30 
graphs=[]
savename='/IQR_sigma_pt_%s_%s_%s'%(input_trainings[0],options.samplename,where)
c = ROOT.TCanvas("c","c",900,900)
c.cd()
frame = ROOT.TH1F("frame","",1,0,0.30)
frame.SetStats(0)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetYaxis().SetLabelSize(0.04)
frame.GetYaxis().SetTitle("#bar{#sigma}")
frame.GetXaxis().SetTitle("<#hat{#sigma}>")
frame.GetYaxis().SetRangeUser(0.,0.30)
frame.Draw()
gr_up.Draw("FLsame")
gr.Draw("Psame")
pCMS1.Draw()
pCMS12.Draw()
pCMS2.Draw()
leg = TLegend()
leg = ROOT.TLegend(0.5,0.15,0.9,0.4)
leg.AddEntry(gr,"Inclusive p_{T}" ,"P")
leg.AddEntry(gr_up,"#pm 20% of inclusive p_{T}" ,"F")
leg.SetFillStyle(-1)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.04)
#pCMSt.Draw()

print 'shape of data',data.shape
for num,pt_bin in enumerate(pt_bins):
    data_bin = data.query(pt_bin)
    print pt_bin,data_bin.shape
    y_bin = (data_bin['Jet_mcPt']/(data_bin['Jet_pt_raw']*data_bin['Jet_corr_JEC'])).values.reshape(-1,1)
    res_bin = (data_bin['Jet_resolution_NN_%s'%input_trainings[0]])
    y_pred_bin = (data_bin['Jet_pt_reg_NN_%s'%input_trainings[0]]) #bad name because it is actually a correction
    # errors vector
    err_bin = y_bin[:,0]-y_pred_bin

    ##Draw IQR/2 vs resolution estimator
    res_bins, err_qt_res = utils.profile(err_bin,res_bin,bins=30,range=[0,0.3],moments=False,average=True) 
    err_iqr2 =  0.5*(err_qt_res[2]-err_qt_res[0])
    res_bins_array = array('d',res_bins)
    err_iqr2_array = array('d',err_iqr2)
    graphs.append(TGraph(len(res_bins),res_bins_array,err_iqr2_array))
    graphs[num].SetMarkerSize(1.8)
    graphs[num].SetMarkerColor(colors[num])
    graphs[num].SetMarkerStyle(markers[num])
    graphs[num].Draw("Psame")
    leg.AddEntry(graphs[num],"%s"%pt_bins_names[num] ,"P")

gr.Draw("Psame")
leg.Draw()
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
c.SaveAs(scratch_plots+savename+"_additional_pt_root.C"  )
c.SaveAs(scratch_plots+savename+"_additional_pt_root.root"  )
c.SaveAs(scratch_plots+savename+"_additional_pt_root.pdf"  )
