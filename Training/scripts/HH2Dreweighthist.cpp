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

using namespace std;

//c++ -lm -o MakeMap MakeMap.cpp `root-config --glibs --cflags`

// open input txt file and append all the files it contains to TChain


int main ()
{
	//	TString tag = "2016";
  //  TString filedir = "/shome/nchernya/HHbbgg_ETH_devel/root_files/HHreweighting_01_02_2018/"; //2016
  //  TString filename = "output_GluGluToHHTo2B2G_mix12nodes_13TeV-madgraph.root"; //2016
    TString tag = "2017";
    TString filedir = "/shome/nchernya/HHbbgg_ETH_devel/root_files/HHreweighting_01_02_2018/"; //2017
    TString filename = "output_GluGluToHHTo2B2G_mix6nodes_13TeV-madgraph_2017.root"; //2017

    TFile* fIn = TFile::Open(filedir+filename);
	// TTree* ch = (TTree*)fIn->Get("GluGluToHHTo2B2G_mix12nodes_GenAll"); //2016
	 TTree* ch = (TTree*)fIn->Get("GluGluToHHTo2B2G_mixnodes_GenAll"); //2017


    float   leadPho_px;
    float   leadPho_py;
    float   leadPho_pz;
    float   leadPho_e;
    float   subleadPho_px;
    float   subleadPho_py;
    float   subleadPho_pz;
    float   subleadPho_e;
   
    float   leadJet_px;
    float   leadJet_py;
    float   leadJet_pz;
    float   leadJet_e;
    float   subleadJet_px;
    float   subleadJet_py;
    float   subleadJet_pz;
    float   subleadJet_e;

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
    TFile* fOut = new TFile (filedir+"outMap_5Dbinning_"+tag+".root", "recreate");
    double binning_mHH [56] = { 250,260,270,280,290,300,310,320,330,340,
                                350,360,370,380,390,400,410,420,430,440, 
                                450,460,470,480,490,
                                500,510,520,530,540,550,600,610,620,630,
                                640,650,660,670,680,690,700,750,800,850,
                                900,950,1000,1100,1200,1300,1400,1500.,1750,2000,50000};
    double binning_cth [5]  = {0.0, 0.4, 0.6, 0.8, 1.0} ;

    int nbins_mHH = 55; // size of arrays - 1
    int nbins_cth = 4;  // size of arrays - 1
    TH2F* hMap = new TH2F ("allHHNodeMap", "allHHNodeMap", nbins_mHH, binning_mHH, nbins_cth, binning_cth );
    TH1F* hMap1D = new TH1F ("allHHNodeMap1D", "allHHNodeMap1D", nbins_mHH, binning_mHH);
    TH1F* hMap1D_dcos = new TH1F ("allHHNodeMap1D_dcos", "allHHNodeMap1D_dcos", 100, -1.,1.);



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
////////////
        hh = vH1 + vH2;
		  h_1 = vPho1 + vPho2;
///////////
        float mHH = vSum.M();

        vH1.Boost(-vSum.BoostVector());                     
        float ct1 = vH1.CosTheta();

        hMap->Fill(mHH, TMath::Abs(ct1));
        hMap1D->Fill(mHH);


///////////////
/*
	 float ebeam = 6500.;
    TLorentzVector p1, p2;
    p1.SetPxPyPzE(0, 0,  ebeam, ebeam);
    p2.SetPxPyPzE(0, 0, -ebeam, ebeam);
    TVector3 boost = - hh.BoostVector();
    p1.Boost(boost);
    p2.Boost(boost);
    h_1.Boost(boost);
    TVector3 CSaxis = p1.Vect().Unit() - p2.Vect().Unit();
    CSaxis.Unit();
    float ct_other =  cos(   CSaxis.Angle( h_1.Vect().Unit() )    );
    cout <<  " --> " << ct1 << " " << ct_other << "  "<<iEv<<endl;
    hMap1D_dcos->Fill(ct1-ct_other);
*/
///////////////////////////

    }

    fOut->cd();
    hMap->Write();
    hMap1D->Write();
//    hMap1D_dcos->Write();
	fOut->Close();
	fIn->Close();
}

