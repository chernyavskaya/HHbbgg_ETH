import ROOT
from ROOT import TFile, TTree, gStyle, TF1, gROOT

gROOT.SetBatch(True)
gROOT.ProcessLineSync(".x /mnt/t3nfs01/data01/shome/nchernya/setTDRStyle.C")
gROOT.ForceStyle()
gStyle.SetPadTopMargin(0.06)
gStyle.SetPadRightMargin(0.04)
gStyle.SetPadLeftMargin(0.15)

what ='Jet_pt'
#what ='Jet_eta'
#what ='target'
what_name=''
if what=='Jet_pt' :  
	bins=100
	xmin=0
	xmax=1200
	what_name = 'p_{T}^{reco} (GeV)'
if what=='Jet_eta' :
	bins=50
	xmin=-5
	xmax=5
	what_name = '#eta'
if what=='target' :
	what='Jet_mcPt/(Jet_pt*Jet_rawEnergy/Jet_e*Jet_corr)'
	bins=50
	xmin=0
	xmax=2
	what_name = 'p_{T}^{gen} / p_{T}^{reco}'


right,top   = gStyle.GetPadRightMargin(),gStyle.GetPadTopMargin()
left,bottom = gStyle.GetPadLeftMargin(),gStyle.GetPadBottomMargin()

#pCMS1 = ROOT.TPaveText(left*1.1,1.-top*3.85,0.4,1.,"NDC") #with Preliminary
pCMS1 = ROOT.TPaveText(left*1.1,1.-top*4,0.4,1.,"NDC") #without Preliminary
pCMS1.SetTextFont(62)
pCMS1.AddText("CMS")

pCMS12 = ROOT.TPaveText(left*1.1+0.1,1.-top*4,0.57,1.,"NDC")
pCMS12.SetTextFont(52)
pCMS12.AddText("Simulation")
#pCMS12.AddText("Simulation Preliminary")



pCMS2 = ROOT.TPaveText(0.5,1.-top,1.-right*0.5,1.,"NDC")
pCMS2.SetTextFont(42)
pCMS2.AddText("(13 TeV)")


pCMSt = ROOT.TPaveText(0.84,1.-top*3.7,0.9,1,"NDC")
pCMSt.SetTextFont(42)
pCMSt.AddText("t#bar{t}")

for item in [pCMSt,pCMS2,pCMS12,pCMS1]:
	item.SetTextSize(top*0.75)
	item.SetTextAlign(12)
	item.SetFillStyle(-1)
	item.SetBorderSize(0)

for item in [pCMS2]:
	item.SetTextAlign(32)


name="/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/root_files/heppy_05_10_2017/ttbar_RegressionPerJet_heppy_energyRings3_forTraining_LargeAll.root"
f = TFile.Open(name, "read")

t = f.Get("tree")
hist = ROOT.TH1F("hist","hist",bins,xmin,xmax)
hist.SetLineWidth(2)
hist.SetLineColor(ROOT.kAzure-3)
hist.SetFillColor(ROOT.kAzure+7)
hist.SetFillStyle(3005)

c = ROOT.TCanvas("c","c",900,900)
c.SetLogy() # for pt
#c.SetBottomMargin(0.3)
#cuts='(Jet_pt > 20) & (Jet_mcFlavour==5 | Jet_mcFlavour==-5) & (Jet_eta<2.5 & Jet_eta>-2.5) & (Jet_mcPt>0) & (Jet_mcPt<6000)'
cuts='(Jet_pt > 20) & (Jet_mcFlavour==5 | Jet_mcFlavour==-5) & (Jet_mcPt>0) & (Jet_mcPt<6000)'
t.Draw("%s>>hist"%what,cuts)
frame = ROOT.TH1F("hframe", "hframe", 1000, xmin,xmax)
frame.SetStats(0)
frame.GetXaxis().SetLabelSize(0.04)
frame.GetXaxis().SetTitle("%s"%what_name)
frame.GetYaxis().SetTitle("Normalized to Unity")
frame.GetYaxis().SetLabelSize(0.04)
hist.Scale(1./hist.Integral())
#frame.GetYaxis().SetRangeUser(1e-01,hist.GetMaximum()*30) #pt
frame.GetYaxis().SetRangeUser(1e-08,hist.GetMaximum()*30) #pt norm without preliminary
#frame.GetYaxis().SetRangeUser(1e-08,hist.GetMaximum()*30) #pt norm with preliminary
#frame.GetYaxis().SetRangeUser(1e-01,hist.GetMaximum()*1.05) #target
#frame.GetYaxis().SetRangeUser(1e-03,hist.GetMaximum()*1.15) #target norm with preliminary
#frame.GetYaxis().SetRangeUser(1e-03,hist.GetMaximum()*1.05) #target norm without preliminary
frame.Draw()
hist.Draw("same")
pCMS1.Draw()
pCMS12.Draw()
pCMS2.Draw()
pCMSt.Draw()
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()
name="../plots/paper/bjet_spectrum_%s_filled_paper"%what_name.replace(' ','').replace('{','').replace('}','').replace('^','').replace('/','').replace('#','').replace('(','').replace(')','')
c.SaveAs(name+'.pdf')
c.SaveAs(name+'.C')
c.SaveAs(name+'.root')
