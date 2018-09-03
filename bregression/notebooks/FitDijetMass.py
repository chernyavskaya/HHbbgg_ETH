import numpy as np
import json
import pandas as pd

import ROOT
import math
from array import array
from ROOT import std
from ROOT import gROOT
from ROOT import gStyle
from ROOT import TH1F, TGraph, TF1, THStack
from ROOT import TCanvas
from ROOT import RooRealVar, RooDataHist, RooFormulaVar, RooVoigtian, RooChebychev, RooArgList,                  RooArgSet, RooAddPdf, RooDataSet, RooCategory, RooSimultaneous,                  RooBreitWigner, RooCBShape, RooFFTConvPdf, RooBukinPdf, RooBifurGauss, RooGenericPdf, RooChi2Var, RooBernstein

import matplotlib.pyplot as plt
from optparse import OptionParser, make_option

parser = OptionParser(option_list=[
    make_option("--cut",type='string',dest="cut",default=''),
])

## parse options
(options, args) = parser.parse_args()

out_dir = '/scratch/nchernya/HHbbgg/paper/output_root/'
filename = 'ZHbll_dijetmass_pt_per_event'
cut_name = options.cut
data=pd.read_hdf(out_dir+filename+'.hd5',columns=None)

if cut_name!='' : data = data.query(cut_name)

bins = np.linspace(50, 200, 100)
n,bins,patches = plt.hist(data[data.dijetM > 0]['dijetM'],bins=bins,color='blue',alpha=0.5)
n,bins,patches = plt.hist(data[data.dijetM_reg > 0]['dijetM_reg'],bins=bins,color='red',alpha=0.5)




def fit_dijetmass(rel_diff_regressed,rel_diff,style=True,n_bins=100,outString=None):
    if style==True:
        gROOT.SetBatch(True)
        gROOT.ProcessLineSync(".x ~/HHbbgg_ETH/scripts/setTDRStyle.C")
        gROOT.ForceStyle()
        gStyle.SetPadTopMargin(0.06)
        gStyle.SetPadRightMargin(0.04)
        gStyle.SetPadLeftMargin(0.15)

    c_min = min(min(rel_diff_regressed),min(rel_diff))
    c_max = max(max(rel_diff_regressed),max(rel_diff))
    c_min=50.
    c_max=200.

    Histo_rel_diff = np.histogram(rel_diff,bins=n_bins,range=(c_min,c_max))
    Histo_rel_diff_reg = np.histogram(rel_diff_regressed,bins=n_bins,range=(c_min,c_max))

    h_rel_diff = TH1F("hrel_diff", "hrel_diff", n_bins, c_min, c_max)
    for i in range(len(rel_diff)):
        h_rel_diff.Fill(rel_diff[i])
    h_rel_diff_reg = TH1F("hrel_diff_reg", "hrel_diff_reg", n_bins, c_min, c_max)
    for i in range(len(rel_diff_regressed)):
        h_rel_diff_reg.Fill(rel_diff_regressed[i])
    h_rel_diff_reg.SetLineColor(ROOT.kBlue+1)
    h_rel_diff_reg.SetMarkerColor(ROOT.kBlue+1)
    h_rel_diff_reg.SetMarkerStyle(20)
    h_rel_diff_reg.SetFillColor(ROOT.kBlue-10);
    h_rel_diff_reg.SetFillStyle(1001)
    h_rel_diff_reg.SetLineWidth(2)
    h_rel_diff.SetLineColor(ROOT.kRed)
    h_rel_diff.SetMarkerColor(ROOT.kRed)
    h_rel_diff.SetMarkerStyle(20)
    h_rel_diff.SetLineWidth(2)

    h_rel_diff_fine = TH1F("hrel_diff_fine", "hrel_diff_fine", 200, c_min, c_max)
    h_rel_diff_reg_fine = TH1F("hrel_diff_reg_fine", "hrel_diff_reg_fine", 200, c_min, c_max)
    for i in range(len(rel_diff)):
        h_rel_diff_fine.Fill(rel_diff[i])
    for i in range(len(rel_diff_regressed)):
        h_rel_diff_reg_fine.Fill(rel_diff_regressed[i])

    AllHistos= [Histo_rel_diff, Histo_rel_diff_reg]
    h_max = max([histo[0].max() for histo in AllHistos])*1.2
    h_min = min([histo[0].min() for histo in AllHistos])

    c = ROOT.TCanvas("c","c",900,900)
    c.cd()
    frame = TH1F("hframe", "hframe", n_bins, c_min, c_max)
    frame.SetStats(0)
    frame.GetXaxis().SetTitleOffset(0.91);
    frame.GetYaxis().SetTitle("Events")
    frame.GetXaxis().SetTitle("M(bb) (GeV)")
    frame.GetYaxis().SetLabelSize(0.04)
    frame.GetYaxis().SetRangeUser(h_min,h_max)

    frame.Draw()
    h_rel_diff.Draw("samePE")
    h_rel_diff_reg.Draw("samePE")
    y0,x0       = h_rel_diff.GetMaximum(),h_rel_diff.GetXaxis().GetBinCenter(h_rel_diff.GetMaximumBin())
  #  x1,x2       = h_rel_diff.GetBinCenter(h_rel_diff.FindFirstBinAbove(y0/2.)),h_rel_diff.GetBinCenter(h_rel_diff.FindLastBinAbove((y0/2.)))
    x1,x2       = h_rel_diff_fine.GetBinCenter(h_rel_diff_fine.FindFirstBinAbove(h_rel_diff_fine.GetBinContent(h_rel_diff_fine.FindBin(x0))/2.)),h_rel_diff_fine.GetBinCenter(h_rel_diff_fine.FindLastBinAbove( h_rel_diff_fine.GetBinContent(h_rel_diff_fine.FindBin(x0))/2.))
    fwhm0        = x2-x1
    y0_reg,x0_reg       = h_rel_diff_reg.GetMaximum(),h_rel_diff_reg.GetXaxis().GetBinCenter(h_rel_diff_reg.GetMaximumBin())
  #  x1_reg,x2_reg       = h_rel_diff_reg.GetBinCenter(h_rel_diff_reg.FindFirstBinAbove(y0_reg/2.)),h_rel_diff_reg.GetBinCenter(h_rel_diff_reg.FindLastBinAbove((y0_reg/2.)))
    x1_reg,x2_reg       = h_rel_diff_reg_fine.GetBinCenter(h_rel_diff_reg_fine.FindFirstBinAbove(h_rel_diff_reg_fine.GetBinContent(h_rel_diff_reg_fine.FindBin(x0_reg))/2.)),h_rel_diff_reg_fine.GetBinCenter(h_rel_diff_reg_fine.FindLastBinAbove( h_rel_diff_reg_fine.GetBinContent(h_rel_diff_reg_fine.FindBin(x0_reg))/2.))
    fwhm_reg0        = x2_reg-x1_reg
    print('Nominal : mean, RMS, fwhm :',h_rel_diff.GetMean(), h_rel_diff.GetRMS(),fwhm0)
    print('Regresesd : mean, RMS,fwhm : ',h_rel_diff_reg.GetMean(), h_rel_diff_reg.GetRMS(),fwhm_reg0)


    plotFolder='/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/bregression/plots/paper/ZHbbll/'



    leg = ROOT.TLegend(0.55,0.75,0.9,0.9)
    leg.SetFillStyle(-1)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.03)
  #  leg.Draw()


    h_names = ['nom','reg']
    datahists = [h_rel_diff,h_rel_diff_reg]
    x=[]
    datahist=[]
    m=[]
    m_initial=[110,120]
    s=[]
    s_initial=[ 18.210,16.967]
    a=[]
    a_initial=[1.,1.]
    n=[]
    n_initial=[ 1.,1.]

    Ap,Xp,sigp,xi,rho1,rho2 = [],[],[],[],[],[]
    Xp_initial,sigp_initial,xi_initial,rho1_initial,rho2_initial =  120., 17.11,-0.196063,-0.0991912,  0.215238
    meanr, sigmaL, sigmaR, alphaL, alphaR = [],[],[],[],[]

    fsig=[]
    sig=[]
    bkg=[]
    signal=[]
    model=[]
    res=[]
    integral=[]
    b0,b1,b2,b3 = [],[],[],[]
    formula=[]
    scale_factors=[]
    scaled_cb=[]
    func=[]
    colors=[ROOT.kBlue,ROOT.kRed]
    chi_squares=[]
    fwhm_bukin=[]
    fwhm=[]
    fwhm.append( -1 *(h_rel_diff.GetBinCenter( h_rel_diff.FindFirstBinAbove(h_rel_diff.GetMaximum()/2.)  )  - h_rel_diff.GetBinCenter( h_rel_diff.FindLastBinAbove(h_rel_diff.GetMaximum()/2.) ) )  )
    fwhm.append( -1 *(h_rel_diff_reg.GetBinCenter( h_rel_diff_reg.FindFirstBinAbove(h_rel_diff_reg.GetMaximum()/2.)  )  - h_rel_diff_reg.GetBinCenter( h_rel_diff_reg.FindLastBinAbove(h_rel_diff_reg.GetMaximum()/2.) ) )  )
    print("FWHM = %.4f,%.4f "%(fwhm[0],fwhm[1])) 


    for num,h in enumerate(h_names):
        x.append(RooRealVar("x_%s"%h,"x_%s"%h,c_min,c_max))
        datahist.append(RooDataHist("roohist_%s"%h,"roohist_%s"%h,RooArgList(x[num]),datahists[num]))

      #######################Bukin function ##################
        Xp.append(RooRealVar("Xp_%s"%h,"Xp_%s"%h,Xp_initial,110,130.))
        sigp.append(RooRealVar("sigp_%s"%h,"sigp_%s"%h,sigp_initial,12,23))
        xi.append(RooRealVar("xi_%s"%h,"xi_%s"%h,xi_initial,-1,1))
        rho1.append(RooRealVar("rho1_%s"%h,"rho1_%s"%h,rho1_initial,-1,1)) #left
        rho2.append(RooRealVar("rho2_%s"%h,"rho2_%s"%h,rho2_initial,-1,1)) #right
        sig.append(RooBukinPdf("signal_bukin_%s"%h,"signal_bukin_%s"%h,x[num],Xp[num],sigp[num],xi[num],rho1[num],rho2[num]))
       #######################Crystal ball################ 
        m.append(RooRealVar("mean_%s"%h,"mean_%s"%h,m_initial[num],110,130))
        s.append(RooRealVar("sigma_%s"%h,"sigma_%s"%h,s_initial[num],7,30))
        a.append(RooRealVar("alpha_%s"%h,"alpha_%s"%h,a_initial[num],-5,5.))
        n.append(RooRealVar("exp_%s"%h,"exp_%s"%h,n_initial[num],0.,100.))
        b0.append(RooRealVar("b0_%s"%h,"b0_%s"%h,0.1,0.,1.))
        b1.append(RooRealVar("b1_%s"%h,"b1_%s"%h,0.1,0.,1.))
        b2.append(RooRealVar("b2_%s"%h,"b2_%s"%h,0.01,0.,1.))
        b3.append(RooRealVar("b3_%s"%h,"b3_%s"%h,0.01,0.,1.))
        bkg.append(RooBernstein("signal_bkg_%s"%h, "signal_bkg_%s"%h ,x[num],RooArgList(b0[num],b1[num],b2[num],b3[num])))
        fsig.append(RooRealVar("fsig_%s"%h,"fsig_%s"%h,0.8,0.5,1.))
        signal.append(RooCBShape("signal_gauss_%s"%h,"signal_gauss_%s"%h,x[num],m[num],s[num],a[num],n[num]))
      #  sig.append(RooAddPdf("signal_model_%s"%h, "signal_model_%s"%h ,RooArgList(signal[num],bkg[num]),RooArgList(fsig[num])))

        res.append(sig[num].fitTo(datahist[num],ROOT.RooFit.Save(ROOT.kTRUE)))
        res[num].Print()

       # chi_squares.append((x[num].frame()).chiSquare())
        x[num].setRange("integralRange%s"%h, c_min,c_max)
        integral.append(sig[num].createIntegral(RooArgSet(x[num]), ROOT.RooFit.Range("integralRange%s"%h)))

        scale_factors.append(datahists[num].Integral()*datahists[num].GetBinWidth(1)/integral[num].getVal())
        scale_factors.append(datahists[num].Integral()*datahists[num].GetBinWidth(1)/integral[num].getVal())
      #  formula.append("%f *signal_gauss_%s"%(scale_factors[num],h))
        formula.append("%f *signal_bukin_%s"%(scale_factors[num],h))
       # formula.append("%f *signal_model_%s"%(scale_factors[num],h))
     #   formula.append("%f *signal_cruijff_%s"%(scale_factors[num],h))
       # create a scaled  function = scale * function
        scaled_cb.append(RooFormulaVar("scaled_cb_%s"%h,formula[num],RooArgList(sig[num])))
        func.append(scaled_cb[num].asTF(RooArgList(x[num])))
        func[num].SetLineColor(colors[num])
      #  datahists[num].SetMarkerColor(colors[num])
      #  fwhm_bukin.append(sigp[num].getVal()*2*math.sqrt(2*math.log(2)))

      #  chi_squares.append(RooChi2Var("chi2_%s"%h,"chi2_%s"%h,sig[num],datahist[num]))


    fitfunc='Bukin'
 #   fitfunc='CB_pol'
    fit_result_file = std.ofstream(plotFolder+"/fitResult_%s"%(fitfunc)+str(outString)+'.txt')
    res[0].floatParsFinal().printMultiline(fit_result_file, 1111, True)
    res[1].floatParsFinal().printMultiline(fit_result_file, 1111, True)
    fit_result_file.close()

    txt_file = open(plotFolder+"/mean_fwhm_"+str(outString)+'.txt','w')
    txt_file.write('Nominal : mean, RMS, fwhm : %.4f,%.4f,%.4f\n'%(h_rel_diff.GetMean(), h_rel_diff.GetRMS(),fwhm0))
    txt_file.write('Regressed : mean, RMS,fwhm : %.4f,%.4f,%.4f\n'%(h_rel_diff_reg.GetMean(), h_rel_diff_reg.GetRMS(),fwhm_reg0))
    improvement = (fwhm_reg0/h_rel_diff_reg.GetMean() - fwhm0/h_rel_diff.GetMean())/(fwhm_reg0/h_rel_diff_reg.GetMean() + fwhm0/h_rel_diff.GetMean())*2
    improvement_Xp = (fwhm_reg0/Xp[1].getVal() - fwhm0/Xp[0].getVal())/(fwhm_reg0/Xp[1].getVal() + fwhm0/Xp[0].getVal())*2
    improvement_x0 = (fwhm_reg0/x0_reg - fwhm0/x0)/(fwhm_reg0/x0_reg + fwhm0/x0)*2
    improvement_x0_jec = (fwhm_reg0/x0_reg - fwhm0/x0)/(fwhm0/x0)
    txt_file.write('Improvement FWHM/Mean: %.4f\n'%improvement)
    txt_file.write('Improvement FWHM/Xp : %.4f\n'%improvement_Xp)
    txt_file.write('Improvement FWHM/Peak : %.4f\n'%improvement_x0)
    txt_file.write('Improvement FWHM/Peak wrt JEC : %.4f\n'%improvement_x0_jec)
    txt_file.close()


    leg.AddEntry(h_rel_diff,"Nominal JEC" ,"P")
    leg.AddEntry(h_rel_diff_reg,"Regressed" ,"P")


    c2 = ROOT.TCanvas("c2","c2",900,900)
    c2.cd()
    frame.Draw()
 #   func[0].Draw("same")
 #   func[1].Draw("same")
    hS_reg = THStack("hS_reg","hS_reg")
    hS_reg.Add(h_rel_diff_reg)
    hS_reg.Draw("same,hist")
    hS = THStack("hs","hs")
    hS.Add(h_rel_diff)
    hS.Draw("same,hist")
    ROOT.gPad.RedrawAxis()
    h_rel_diff.Draw("PEHISTsame")
    h_rel_diff_reg.Draw("PEHISTsame")
    leg.Draw()

    c2.SaveAs(plotFolder+"dijet_%s_"%(fitfunc)+str(outString)+'_root.png')
    c2.SaveAs(plotFolder+"dijet_%s_"%(fitfunc)+str(outString)+'_root.pdf')
    c2.Draw()


style=True
fit_dijetmass(data[data.dijetM_reg > 0]['dijetM_reg'].values.reshape(-1,1),data[data.dijetM > 0]['dijetM'].values.reshape(-1,1),style,50,cut_name)

