import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT
from ROOT import TCanvas, TH1F, TGraph
from ROOT import gROOT
from ROOT import gStyle
from optparse import OptionParser, make_option

gROOT.SetBatch(True)
gROOT.ProcessLineSync(".x /mnt/t3nfs01/data01/shome/nchernya/setTDRStyle.C")
gROOT.ForceStyle()
gStyle.SetPadTopMargin(0.06)
gStyle.SetPadRightMargin(0.04)
gStyle.SetPadLeftMargin(0.15)

parser = OptionParser(option_list=[
    make_option("--training",type='string',dest="training",default='2018-04-06_job23_2016'),
    make_option("--inp-file",type='string',dest='inp_file',default='applied_res_ttbar_RegressionPerJet_heppy_energyRings3_forTesting.hd5'),
    make_option("--inp-dir",type='string',dest="inp_dir",default='/scratch/nchernya/HHbbgg/paper/output_root/'),
    make_option("--sample-name",type='string',dest="samplename",default='ttbar'),
    make_option("--where",type='string',dest="where",default=''),
])

## parse options
(options, args) = parser.parse_args()

file = options.inp_file
training =options.training
path = options.inp_dir
sample_name = 'ttbar'
path2='/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/October06_2019_2016nanoAOD/%s/'%sample_name

data = pd.read_hdf('%s%s'%(path,file))
res =  data['Jet_pt_raw']*data['Jet_corr_JEC']*data['Jet_pt_reg_NN_%s'%training]
#res =  data['Jet_pt_raw']*data['Jet_corr_JEC']
print data['Jet_pt_reg_NN_%s'%training].values
res=np.array(res)
plt.hist(res,bins=200,normed=1,histtype='stepfilled')
axes = plt.gca()
axes.set_xlim(0,500)
plt.grid(alpha=0.2,linestyle='--',markevery=2)
ymin, ymax = (axes).get_ylim()
xmin, xmax = (axes).get_xlim()
samplename='$t\\bar{t}$'
plt.text(xmax*0.8,ymax*0.85,r'%s'%samplename, fontsize=30)
plt.xlabel(r'$\hat{\sigma}$',fontsize=30)
plt.ylabel('A.U.',fontsize=30)
savename='pt_%s'%sample_name
plt.savefig(path2+savename+'.pdf')
plt.savefig(path2+savename+'.png')


#####Plot with ROOT#####
Rhist = TH1F('res','res',200,0,500)
for i in res:
   Rhist.Fill(i)
Rhist.Scale(1./Rhist.Integral())



Rhist.SetLineWidth(2)
Rhist.SetLineColor(1)
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


pCMSt = ROOT.TPaveText(0.8,1.-top*4,0.85,1,"NDC")
pCMSt.SetTextFont(42)
pCMSt.AddText("t#bar{t}")

for item in [pCMSt,pCMS2,pCMS12,pCMS1]:
	item.SetTextSize(top*0.75)
	item.SetTextAlign(12)
	item.SetFillStyle(-1)
	item.SetBorderSize(0)

for item in [pCMS2]:
	item.SetTextAlign(32)


c = ROOT.TCanvas("c","c",900,900)


c = ROOT.TCanvas("c","c",900,900)
c.cd()
frame = ROOT.TH1F("frame","",1,xmin,xmax)
frame.SetStats(0)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetYaxis().SetLabelSize(0.04)
frame.GetYaxis().SetTitle("A.U.")
frame.GetXaxis().SetTitle("Jet pT (GeV)")
frame.GetYaxis().SetRangeUser(0.,Rhist.GetMaximum()*1.2)
frame.Draw()
Rhist.Draw("Hsame")
pCMS1.Draw()
pCMS12.Draw()
pCMS2.Draw()
pCMSt.Draw()

ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
savename='pt_%s'%sample_name
c.SaveAs(path2+savename+"_root.png"  )
c.SaveAs(path2+savename+"_root.pdf"  )
