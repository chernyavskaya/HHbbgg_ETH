import numpy as np
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
gStyle.SetPadLeftMargin(0.15)

savename='evolution'
sample_name = 'ttbar'
path2='/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/paper/%s/'%sample_name


parameters = array('d',[184009,728265,2829513,4930761])
bins = array('d',[-300000,360000,1300000,4100000,5700000])
validation = array('d',[0.411737,0.409737,0.409075,0.408875])
training = array('d',[ 0.415406,0.409928,0.407396,0.406751])
name_parameters = ['184k','727k','2.83M','4.93M']
 
gr_val = TGraph(len(parameters),parameters,validation)
gr_train = TGraph(len(parameters),parameters,training)
gr_train.SetMarkerStyle(20)
gr_train.SetMarkerColor(ROOT.kRed)
gr_val.SetMarkerStyle(22)
gr_val.SetMarkerColor(ROOT.kBlue)

for item in [gr_val,gr_train]:
	item.SetMarkerSize(1.9)

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
pCMS2.AddText("(13 TeV)")


pCMSt = ROOT.TPaveText(0.8,0.8,0.85,0.9,"NDC")
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
c.cd()
frame = ROOT.TH1F("frame","",4,bins)
frame.SetStats(0)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetYaxis().SetLabelSize(0.04)
frame.GetYaxis().SetTitle("error")
frame.GetXaxis().SetTitle("Number of trainable parameters")
frame.GetYaxis().SetRangeUser(0.40,0.42)
##
frame.GetXaxis().SetNdivisions(104)
frame.GetYaxis().SetNdivisions(104)
#axis = frame.GetXaxis()
#axis.SetNdivisions(0)
for i in range(0,len(parameters)):
	frame.GetXaxis().SetBinLabel(i+1,name_parameters[i]);
#

##
frame.Draw()
gr_train.Draw("Psame")
gr_val.Draw("Psame")
pCMS1.Draw()
#pCMS12.Draw()
#pCMS2.Draw()
#pCMSt.Draw()

leg = TLegend()
leg = ROOT.TLegend(0.7,0.75,0.9,0.9)
leg.AddEntry(gr_train,"Training" ,"P")
leg.AddEntry(gr_val,"Validation" ,"P")
leg.SetFillStyle(-1)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.04)
leg.Draw()



ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
c.SaveAs(path2+savename+"_root.png"  )
c.SaveAs(path2+savename+"_root.pdf"  )
