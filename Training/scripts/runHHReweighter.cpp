#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TString.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TDirectory.h"
#include "TLorentzVector.h"
#include <map>
#include <fstream>
#include "HHReweight5D.h"

using namespace std;

//c++ -lm -o runHH runHHReweighter.cpp HHReweight5D.cpp `root-config --glibs --cflags`
int main ()
{
	 TString ending = "18092019";
    TString inputDir = "/shome/nchernya/HHbbgg_ETH_devel/root_files/HHreweighting_18_09_2019/";
	TString tag = "2016";
    TString filename = "output_GluGluToHHTo2B2G_node_all_merged_2016.root"; //2016
  //  TString tag = "2018";
 //   TString filename = "output_GluGluToHHTo2B2G_node_all_merged_2018.root"; //2017

    TFile* fIn = TFile::Open(inputDir+filename);
	 TTree* ch = (TTree*)fIn->Get("GluGluToHHTo2B2G_mixnodes_GenAll"); 

    float   leadPho_px, leadPho_py, leadPho_pz, leadPho_e;
    float   subleadPho_px, subleadPho_py, subleadPho_pz, subleadPho_e;
    float   leadJet_px, leadJet_py, leadJet_pz, leadJet_e;
    float   subleadJet_px, subleadJet_py, subleadJet_pz, subleadJet_e;
	 float mbb, mgg, mhh;
 
    ch->SetBranchAddress("leadPho_px", &leadPho_px);
    ch->SetBranchAddress("leadPho_py", &leadPho_py);
    ch->SetBranchAddress("leadPho_pz", &leadPho_pz);
    ch->SetBranchAddress("leadPho_e", &leadPho_e);
    ch->SetBranchAddress("subleadPho_px", &subleadPho_px);
    ch->SetBranchAddress("subleadPho_py", &subleadPho_py);
    ch->SetBranchAddress("subleadPho_pz", &subleadPho_pz);
    ch->SetBranchAddress("subleadPho_e", &subleadPho_e);

    ch->SetBranchAddress("leadJet_px",&leadJet_px);
    ch->SetBranchAddress("leadJet_py", &leadJet_py);
    ch->SetBranchAddress("leadJet_pz", &leadJet_pz);
    ch->SetBranchAddress("leadJet_e", &leadJet_e);
    ch->SetBranchAddress("subleadJet_px", &subleadJet_px);
    ch->SetBranchAddress("subleadJet_py", &subleadJet_py);
    ch->SetBranchAddress("subleadJet_pz", &subleadJet_pz);
    ch->SetBranchAddress("subleadJet_e", &subleadJet_e);

    ch->SetBranchAddress("mgg", &mgg);
    ch->SetBranchAddress("mbb", &mbb);
    ch->SetBranchAddress("mhh", &mhh);

    // // must be same binning as Xanda!
    // new binning for dynamic reweight -- again these weird Xanda binnings
    TString inMapFile   = "outMap_5Dbinning_"+tag+".root" ;
    TFile* fOut = new TFile (inputDir+inMapFile, "recreate");
    double binning_mHH [56] = { 250,260,270,280,290,300,310,320,330,340,
                                350,360,370,380,390,400,410,420,430,440, 
                                450,460,470,480,490,
                                500,510,520,530,540,550,600,610,620,630,
                                640,650,660,670,680,690,700,750,800,850,
                                900,950,1000,1100,1200,1300,1400,1500.,1750,2000,50000};
    double binning_cth [5]  = {0.0, 0.4, 0.6, 0.8, 1.0} ;

    int nbins_mHH = 55; // size of arrays - 1
    int nbins_cth = 4;  // size of arrays - 1
    TString inHistoName = "allHHNodeMap2D";
    TH2F* hMap = new TH2F (inHistoName, inHistoName, nbins_mHH, binning_mHH, nbins_cth, binning_cth );
    TH1F* hMap1D = new TH1F ("allHHNodeMap1D", "allHHNodeMap1D", nbins_mHH, binning_mHH);

    TLorentzVector vPho1,vPho2,vJet1,vJet2, vH1, vH2, vBoost, vSum;
    TLorentzVector hh,h_1;
    for (int iEv = 0; iEv<ch->GetEntries(); ++iEv)
    {
        ch->GetEntry(iEv);
        if (iEv % 100000 == 0) cout << "Event: " << iEv << endl;

        vPho1.SetPxPyPzE (leadPho_px, leadPho_py,leadPho_pz,leadPho_e );
        vPho2.SetPxPyPzE (subleadPho_px, subleadPho_py,subleadPho_pz,subleadPho_e );
        vJet1.SetPxPyPzE (leadJet_px, leadJet_py,leadJet_pz,leadJet_e );
        vJet2.SetPxPyPzE (subleadJet_px, subleadJet_py,subleadJet_pz,subleadJet_e );

        vH1 = vPho1 + vPho2;
        vH2 = vJet1 + vJet2;
        vSum = vH1+vH2;
        float mHH = vSum.M();
        vH1.Boost(-vSum.BoostVector());                     
        float ct1 = vH1.CosTheta();
        hMap->Fill(mHH, TMath::Abs(ct1));
        hMap1D->Fill(mHH);
    }
   fOut->cd();
   hMap->Write();
   hMap1D->Write();
	fIn->Close();
   fOut->Close();
//////////////////////////////////////////Preapre reweighting file with histograms that we will pass to flashgg///////////////////////////////////////

    string coeffFile  = "coefficientsByBin_extended_3M_costHHSim_19-4.txt";
    cout << "** INFO: reading histo named: " << inHistoName << " from file: " << inMapFile << endl;
    cout << "** INFO: HH reweight coefficient file is: " << coeffFile << endl;
    TFile* fHHDynamicRew = new TFile(inputDir+inMapFile);
    
    TH2* hhreweighterInputMap =  (TH2*) fHHDynamicRew->Get(inHistoName);
    
    HHReweight5D* hhreweighter;
    hhreweighter = new HHReweight5D(((string)inputDir).append(coeffFile), hhreweighterInputMap,inputDir);
  //  float HHweight = hhreweighter->getWeight(7.5, 1.0, -1.0, 0., 0., 300., 0.5);
  //  cout<<"I got the weight : "<<HHweight<<endl;

///////////////////////////////////Now only need to hadd two root files with histograms/////////////////// 	
cout<<"!!!!!!!!!!!!!!!!!!!!!Now you just need to hadd two histograms files :!!!!!!!!!!!!!!!!!!!!"<<endl;
cout<<"hadd "<<inputDir<<"HHreweight_"<<tag<<"nodes_"<<ending<<".root   "<<inputDir<<inMapFile<< "      "<<inputDir<<"HHReweight_histograms.root"<<endl;


}

