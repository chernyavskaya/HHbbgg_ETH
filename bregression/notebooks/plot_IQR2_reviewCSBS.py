import numpy as np
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
from ROOT import TLatex

gROOT.SetBatch(True)
gROOT.ProcessLineSync(".x /work/nchernya/setTDRStyle.C")
gROOT.ForceStyle()
gStyle.SetPadTopMargin(0.06)
gStyle.SetPadRightMargin(0.04)
gStyle.SetPadLeftMargin(0.19)


right,top   = gStyle.GetPadRightMargin(),gStyle.GetPadTopMargin()
left,bottom = gStyle.GetPadLeftMargin(),gStyle.GetPadBottomMargin()

pCMS1 = ROOT.TPaveText(left*1.1,1.-top*4,0.4,1.,"NDC") #without Preliminary
#pCMS1 = ROOT.TPaveText(left*1.1,1.-top*3.85,0.4,1.,"NDC") #with Preliminary
pCMS1.SetTextFont(62)
pCMS1.AddText("CMS")

pCMS12 = ROOT.TPaveText(left*1.1+0.1,1.-top*4,0.57,1.,"NDC")
pCMS12.SetTextFont(52)
pCMS12.AddText("Simulation")
#pCMS12.AddText("Simulation Preliminary")


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
    make_option("--inp-dir",type='string',dest="inp_dir",default='/work/nchernya/HHbbgg_ETH_devel/bregression/output_files/NN_psi_training/paper/'),
    make_option("--sample-name",type='string',dest="samplename",default='ttbar'),
    make_option("--where",type='string',dest="where",default=''),
])

## parse options
(options, args) = parser.parse_args()
input_trainings = options.training.split(',')

now = str(datetime.datetime.now()).split(' ')[0]
#scratch_plots ='/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/2017JECv32/June05/'   #for studies
savetag='March26_2020_CSBS'
scratch_plots ='/work/nchernya/HHbbgg_ETH_devel/bregression/plots/paper/March26_2020/'  #for paper
dirs=['',input_trainings[0],options.samplename]
dirs=['',options.samplename]
for i in range(len(dirs)):
  scratch_plots=scratch_plots+'/'+dirs[i]+'/'
  if not os.path.exists(scratch_plots):
    os.mkdir(scratch_plots)
 

# ## Read test data and model
# load data
data = io.read_data('%s%s'%(options.inp_dir,options.inp_file),columns=None).query('(Jet_pt>20) and (abs(Jet_eta)<0.5)')  # Jet pt 20 GeV was added after the final discussion with ARC
data.describe()
if options.where!='' : data = data.query(options.where)

#Regions of pt and eta 
file_regions = open('..//scripts/regionsPtEta.json')
regions_summary = json.loads(file_regions.read())
region_names = regions_summary['pt_regions']+regions_summary['eta_region_names']

#y = (data['Jet_mcPt']/data['Jet_pt']).values.reshape(-1,1)
y_gen = (data['Jet_mcPt']/(data['Jet_pt_raw']*data['Jet_corr_JEC'])).values.reshape(-1,1)
#y = (data['Jet_mcPt']/(data['Jet_pt_raw']*data['Jet_corr_JEC'])).values.reshape(-1,1)
y = ((data['Jet_pt_raw']*data['Jet_corr_JEC'])/data['Jet_mcPt']).values.reshape(-1,1)
X_pt = (data['Jet_pt_raw']).values.reshape(-1,1) 
#X_pt = (data['Jet_pt_raw']*data['Jet_corr_JEC']).values.reshape(-1,1) # test
#X_pt = (data['Jet_mcPt']).values.reshape(-1,1)  # For D.H. test
X_pt_jec = (data['Jet_pt_raw']*data['Jet_corr_JEC']).values.reshape(-1,1)
X_pt_gen = (data['Jet_mcPt']).values.reshape(-1,1)
X_eta = (data['Jet_eta']).values.reshape(-1,1)
X_rho = (data['rho']).values.reshape(-1,1)
res = (data['Jet_resolution_NN_%s'%input_trainings[0]]).values.reshape(-1,1)
y_pred = (data['Jet_pt_reg_NN_%s'%input_trainings[0]]) #bad name because it is actually a correction
y_corr = (y_gen[:,0]/y_pred).values.reshape(-1,1)
# errors vector
err = (y_gen[:,0]-y_pred).values.reshape(-1,1)

linestyles = ['-.', '--','-', ':']
where = (options.where).replace(' ','').replace('<','_').replace('>','_').replace('(','').replace(')','')

whats = ['p_T (GeV)','\eta','\\rho (GeV)']
whats_root = ['p_{T} (GeV)','#eta','#rho (GeV)']
#whats_root = ['p_{T}^{gen} (GeV)','#eta','#rho (GeV)'] # for D.H. test
ranges = [[50,400],[-3,3],[0,50]]
#ranges = [[150,400],[-3,3],[0,40]]  # gen for Phil
binning =[50,10,20] #[50,20]
#for i in range(0,3):
for i in range(0,1):
 if i==0 : X = X_pt
 elif i==1 : X = X_eta
 elif i==2 : X = X_rho
 print(i,X)
 
 bins=binning[i]
 if ('HHbbgg' in options.samplename) and ('p_T' in whats[i]) : 
      bins=int(binning[i]/3.)
      ranges[i] =  [50,400]
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


 _, _, _, y_qt_pt_gen = utils.profile(y,X_pt_gen,range=ranges[i],bins=bins,uniform=False,quantiles=np.array([0.25,0.4,0.5,0.75]))
 err_iqr2_gen =  0.5*(y_qt_pt_gen[3]-y_qt_pt_gen[0])

 _, _,_, y_corr_qt_pt_gen = utils.profile(y_corr,X_pt_gen,bins=bins,quantiles=np.array([0.25,0.4,0.5,0.75])) 
 err_corr_iqr2_gen =  0.5*(y_corr_qt_pt_gen[3]-y_corr_qt_pt_gen[0])

 binc = 0.5*(bins[1:]+bins[:-1])
####Calculate the improvement on IQR/2 ###
 iqr2_improvement = 2*(np.array(err_iqr2)-np.array(err_corr_iqr2))/(np.array(err_iqr2)+np.array(err_corr_iqr2))
 iqr2_rel_improvement = 2*(np.array(err_iqr2/y_40_pt)-np.array(err_corr_iqr2/y_corr_40_pt))/(np.array(err_iqr2/y_40_pt)+np.array(err_corr_iqr2/y_corr_40_pt))

 if ('eta' in whats[i]) : 
     binc[0] = -2.5
     binc[-1] = 2.5
    
 gr_iqr2_corr = TGraph(len(binc),array('d',binc),array('d',err_corr_iqr2))
 gr_iqr2 = TGraph(len(binc),array('d',binc),array('d',err_iqr2))
 gr_iqr2_corr_gen = TGraph(len(binc),array('d',binc),array('d',err_corr_iqr2_gen))
 gr_iqr2_gen = TGraph(len(binc),array('d',binc),array('d',err_iqr2_gen))

 plt.plot(binc,y_25_pt,label='baseline',linestyle=linestyles[0],color='b')
 gr25 = TGraph(len(binc),array('d',binc),array('d',y_25_pt))
 plt.plot(binc,y_corr_25_pt,label='DNN',linestyle=linestyles[2],color='r')
 grcorr25 = TGraph(len(binc),array('d',binc),array('d',y_corr_25_pt))
 plt.plot(binc,y_40_pt,linestyle=linestyles[0],color='b')
 gr40 = TGraph(len(binc),array('d',binc),array('d',y_40_pt))
 plt.plot(binc,y_corr_40_pt,linestyle=linestyles[2],color='r')
 grcorr40 = TGraph(len(binc),array('d',binc),array('d',y_corr_40_pt))
 plt.plot(binc,y_median_pt,linestyle=linestyles[0],color='b')
 gr50 = TGraph(len(binc),array('d',binc),array('d',y_median_pt))
 plt.plot(binc,y_corr_median_pt,linestyle=linestyles[2],color='r')
 grcorr50 = TGraph(len(binc),array('d',binc),array('d',y_corr_median_pt))
 plt.plot(binc,y_75_pt,linestyle=linestyles[0],color='b')
 gr75 = TGraph(len(binc),array('d',binc),array('d',y_75_pt))
 plt.plot(binc,y_corr_75_pt,linestyle=linestyles[2],color='r')
 grcorr75 = TGraph(len(binc),array('d',binc),array('d',y_corr_75_pt))

 grmean = TGraph(len(binc),array('d',binc),array('d',y_mean_pt))
 grcorrmean = TGraph(len(binc),array('d',binc),array('d',y_corr_mean_pt))
 for num,item in enumerate([grmean,grcorrmean]) :
	item.SetLineStyle(5)
	item.SetLineWidth(3)
	item.SetLineColor(ROOT.kGreen)
 for num,item in enumerate([grcorrmean]) :
	item.SetLineStyle(1)
 

 ymin, ymax = (plt.gca()).get_ylim()
 xmin, xmax = (plt.gca()).get_xlim()
 widths = [2,3,4,5]
 for num,item in enumerate([gr25,gr40,gr50,gr75,gr_iqr2_gen]) :
	item.SetLineStyle(1)
	item.SetLineWidth(3)
	item.SetLineColor(ROOT.kBlue)
 for num,item in enumerate([grcorr25,grcorr40,grcorr50,grcorr75,gr_iqr2_corr_gen]) :
	item.SetLineStyle(1)
	item.SetLineWidth(3)
	item.SetLineColor(ROOT.kRed)

 for num,item in enumerate([gr_iqr2]) :
	item.SetLineStyle(5)
	item.SetLineWidth(3)
	item.SetLineColor(ROOT.kAzure+6)
 for num,item in enumerate([gr_iqr2_corr]) :
	item.SetLineStyle(5)
	item.SetLineWidth(3)
	item.SetLineColor(ROOT.kOrange-3)

 import csv
 jetmet_x = []
 jetmet_y = []
 with open('/work/nchernya/HHbbgg_ETH_devel/bregression/inputs/JetMet_arx1107_4277_Fig34c_eta05.csv', 'rb') as csvfile :
   spamreader = csv.reader(csvfile, delimiter=',')
   for row in spamreader:
     jetmet_x.append(float(row[0]))
     jetmet_y.append(float(row[1]))

 print jetmet_x,jetmet_y

 gr_jetmet = TGraph(len(jetmet_x),array('d',jetmet_x),array('d',jetmet_y))
 gr_jetmet.SetLineStyle(1)
 gr_jetmet.SetLineWidth(3)
 gr_jetmet.SetLineColor(ROOT.kGreen+1)


### plot with ROOT : 
 savename_res='/resolution_IQR2_common_%s_%s_%s_%s'%(input_trainings[0],whats[i].replace('\\','').replace(' ','').replace(')','').replace('(','').replace('-','_'),options.samplename,where)
 c3 = ROOT.TCanvas("canvas%d"%i,"canvas%d"%i,900,900)
 c3.cd()
 c3.SetLogx()
 frame3 = ROOT.TH1F("frame3%d"%i,"",1,xmin,xmax)
 frame3.SetStats(0)
 frame3.GetXaxis().SetLabelSize(0.04)
 frame3.GetYaxis().SetLabelSize(0.04)
 frame3.GetYaxis().SetTitle("jet p_{T} resolution")
 frame3.GetXaxis().SetTitle(whats_root[i])
 frame3.GetYaxis().SetRangeUser(ymin,ymax*1.1)
 frame3.GetYaxis().SetRangeUser(0.,0.2) #without Preliminary
 frame3.GetXaxis().SetLimits(40, 500)
 frame3.Draw()
 gr_iqr2_corr_gen.Draw("Lsame")
 gr_iqr2_gen.Draw("Lsame")
 gr_iqr2_corr.Draw("Lsame")
 gr_iqr2.Draw("Lsame")
 gr_jetmet.Draw("Lsame")
 
 leg = TLegend()
 leg = ROOT.TLegend(0.45,0.65,0.8,0.85) #without Preliminary
 leg.AddEntry(gr_jetmet,"arx 1107.4277 PFJets, core fit" ,"L")
 leg.AddEntry(gr_iqr2_gen,"Baseline in p_{T}^{gen} bins, IQR/2" ,"L")
 leg.AddEntry(gr_iqr2_corr_gen,"DNN in p_{T}^{gen} bins, IQR/2" ,"L")
 leg.AddEntry(gr_iqr2,"Baseline in in p_{T}^{reco} bins, IQR/2" ,"L")
 leg.AddEntry(gr_iqr2_corr,"DNN in p_{T}^{reco} bins, IQR/2" ,"L")
 leg.SetFillStyle(-1)
 leg.SetBorderSize(0)
 leg.SetTextFont(42)
 leg.SetTextSize(0.03)
 leg.Draw()

# pCMS1.Draw()
# pCMS12.Draw()
 pCMS2.Draw()
 ROOT.gPad.Update()
 ROOT.gPad.RedrawAxis()
 c3.SaveAs(scratch_plots+savename_res+savetag+"_root.C"  )
 c3.SaveAs(scratch_plots+savename_res+savetag+"_root.root"  )
 c3.SaveAs(scratch_plots+savename_res+savetag+"_root.pdf"  )





