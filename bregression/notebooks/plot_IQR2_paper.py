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
from ROOT import TLatex

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
#scratch_plots ='/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/2017JECv32/June05/'   #for studies
savetag='August30_2019'
scratch_plots ='/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/paper/August30_2019/'  #for paper
dirs=['',input_trainings[0],options.samplename]
dirs=['',options.samplename]
for i in range(len(dirs)):
  scratch_plots=scratch_plots+'/'+dirs[i]+'/'
  if not os.path.exists(scratch_plots):
    os.mkdir(scratch_plots)
 

# ## Read test data and model
# load data
data = io.read_data('%s%s'%(options.inp_dir,options.inp_file),columns=None).query('Jet_pt>20')  # Jet pt 20 GeV was added after the final discussion with ARC
data.describe()
if options.where!='' : data = data.query(options.where)

#Regions of pt and eta 
file_regions = open('..//scripts/regionsPtEta.json')
regions_summary = json.loads(file_regions.read())
region_names = regions_summary['pt_regions']+regions_summary['eta_region_names']

#y = (data['Jet_mcPt']/data['Jet_pt']).values.reshape(-1,1)
y = (data['Jet_mcPt']/(data['Jet_pt_raw']*data['Jet_corr_JEC'])).values.reshape(-1,1)
X_pt = (data['Jet_pt_raw']).values.reshape(-1,1) 
#X_pt = (data['Jet_mcPt']).values.reshape(-1,1)  # For D.H. test
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

whats = ['p_T (GeV)','\eta','\\rho (GeV)']
whats_root = ['p_{T} (GeV)','#eta','#rho (GeV)']
#whats_root = ['p_{T}^{gen} (GeV)','#eta','#rho (GeV)'] # for D.H. test
ranges = [[30,400],[-3,3],[0,50]]
#ranges = [[150,400],[-3,3],[0,40]]  # gen for Phil
binning =[50,10,20] #[50,20]
for i in range(0,3):
#for i in range(0,1):
 if i==0 : X = X_pt
 elif i==1 : X = X_eta
 elif i==2 : X = X_rho
 print(i,X)
 
 bins=binning[i]
 if ('HHbbgg' in options.samplename) and ('p_T' in whats[i]) : 
      bins=int(binning[i]/3.)
      ranges[i] =  [50,400]
 if ('HHbbgg' in options.samplename) and ('rho' in whats[i]) : 
      bins=int(binning[i]/2.)
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

 if ('eta' in whats[i]) : 
     binc[0] = -2.5
     binc[-1] = 2.5
    

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
 for num,item in enumerate([gr25,gr40,gr50,gr75]) :
	item.SetLineStyle(5)
	item.SetLineWidth(3)
	item.SetLineColor(ROOT.kBlue)
 for num,item in enumerate([grcorr25,grcorr40,grcorr50,grcorr75]) :
	item.SetLineStyle(1)
	item.SetLineWidth(3)
	item.SetLineColor(ROOT.kRed)
# plt.text(xmin+abs(xmin)*0.05,ymax*0.98,'Quantiles : 0.25, 0.40, 0.50, 0.75', fontsize=30)

 samplename=options.samplename
 if options.samplename=='ttbar' : samplename='$t\\bar{t}$'
 if options.samplename=='ZHbbll' : samplename='$Z(\\to{bb})H(\\to{l^+l^-})$'
 if options.samplename=="HHbbggSM" : samplename='$H(\\to{bb})H(\\to{\gamma\gamma})$ SM'
 if options.samplename=="HHbbgg500" : samplename='$H(\\to{bb})H(\\to{\gamma\gamma})$ 500 GeV'
 if options.samplename=="HHbbgg700" : samplename='$H(\\to{bb})H(\\to{\gamma\gamma})$ 700 GeV'
 plt.text(xmin+abs(xmin)*0.05,ymax*0.96,'%s'%samplename, fontsize=30)
 
 plt.xlabel('$%s$'%whats[i], fontsize=30)
 plt.ylabel('$p_{T}^{gen} / p_{T}^{reco}$', fontsize=30)
 plt.legend(loc='upper right',fontsize=30)
 savename='/quantiles_col_%s_%s_%s_%s'%(input_trainings[0],whats[i].replace('\\','').replace(' ','').replace(')','').replace('(','').replace('-','_'),options.samplename,where)
# plt.savefig(scratch_plots+savename+savetag+'.png')
# plt.savefig(scratch_plots+savename+savetag+'.pdf')
 plt.clf()
 
### plot with ROOT : 
 c2 = ROOT.TCanvas("canvas%d"%i,"canvas%d"%i,900,900)
 c2.cd()
 frame = ROOT.TH1F("frame%d"%i,"",1,xmin,xmax)
 frame.SetStats(0)
 frame.GetXaxis().SetLabelSize(0.04)
 frame.GetYaxis().SetLabelSize(0.04)
 frame.GetYaxis().SetTitle("p_{T}^{gen} / p_{T}^{reco}")
 frame.GetXaxis().SetTitle(whats_root[i])
 frame.GetYaxis().SetRangeUser(ymin,ymax*1.1)
 frame.GetYaxis().SetRangeUser(0.85,1.35)
 if ('p_T') in whats[i] and 'HHbbgg' in options.samplename: frame.GetXaxis().SetLimits(30, 350)
 if ('p_T') in whats[i] and 'ttbar' in options.samplename: frame.GetXaxis().SetLimits(-20, 360)
# if ('p_T') in whats[i] and 'ttbar' in options.samplename: frame.GetXaxis().SetLimits(120, 370)  # for D.H. gen Phil test
 if ('rho') in whats[i] and 'ttbar' in options.samplename: frame.GetXaxis().SetLimits(-4, 47)
 if ('eta') in whats[i] and 'ttbar' in options.samplename: frame.GetXaxis().SetLimits(-3.6, 3.6)
 frame.Draw()
 for item in [gr25,gr40,gr50,gr75,grcorr25,grcorr40,grcorr50,grcorr75]:
# for item in [gr25,gr40,gr50,gr75,grcorr25,grcorr40,grcorr50,grcorr75,grmean,grcorrmean]:
     item.Draw("Lsame")

 
 if i==0: pName.AddText("%s"%samplename)

 leg = TLegend()
 leg = ROOT.TLegend(0.75,0.75,0.9,0.9)
# leg = ROOT.TLegend(0.6,0.75,0.9,0.9) # D.H. test
 leg.AddEntry(gr25,"Baseline" ,"L")
 leg.AddEntry(grcorr25,"DNN" ,"L")
# leg.AddEntry(grmean,"Baseline average" ,"L") # D.H. test
# leg.AddEntry(grcorrmean,"DNN average" ,"L") # D.H. test
 leg.SetFillStyle(-1)
 leg.SetBorderSize(0)
 leg.SetTextFont(42)
 leg.SetTextSize(0.04)
 leg.Draw()

 latex_posX_before = [-10,-3.45,-2.25]
 latex_posY_before = [[0.875,0.935,0.98,1.13],[0.9,0.955,0.985,1.1],[0.91,0.958,0.985,1.082]]
 latex_posX_after = [310.,2.65,40.5]
 latex_posY_after = [[0.94,0.97,1.00,1.055],[.94,1.0,1.04,1.175],[0.94,1.0,1.042,1.18]]
# latex_posX_before = [130,-3.,1.] #for D.H. test
# latex_posY_before = [[0.96,1.,1.05,1.14],[0.9,0.955,0.99,1.11],[0.915,0.965,0.994,1.094]]# D.H test
# latex_posX_after = [340.,2.6,40.] #D.H test 
# latex_posY_after = [[0.97,1,1.03,1.1],[.95,1.01,1.05,1.20],[0.95,1.01,1.055,1.205]]# D.H. test
 latex = TLatex()
 latex.SetTextFont(72)
# latex.SetTextFont(42)
 #latex.SetTextSize(0.028)
 latex.SetTextSize(0.04) #0.33
 latex.SetTextAlign(12)
 latex.SetTextColor(4)
 latex.DrawLatex(latex_posX_after[i],latex_posY_after[i][0],"25%")
 latex.DrawLatex(latex_posX_after[i],latex_posY_after[i][1],"40%")
 latex.DrawLatex(latex_posX_after[i],latex_posY_after[i][2],"50%")
 latex.DrawLatex(latex_posX_after[i],latex_posY_after[i][3],"75%")
 latex.SetTextColor(2)
 latex.DrawLatex(latex_posX_before[i],latex_posY_before[i][0],"25%")
 latex.DrawLatex(latex_posX_before[i],latex_posY_before[i][1],"40%")
 latex.DrawLatex(latex_posX_before[i],latex_posY_before[i][2],"50%")
 latex.DrawLatex(latex_posX_before[i],latex_posY_before[i][3],"75%")

 pCMS1.Draw()
 pCMS12.Draw()
 pCMS2.Draw()
# pCMSt.Draw()
 if options.samplename!='ttbar' : pName.Draw()
 ROOT.gPad.Update()
 ROOT.gPad.RedrawAxis()
 c2.SaveAs(scratch_plots+savename+savetag+"_root.C"  )
 c2.SaveAs(scratch_plots+savename+savetag+"_root.root"  )
 c2.SaveAs(scratch_plots+savename+savetag+"_root.pdf"  )





