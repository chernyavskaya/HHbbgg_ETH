#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TLorentzVector.h"
#include <TH1F.h>
#include <string>
#include <sstream>
#include <map>
#include <cmath>
#include <TH2F.h>
#include <TH3F.h>
#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TSystem.h>
#include <TChain.h>
#include <TLorentzVector.h>
#include <TLegend.h>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <algorithm> 
#include <TRandom2.h>

using namespace std;

double deltaPhi(double phi1, double phi2)
{
	double PI = 3.14159265;
	double result = phi1 - phi2;
	while (result > PI) result -= 2*PI;
	while (result <= -PI) result += 2*PI;
	return result;
}
int main(int argc, char* argv[]){
int nstart = atoi(argv[1]);
int nend = atoi(argv[2]);
int fileout = atoi(argv[3]);
TString name = argv[4];
//void treeForRegression_2017(int nstart=1,int nend=1,int fileout=1,TString name = "new"){
//
//	TString inputfilename = "root://xrootd-cms.infn.it//store/user/legianni/NanoBReg01Fall17/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X-NanoBReg01Fall17/180324_124006/0000/";
//	TString inputfilename = "root://cms-xrd-global.cern.ch//store/user/legianni/NanoBReg02Fall17/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X-NanoBReg02Fall17/180328_230216/0000/";
//	TString inputfilename = "/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/submit_jobs/2017/";
//	TString inputfilename = "root://xrootd-cms.infn.it///store/user/arizzi/NanoRegression2/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODV2-NanoRegr2__017_realistic_v14-v1/180506_192512/0000/";
//	TString inputfilename = "root://xrootd-cms.infn.it////store/user/arizzi/NanoRegression2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODV2-NanoRegr2__017_realistic_v14-v1/180508_083758/0000/";
	TString inputfilename = "root://xrootd-cms.infn.it///store/user/legianni/NanoREGInputs18/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NANO_withRegInputs/190411_144336/0000/";

	TChain *tree=new TChain("Events");
   TString full_file_name="";
	for (int num=nstart;num<nend;num++){  //used for training as a test 
		TString str_tmp;
		str_tmp.Form("%d",num);
		cout<<str_tmp<<endl;
   //   full_file_name = inputfilename+"test94X_NANO_"+str_tmp+".root";
      full_file_name = inputfilename+"myNanoProdMc_NANO_"+str_tmp+".root";
    //  full_file_name = "nano_variables3.root";
		tree->Add(full_file_name);
	   std::cout<<"Added input file "<<full_file_name<<std::endl;
	}
//   tree->Print();
	tree->SetBranchAddress("*", 0);
	float rho;
	float met_pt,met_eta,met_phi;
	float GenJet_wNuPt[15];
	int          nhJCidx, nhJidx, nJet,nGenBQuarkFromTop;
	int         hJCidx[2], hJidx[2],Jet_mult[30],Jet_mcIdx[30],Jet_mcFlavour[30];  
	float      Jet_btagCMVA[30],Jet_btagDeepC[30] ,Jet_btagDeepB[30] ,  Jet_rawPt[30],Jet_corr[30],Jet_pt_reg[30],Jet_pt[30],Jet_rawPtAfterSmearing[30],Jet_corr_JEC[30],Jet_corr_JEC1[30],Jet_corr_JEC2[30],Jet_corr_JEC3[30],Jet_corr_JER[30],Jet_eta[30],Jet_phi[30],Jet_mass[30],Jet_chHEF[30],Jet_neHEF[30], Jet_muEF[30],Jet_chEmEF[30],Jet_neEmEF[30],Jet_chMult[30],Jet_nhMult[30],Jet_leadTrackPt[30],Jet_leptonPt[30],Jet_leptonPtRel[30],Jet_leptonPtRelnanoAOD[30],Jet_leptonDeltaR[30],Jet_vtxMass[30],Jet_vtxNtracks[30],Jet_vtxPt[30],Jet_vtx3DSig[30],Jet_vtx3DVal[30],GenBQuarkFromTop_pt[4],GenBQuarkFromTop_eta[4],GenBQuarkFromTop_phi[4],GenBQuarkFromTop_mass[4], Jet_ptd[30],Jet_axis2[30],Jet_leptonPdgId[30],Jet_leptonPtRelInv[30];
	Int_t Jet_puId[30],Jet_id[30];
	float genweight, puweight, genweight_, puweight_, bTagWeight_, bTagWeight;
	float Jet_rawFactor[30];
   float Jet_rawEnergy[30];
	float Jet_energyRing_dR0_neut[30],Jet_energyRing_dR1_neut[30],Jet_energyRing_dR2_neut[30],Jet_energyRing_dR3_neut[30],Jet_energyRing_dR4_neut[30],Jet_energyRing_dR5_neut[30];
	float Jet_energyRing_dR0_ch[30],Jet_energyRing_dR1_ch[30],Jet_energyRing_dR2_ch[30],Jet_energyRing_dR3_ch[30],Jet_energyRing_dR4_ch[30],Jet_energyRing_dR5_ch[30];
	float Jet_energyRing_dR0_em[30],Jet_energyRing_dR1_em[30],Jet_energyRing_dR2_em[30],Jet_energyRing_dR3_em[30],Jet_energyRing_dR4_em[30],Jet_energyRing_dR5_em[30];
	float Jet_energyRing_dR0_mu[30],Jet_energyRing_dR1_mu[30],Jet_energyRing_dR2_mu[30],Jet_energyRing_dR3_mu[30],Jet_energyRing_dR4_mu[30],Jet_energyRing_dR5_mu[30];
   int Jet_numDaughters_pt03[30];
	int Jet_numberOfDaughters[30];
	
	int run,luminosityBlock;
	long event;
	int run_,luminosityBlock_;
	long event_;

	int nPVs,nPVs_,nPVs_good,nPVs_good_;

	float Jet_bRegNN2[30],Jet_bRegNN2res[30];
	float Jet_bRegNN2_,Jet_bRegNN2res_;



//	TFile *hist_file = TFile::Open("/afs/cern.ch/work/n/nchernya/ETH/b_regression/heppy/unweighting_hist.root","read");
//	TFile *hist_file = TFile::Open("/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/root_files/unweighting_hist.root","read");
//	TH1F *hist_unweight = (TH1F*)hist_file->Get("hist_ratio");


	tree->SetBranchAddress("fixedGridRhoFastjetAll", &rho);
	tree->SetBranchAddress("genWeight",&genweight);
	tree->SetBranchAddress("PV_npvs", &nPVs);
	tree->SetBranchAddress("PV_npvsGood", &nPVs_good);
	tree->SetBranchAddress("MET_pt", &met_pt);
//	tree->SetBranchAddress("MET_eta", &met_eta);
	tree->SetBranchAddress("MET_phi", &met_phi);
	tree->SetBranchAddress("nJet", &nJet);
	tree->SetBranchAddress("Jet_puId", &Jet_puId);
	tree->SetBranchAddress("Jet_jetId", &Jet_id);
	tree->SetBranchAddress("Jet_btagCMVA", &Jet_btagCMVA);
	tree->SetBranchAddress("Jet_btagDeepC", &Jet_btagDeepC);
	tree->SetBranchAddress("Jet_btagDeepB", &Jet_btagDeepB);
	tree->SetBranchAddress("Jet_rawFactor", &Jet_rawFactor);
	tree->SetBranchAddress("Jet_partonFlavour", &Jet_mcFlavour);
	tree->SetBranchAddress("Jet_pt", &Jet_pt);
	tree->SetBranchAddress("Jet_eta", &Jet_eta);
	tree->SetBranchAddress("Jet_phi", &Jet_phi);
	tree->SetBranchAddress("Jet_mass", &Jet_mass);
	tree->SetBranchAddress("Jet_chHEF", &Jet_chHEF);
//	tree->SetBranchAddress("Jet_muEF", &Jet_muEF);
	tree->SetBranchAddress("Jet_neHEF", &Jet_neHEF);
	tree->SetBranchAddress("Jet_chEmEF", &Jet_chEmEF);
	tree->SetBranchAddress("Jet_neEmEF", &Jet_neEmEF);
//	tree->SetBranchAddress("Jet_chMult", &Jet_chMult);
//	tree->SetBranchAddress("Jet_nhMult", &Jet_nhMult);
	tree->SetBranchAddress("Jet_leadTrackPt", &Jet_leadTrackPt);
	tree->SetBranchAddress("Jet_leptonPt", &Jet_leptonPt);
	tree->SetBranchAddress("Jet_leptonPtRelv0", &Jet_leptonPtRel);
	tree->SetBranchAddress("Jet_leptonPtRel", &Jet_leptonPtRelnanoAOD);
	tree->SetBranchAddress("Jet_leptonDeltaR", &Jet_leptonDeltaR);
	tree->SetBranchAddress("Jet_leptonPdgId", &Jet_leptonPdgId);
	tree->SetBranchAddress("Jet_leptonPtRelInv", &Jet_leptonPtRelInv);  //the same is v0
	tree->SetBranchAddress("Jet_vtxMass", &Jet_vtxMass);
	tree->SetBranchAddress("Jet_vtxNtrk", &Jet_vtxNtracks);
	tree->SetBranchAddress("Jet_vtxPt", &Jet_vtxPt);
	tree->SetBranchAddress("Jet_vtx3deL", &Jet_vtx3DSig);
	tree->SetBranchAddress("Jet_vtx3dL", &Jet_vtx3DVal);
	tree->SetBranchAddress("Jet_ptD", &Jet_ptd);
	tree->SetBranchAddress("Jet_genJetIdx",&Jet_mcIdx);
	tree->SetBranchAddress("Jet_genPtwNu",&GenJet_wNuPt);
/*	tree->SetBranchAddress("GenBQuarkFromTop_pt",&GenBQuarkFromTop_pt);
	tree->SetBranchAddress("GenBQuarkFromTop_mass",&GenBQuarkFromTop_mass);
	tree->SetBranchAddress("GenBQuarkFromTop_phi",&GenBQuarkFromTop_phi);
	tree->SetBranchAddress("GenBQuarkFromTop_eta",&GenBQuarkFromTop_eta);
	tree->SetBranchAddress("nGenBQuarkFromTop",&nGenBQuarkFromTop);
*/	
   tree->SetBranchAddress("Jet_NeFractionEnergyRing0",&Jet_energyRing_dR0_neut);
   tree->SetBranchAddress("Jet_NeFractionEnergyRing1",&Jet_energyRing_dR1_neut);
   tree->SetBranchAddress("Jet_NeFractionEnergyRing2",&Jet_energyRing_dR2_neut);
   tree->SetBranchAddress("Jet_NeFractionEnergyRing3",&Jet_energyRing_dR3_neut);
   tree->SetBranchAddress("Jet_NeFractionEnergyRing4",&Jet_energyRing_dR4_neut);
   tree->SetBranchAddress("Jet_NeFractionEnergyRing5",&Jet_energyRing_dR5_neut);

   tree->SetBranchAddress("Jet_ChFractionEnergyRing0",&Jet_energyRing_dR0_ch);
   tree->SetBranchAddress("Jet_ChFractionEnergyRing1",&Jet_energyRing_dR1_ch);
   tree->SetBranchAddress("Jet_ChFractionEnergyRing2",&Jet_energyRing_dR2_ch);
   tree->SetBranchAddress("Jet_ChFractionEnergyRing3",&Jet_energyRing_dR3_ch);
   tree->SetBranchAddress("Jet_ChFractionEnergyRing4",&Jet_energyRing_dR4_ch);
   tree->SetBranchAddress("Jet_ChFractionEnergyRing5",&Jet_energyRing_dR5_ch);

   tree->SetBranchAddress("Jet_EmFractionEnergyRing0",&Jet_energyRing_dR0_em);
   tree->SetBranchAddress("Jet_EmFractionEnergyRing1",&Jet_energyRing_dR1_em);
   tree->SetBranchAddress("Jet_EmFractionEnergyRing2",&Jet_energyRing_dR2_em);
   tree->SetBranchAddress("Jet_EmFractionEnergyRing3",&Jet_energyRing_dR3_em);
   tree->SetBranchAddress("Jet_EmFractionEnergyRing4",&Jet_energyRing_dR4_em);
   tree->SetBranchAddress("Jet_EmFractionEnergyRing5",&Jet_energyRing_dR5_em);


   tree->SetBranchAddress("Jet_MuFractionEnergyRing0",&Jet_energyRing_dR0_mu);
   tree->SetBranchAddress("Jet_MuFractionEnergyRing1",&Jet_energyRing_dR1_mu);
   tree->SetBranchAddress("Jet_MuFractionEnergyRing2",&Jet_energyRing_dR2_mu);
   tree->SetBranchAddress("Jet_MuFractionEnergyRing3",&Jet_energyRing_dR3_mu);
   tree->SetBranchAddress("Jet_MuFractionEnergyRing4",&Jet_energyRing_dR4_mu);
   tree->SetBranchAddress("Jet_MuFractionEnergyRing5",&Jet_energyRing_dR5_mu);
   
	tree->SetBranchAddress("Jet_numDaughtersPt03",&Jet_numDaughters_pt03);
	tree->SetBranchAddress("Jet_nConstituents",&Jet_numberOfDaughters);
//   tree->SetBranchAddress("Jet_rawEnergy",&Jet_rawEnergy);

	tree->SetBranchAddress("Jet_JEC1", &Jet_corr_JEC1);
	tree->SetBranchAddress("Jet_JEC2", &Jet_corr_JEC2);
	tree->SetBranchAddress("Jet_JEC3", &Jet_corr_JEC3);
		
	tree->SetBranchAddress("event",&event);
	tree->SetBranchAddress("luminosityBlock",&luminosityBlock);
	tree->SetBranchAddress("run",&run);
	
	tree->SetBranchAddress("Jet_bRegNN2",&Jet_bRegNN2);
	tree->SetBranchAddress("Jet_bRegNN2res",&Jet_bRegNN2res);


	Long64_t nentries = tree->GetEntries();
	std::cout<< " nentries "<<nentries<<std::endl;
	Long64_t nbytes = 0, nb = 0;
	TString outname ;
   outname.Form("%d",fileout);
//	TFile *outfile=new TFile(name+"_RegressionPerJet_heppy_energyRings3_forTraining_Large"+outname+"_unweighted.root", "recreate");
	TFile *outfile=new TFile(name+"_RegressionPerJet_nanoAOD_2018_"+outname+".root", "recreate");
	int Jet_vtxNtrk;
	Int_t Jet_puId_, Jet_id_;
	float  Jet_mass_,Jet_corr_, Jet_e_, rho_, Jet_pt_,Jet_pt_reg_,Jet_eta_,Jet_phi_, Jet_leptonPtRel_,Jet_leptonPtRelnanoAOD_,Jet_leptonDeltaR_,Jet_leptonPt_, Jet_muEF_, Jet_leadTrackPt_, Jet_chHEF_, Jet_chEmEF_, Jet_neHEF_, Jet_neEmEF_, Jet_vtx3dL_, Jet_vtx3deL_, Jet_chMult_, Jet_nhMult_,Jet_mcPt_, Jet_mcEta_, Jet_mcPhi_, Jet_mcM_,  Jet_csv_, Jet_flavor_,  met_pt_, met_phi_, Jet_mcFlavour_,  Jet_met_dPhi_, Jet_mcE_, Jet_btagCMVA_, Jet_btagDeepC_,Jet_btagDeepB_, Jet_mt_, Jet_vtxMass_, Jet_vtx3dL, Jet_vtx3deL, Jet_vtxPt_, dR_, Jet_mcPtq_, Jet_corr_JER_,Jet_corr_JEC_, Jet_corr_JEC1_,Jet_corr_JEC2_,Jet_corr_JEC3_, Jet_rawPtAfterSmearing_,Jet_ptd_,Jet_axis2_,Jet_leptonPdgId_, Jet_leptonPtRelInv_;
	Jet_mass_=-999,Jet_corr_=-999, Jet_e_=-999, Jet_mt_=-999, rho_=-999, nPVs_=-999,Jet_pt_=-999,Jet_eta_=-999,Jet_phi_=-999, Jet_leptonPtRel_=-999,Jet_leptonDeltaR_=-999,Jet_leptonPt_=-999,Jet_leadTrackPt_=-999, Jet_chHEF_=-999, Jet_chEmEF_=-999, Jet_neHEF_=-999, Jet_muEF_=-999 ,Jet_neEmEF_=-999, Jet_vtx3dL_=-999, Jet_vtx3deL_=-999, Jet_chMult_=-999, Jet_nhMult_=-999, Jet_mcPt_=-999, Jet_mcEta_=-999, Jet_mcPhi_=-999, Jet_mcM_=-999,   Jet_csv_=-999, Jet_flavor_=-999,  met_pt_=-999, met_phi_=-999, Jet_btagCMVA_=-999, Jet_mcFlavour_=-999,  Jet_puId_=-999 , Jet_id_=-999, Jet_met_dPhi_=-999, Jet_mcE_=-999,  Jet_vtxMass_=-999., Jet_vtx3dL=-999., Jet_vtx3deL=-999., Jet_vtxPt_ =-999., Jet_mcPtq_=-999.;
	Jet_vtxNtrk= -999;

   float Jet_rawEnergy_;
	float Jet_energyRing_dR0_neut_,Jet_energyRing_dR1_neut_,Jet_energyRing_dR2_neut_,Jet_energyRing_dR3_neut_,Jet_energyRing_dR4_neut_,Jet_energyRing_dR5_neut_;
	float Jet_energyRing_dR0_ch_,Jet_energyRing_dR1_ch_,Jet_energyRing_dR2_ch_,Jet_energyRing_dR3_ch_,Jet_energyRing_dR4_ch_,Jet_energyRing_dR5_ch_;
	float Jet_energyRing_dR0_em_,Jet_energyRing_dR1_em_,Jet_energyRing_dR2_em_,Jet_energyRing_dR3_em_,Jet_energyRing_dR4_em_,Jet_energyRing_dR5_em_;
	float Jet_energyRing_dR0_mu_,Jet_energyRing_dR1_mu_,Jet_energyRing_dR2_mu_,Jet_energyRing_dR3_mu_,Jet_energyRing_dR4_mu_,Jet_energyRing_dR5_mu_;

	float Jet_energyRing_dR0_neut_Jet_rawEnergy_,Jet_energyRing_dR1_neut_Jet_rawEnergy_,Jet_energyRing_dR2_neut_Jet_rawEnergy_,Jet_energyRing_dR3_neut_Jet_rawEnergy_,Jet_energyRing_dR4_neut_Jet_rawEnergy_,Jet_energyRing_dR5_neut_Jet_rawEnergy_;
	float Jet_energyRing_dR0_ch_Jet_rawEnergy_,Jet_energyRing_dR1_ch_Jet_rawEnergy_,Jet_energyRing_dR2_ch_Jet_rawEnergy_,Jet_energyRing_dR3_ch_Jet_rawEnergy_,Jet_energyRing_dR4_ch_Jet_rawEnergy_,Jet_energyRing_dR5_ch_Jet_rawEnergy_;
	float Jet_energyRing_dR0_em_Jet_rawEnergy_,Jet_energyRing_dR1_em_Jet_rawEnergy_,Jet_energyRing_dR2_em_Jet_rawEnergy_,Jet_energyRing_dR3_em_Jet_rawEnergy_,Jet_energyRing_dR4_em_Jet_rawEnergy_,Jet_energyRing_dR5_em_Jet_rawEnergy_;
	float Jet_energyRing_dR0_mu_Jet_rawEnergy_,Jet_energyRing_dR1_mu_Jet_rawEnergy_,Jet_energyRing_dR2_mu_Jet_rawEnergy_,Jet_energyRing_dR3_mu_Jet_rawEnergy_,Jet_energyRing_dR4_mu_Jet_rawEnergy_,Jet_energyRing_dR5_mu_Jet_rawEnergy_;

	float Jet_rawFactor_= -999;

	int Jet_numDaughters_pt03_=-999;
	int Jet_numberOfDaughters_=-999;



	TTree *outtree = new TTree("tree", "tree");

	outtree->Branch("Jet_vtxNtrk",            &Jet_vtxNtrk ,"Jet_vtxNtrk/I");
	outtree->Branch("Jet_vtxMass",            &Jet_vtxMass_ ,"Jet_vtxMass_/F");
	outtree->Branch("Jet_vtx3dL",            &Jet_vtx3dL_ ,"Jet_vtx3dL_/F");
	outtree->Branch("Jet_vtx3deL",            &Jet_vtx3deL_ ,"Jet_vtx3deL_/F");
	outtree->Branch("Jet_vtxPt",            &Jet_vtxPt_ ,"Jet_vtxPt_/F");
//	outtree->Branch("dR",            &dR_ ,"dR_/F");
	outtree->Branch("genWeight",            &genweight_ ,"genWeight_/F");
	outtree->Branch("Jet_puId",          &Jet_puId_ ,"Jet_puId_/I");
	outtree->Branch("Jet_id",          &Jet_id_ ,"Jet_id_/I");
	outtree->Branch("Jet_btagCMVA",       &Jet_btagCMVA_ ,"Jet_btagCMVA_/F");
	outtree->Branch("Jet_btagDeepC",       &Jet_btagDeepC_ ,"Jet_btagDeepC_/F");
	outtree->Branch("Jet_btagDeepB",       &Jet_btagDeepB_ ,"Jet_btagDeepB_/F");
	outtree->Branch("Jet_mcPt",    &Jet_mcPt_ ,"Jet_mcPt_/F");
//	outtree->Branch("Jet_mcPtq",    &Jet_mcPtq_ ,"Jet_mcPtq_/F");
	outtree->Branch("Jet_mcFlavour",    &Jet_mcFlavour_ ,"Jet_mcFlavour_/F");
	outtree->Branch("Jet_pt",    &Jet_pt_ ,"Jet_pt_/F");
	outtree->Branch("Jet_mt",    &Jet_mt_ ,"Jet_mt_/F");
	outtree->Branch("Jet_eta",    &Jet_eta_ ,"Jet_eta_/F");
	outtree->Branch("Jet_e",    &Jet_e_ ,"Jet_e_/F");
	outtree->Branch("Jet_phi",    &Jet_phi_ ,"Jet_phi_/F");
	outtree->Branch("Jet_mass",    &Jet_mass_ ,"Jet_mass_/F");
	outtree->Branch("Jet_chHEF",    &Jet_chHEF_, "Jet_chHEF_/F");
//	outtree->Branch("Jet_muEF",    &Jet_muEF_, "Jet_muEF_/F");
	outtree->Branch("Jet_neHEF",    &Jet_neHEF_, "Jet_neHEF_/F");
	outtree->Branch("Jet_chEmEF",    &Jet_chEmEF_ ,"Jet_chEmEF_/F");
	outtree->Branch("Jet_neEmEF",   &Jet_neEmEF_ ,"Jet_neEmEF_/F");
//	outtree->Branch("Jet_chMult",   &Jet_chMult_ ,"Jet_chMult_/F"); 
//	outtree->Branch("Jet_nhMult",   &Jet_nhMult_ ,"Jet_nhMult_/F"); 
	outtree->Branch("Jet_leadTrackPt", &Jet_leadTrackPt_ ,"Jet_leadTrackPt_/F");
//	outtree->Branch("Jet_mcEta", &Jet_mcEta_, "Jet_mcEta_/F");
//	outtree->Branch("Jet_mcPhi", &Jet_mcPhi_ ,"Jet_mcPhi_/F");
//	outtree->Branch("Jet_mcM", &Jet_mcM_ ,"Jet_mcM_/F");
//	outtree->Branch("Jet_mcE", &Jet_mcE_ ,"Jet_mcE_/F");
	outtree->Branch("Jet_leptonPt", &Jet_leptonPt_ ,"Jet_leptonPt_/F");
	outtree->Branch("Jet_leptonPtRel", &Jet_leptonPtRel_ ,"Jet_leptonPtRel_/F"); 
	outtree->Branch("Jet_leptonPtRelnanoAOD", &Jet_leptonPtRelnanoAOD_ ,"Jet_leptonPtRelnanoAOD_/F"); 
	outtree->Branch("Jet_leptonDeltaR", &Jet_leptonDeltaR_ ,"Jet_leptonDeltaR_/F"); 
	outtree->Branch("rho", &rho_ ,"rho_/F");
	outtree->Branch("nPVs", &nPVs_ ,"nPVs_/I");
	outtree->Branch("nPVs_good", &nPVs_good_ ,"nPVs_good_/I");
	outtree->Branch("met_pt",  &met_pt_, "met_pt_/F");
	outtree->Branch("met_phi", &met_phi_, "met_phi_/F");
	outtree->Branch("Jet_met_dPhi", &Jet_met_dPhi_, "Jet_met_dPhi_/F");
	outtree->Branch("Jet_rawEnergy", &Jet_rawEnergy_, "Jet_rawEnergy_/F");
	outtree->Branch("Jet_rawFactor", &Jet_rawFactor_, "Jet_rawFactor_/F");


   outtree->Branch("Jet_energyRing_dR0_neut",&Jet_energyRing_dR0_neut_,"Jet_energyRing_dR0_neut_/F");
   outtree->Branch("Jet_energyRing_dR1_neut",&Jet_energyRing_dR1_neut_,"Jet_energyRing_dR1_neut_/F");
   outtree->Branch("Jet_energyRing_dR2_neut",&Jet_energyRing_dR2_neut_,"Jet_energyRing_dR2_neut_/F");
   outtree->Branch("Jet_energyRing_dR3_neut",&Jet_energyRing_dR3_neut_,"Jet_energyRing_dR3_neut_/F");
   outtree->Branch("Jet_energyRing_dR4_neut",&Jet_energyRing_dR4_neut_,"Jet_energyRing_dR4_neut_/F");
   outtree->Branch("Jet_energyRing_dR5_neut",&Jet_energyRing_dR5_neut_,"Jet_energyRing_dR5_neut_/F");

   outtree->Branch("Jet_energyRing_dR0_ch",&Jet_energyRing_dR0_ch_,"Jet_energyRing_dR0_ch_/F");
   outtree->Branch("Jet_energyRing_dR1_ch",&Jet_energyRing_dR1_ch_,"Jet_energyRing_dR1_ch_/F");
   outtree->Branch("Jet_energyRing_dR2_ch",&Jet_energyRing_dR2_ch_,"Jet_energyRing_dR2_ch_/F");
   outtree->Branch("Jet_energyRing_dR3_ch",&Jet_energyRing_dR3_ch_,"Jet_energyRing_dR3_ch_/F");
   outtree->Branch("Jet_energyRing_dR4_ch",&Jet_energyRing_dR4_ch_,"Jet_energyRing_dR4_ch_/F");
   outtree->Branch("Jet_energyRing_dR5_ch",&Jet_energyRing_dR5_ch_,"Jet_energyRing_dR5_ch_/F");
   
	outtree->Branch("Jet_energyRing_dR0_em",&Jet_energyRing_dR0_em_,"Jet_energyRing_dR0_em_/F");
   outtree->Branch("Jet_energyRing_dR1_em",&Jet_energyRing_dR1_em_,"Jet_energyRing_dR1_em_/F");
   outtree->Branch("Jet_energyRing_dR2_em",&Jet_energyRing_dR2_em_,"Jet_energyRing_dR2_em_/F");
   outtree->Branch("Jet_energyRing_dR3_em",&Jet_energyRing_dR3_em_,"Jet_energyRing_dR3_em_/F");
   outtree->Branch("Jet_energyRing_dR4_em",&Jet_energyRing_dR4_em_,"Jet_energyRing_dR4_em_/F");
   outtree->Branch("Jet_energyRing_dR5_em",&Jet_energyRing_dR5_em_,"Jet_energyRing_dR5_em_/F");

   outtree->Branch("Jet_energyRing_dR0_mu",&Jet_energyRing_dR0_mu_,"Jet_energyRing_dR0_mu_/F");
   outtree->Branch("Jet_energyRing_dR1_mu",&Jet_energyRing_dR1_mu_,"Jet_energyRing_dR1_mu_/F");
   outtree->Branch("Jet_energyRing_dR2_mu",&Jet_energyRing_dR2_mu_,"Jet_energyRing_dR2_mu_/F");
   outtree->Branch("Jet_energyRing_dR3_mu",&Jet_energyRing_dR3_mu_,"Jet_energyRing_dR3_mu_/F");
   outtree->Branch("Jet_energyRing_dR4_mu",&Jet_energyRing_dR4_mu_,"Jet_energyRing_dR4_mu_/F");
   outtree->Branch("Jet_energyRing_dR5_mu",&Jet_energyRing_dR5_mu_,"Jet_energyRing_dR5_mu_/F");

	outtree->Branch("Jet_numDaughters_pt03",&Jet_numDaughters_pt03_,"Jet_numDaughters_pt03_/I");
	outtree->Branch("Jet_numberOfDaughters",&Jet_numberOfDaughters_,"Jet_numberOfDaughters_/I");


   outtree->Branch("Jet_energyRing_dR0_neut_Jet_rawEnergy",&Jet_energyRing_dR0_neut_Jet_rawEnergy_,"Jet_energyRing_dR0_neut_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR1_neut_Jet_rawEnergy",&Jet_energyRing_dR1_neut_Jet_rawEnergy_,"Jet_energyRing_dR1_neut_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR2_neut_Jet_rawEnergy",&Jet_energyRing_dR2_neut_Jet_rawEnergy_,"Jet_energyRing_dR2_neut_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR3_neut_Jet_rawEnergy",&Jet_energyRing_dR3_neut_Jet_rawEnergy_,"Jet_energyRing_dR3_neut_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR4_neut_Jet_rawEnergy",&Jet_energyRing_dR4_neut_Jet_rawEnergy_,"Jet_energyRing_dR4_neut_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR5_neut_Jet_rawEnergy",&Jet_energyRing_dR5_neut_Jet_rawEnergy_,"Jet_energyRing_dR5_neut_Jet_rawEnergy_/F");

   outtree->Branch("Jet_energyRing_dR0_ch_Jet_rawEnergy",&Jet_energyRing_dR0_ch_Jet_rawEnergy_,"Jet_energyRing_dR0_ch_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR1_ch_Jet_rawEnergy",&Jet_energyRing_dR1_ch_Jet_rawEnergy_,"Jet_energyRing_dR1_ch_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR2_ch_Jet_rawEnergy",&Jet_energyRing_dR2_ch_Jet_rawEnergy_,"Jet_energyRing_dR2_ch_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR3_ch_Jet_rawEnergy",&Jet_energyRing_dR3_ch_Jet_rawEnergy_,"Jet_energyRing_dR3_ch_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR4_ch_Jet_rawEnergy",&Jet_energyRing_dR4_ch_Jet_rawEnergy_,"Jet_energyRing_dR4_ch_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR5_ch_Jet_rawEnergy",&Jet_energyRing_dR5_ch_Jet_rawEnergy_,"Jet_energyRing_dR5_ch_Jet_rawEnergy_/F");
   
	outtree->Branch("Jet_energyRing_dR0_em_Jet_rawEnergy",&Jet_energyRing_dR0_em_Jet_rawEnergy_,"Jet_energyRing_dR0_em_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR1_em_Jet_rawEnergy",&Jet_energyRing_dR1_em_Jet_rawEnergy_,"Jet_energyRing_dR1_em_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR2_em_Jet_rawEnergy",&Jet_energyRing_dR2_em_Jet_rawEnergy_,"Jet_energyRing_dR2_em_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR3_em_Jet_rawEnergy",&Jet_energyRing_dR3_em_Jet_rawEnergy_,"Jet_energyRing_dR3_em_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR4_em_Jet_rawEnergy",&Jet_energyRing_dR4_em_Jet_rawEnergy_,"Jet_energyRing_dR4_em_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR5_em_Jet_rawEnergy",&Jet_energyRing_dR5_em_Jet_rawEnergy_,"Jet_energyRing_dR5_em_Jet_rawEnergy_/F");

   outtree->Branch("Jet_energyRing_dR0_mu_Jet_rawEnergy",&Jet_energyRing_dR0_mu_Jet_rawEnergy_,"Jet_energyRing_dR0_mu_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR1_mu_Jet_rawEnergy",&Jet_energyRing_dR1_mu_Jet_rawEnergy_,"Jet_energyRing_dR1_mu_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR2_mu_Jet_rawEnergy",&Jet_energyRing_dR2_mu_Jet_rawEnergy_,"Jet_energyRing_dR2_mu_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR3_mu_Jet_rawEnergy",&Jet_energyRing_dR3_mu_Jet_rawEnergy_,"Jet_energyRing_dR3_mu_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR4_mu_Jet_rawEnergy",&Jet_energyRing_dR4_mu_Jet_rawEnergy_,"Jet_energyRing_dR4_mu_Jet_rawEnergy_/F");
   outtree->Branch("Jet_energyRing_dR5_mu_Jet_rawEnergy",&Jet_energyRing_dR5_mu_Jet_rawEnergy_,"Jet_energyRing_dR5_mu_Jet_rawEnergy_/F");

	outtree->Branch("Jet_numDaughters_pt03",&Jet_numDaughters_pt03_,"Jet_numDaughters_pt03_/I");

	outtree->Branch("Jet_corr_JEC", &Jet_corr_JEC_,"Jet_corr_JEC_/F");
	outtree->Branch("Jet_JEC1", &Jet_corr_JEC1_,"Jet_corr_JEC1_/F");
	outtree->Branch("Jet_JEC2", &Jet_corr_JEC2_,"Jet_corr_JEC2_/F");
	outtree->Branch("Jet_JEC3", &Jet_corr_JEC3_,"Jet_corr_JEC3_/F");
//	outtree->Branch("Jet_rawPtAfterSmearing", &Jet_rawPtAfterSmearing_,"Jet_rawPtAfterSmearing_/F");
	outtree->Branch("Jet_ptd", &Jet_ptd_,"Jet_ptd_/F");
	outtree->Branch("Jet_leptonPdgId",&Jet_leptonPdgId_,"Jet_leptonPdgId_/F");
	outtree->Branch("Jet_leptonPtRelInv",&Jet_leptonPtRelInv_,"Jet_leptonPtRelInv_/F");
		
	outtree->Branch("event",&event_,"event_/I");
	outtree->Branch("run",&run_,"run_/I");
	outtree->Branch("luminosityBlock",&luminosityBlock_,"luminosityBlock_/L");
	
	outtree->Branch("Jet_bRegNN2",&Jet_bRegNN2_,"Jet_bRegNN2_/F");
	outtree->Branch("Jet_bRegNN2res",&Jet_bRegNN2res_,"Jet_bRegNN2res_/F");
	
//	TRandom2 random_gen(0);

	for (Long64_t jentry=0; jentry<nentries;jentry++) {
//	for (Long64_t jentry=0; jentry<100;jentry++) {
		tree->GetEvent(jentry);
		event_ = event;
		run_ = run;
		luminosityBlock_ = luminosityBlock;
	   rho_ = rho;
	   nPVs_ = nPVs;
		nPVs_good_ = nPVs_good;
		genweight_ = genweight;
		for(int i =0 ; i<nJet; i++){

//////////////Unweighting/////////////////////
/*
			float rdn;
			rdn = random_gen.Uniform(0,1);
			float current_pt_value;
			float current_pt_bin = hist_unweight->FindBin(Jet_pt[i]);
			if (current_pt_bin < hist_unweight->GetNbinsX() )   current_pt_value = hist_unweight->GetBinContent(hist_unweight->FindBin(Jet_pt[i]));
			else current_pt_value=1.;
		if (!(rdn<current_pt_value)) continue;
*/
//////////////Unweighting ends/////////////////////

	//		if(Jet_mcIdx[i]<0 ) continue;
	//		if(Jet_mcIdx[i]>15 ) continue;
			TLorentzVector hJ0, hJ1;
			Jet_pt_=Jet_pt[i];
		//	Jet_pt_reg_=Jet_pt_reg[i];
			Jet_eta_=Jet_eta[i];
			Jet_phi_=Jet_phi[i];
			Jet_puId_ = Jet_puId[i];
			Jet_id_ = Jet_id[i];
			Jet_mass_=Jet_mass[i];
			Jet_met_dPhi_=deltaPhi(met_phi,Jet_phi[i]);
			met_pt_= met_pt;
			met_phi_= met_phi;
			Jet_leptonPtRel_ = std::max(float(0.),Jet_leptonPtRel[i]);
			Jet_leptonPtRelnanoAOD_ = std::max(float(0.),Jet_leptonPtRelnanoAOD[i]);
			Jet_leptonDeltaR_ = std::max(float(0.),Jet_leptonDeltaR[i]);
			Jet_leptonPt_ = std::max(float(0.),Jet_leptonPt[i]);
			Jet_leadTrackPt_ = Jet_leadTrackPt[i];
//			Jet_muEF_ =  std::min(float(1.),Jet_muEF[i]);
			Jet_chHEF_ =  std::min(float(1.),Jet_chHEF[i]);
			Jet_chEmEF_=  std::min(float(1.), Jet_chEmEF[i]);
			Jet_neHEF_=  std::min(float(1.),Jet_neHEF[i]);
			Jet_neEmEF_ = std::min(float(1.),Jet_neEmEF[i]);

			Jet_energyRing_dR0_neut_ = Jet_energyRing_dR0_neut[i];
			Jet_energyRing_dR1_neut_ = Jet_energyRing_dR1_neut[i];
			Jet_energyRing_dR2_neut_ = Jet_energyRing_dR2_neut[i];
			Jet_energyRing_dR3_neut_ = Jet_energyRing_dR3_neut[i];
			Jet_energyRing_dR4_neut_ = Jet_energyRing_dR4_neut[i];
			Jet_energyRing_dR5_neut_ = Jet_energyRing_dR5_neut[i];

			Jet_energyRing_dR0_ch_ = Jet_energyRing_dR0_ch[i];
			Jet_energyRing_dR1_ch_ = Jet_energyRing_dR1_ch[i];
			Jet_energyRing_dR2_ch_ = Jet_energyRing_dR2_ch[i];
			Jet_energyRing_dR3_ch_ = Jet_energyRing_dR3_ch[i];
			Jet_energyRing_dR4_ch_ = Jet_energyRing_dR4_ch[i];
			Jet_energyRing_dR5_ch_ = Jet_energyRing_dR5_ch[i];
			
			Jet_energyRing_dR0_em_ = Jet_energyRing_dR0_em[i];
			Jet_energyRing_dR1_em_ = Jet_energyRing_dR1_em[i];
			Jet_energyRing_dR2_em_ = Jet_energyRing_dR2_em[i];
			Jet_energyRing_dR3_em_ = Jet_energyRing_dR3_em[i];
			Jet_energyRing_dR4_em_ = Jet_energyRing_dR4_em[i];
			Jet_energyRing_dR5_em_ = Jet_energyRing_dR5_em[i];
	
			Jet_energyRing_dR0_mu_ = Jet_energyRing_dR0_mu[i];
			Jet_energyRing_dR1_mu_ = Jet_energyRing_dR1_mu[i];
			Jet_energyRing_dR2_mu_ = Jet_energyRing_dR2_mu[i];
			Jet_energyRing_dR3_mu_ = Jet_energyRing_dR3_mu[i];
			Jet_energyRing_dR4_mu_ = Jet_energyRing_dR4_mu[i];
			Jet_energyRing_dR5_mu_ = Jet_energyRing_dR5_mu[i];
			
			Jet_bRegNN2_ = Jet_bRegNN2[i];
			Jet_bRegNN2res_ = Jet_bRegNN2res[i];

			Jet_corr_JEC1_ = Jet_corr_JEC1[i];	
			Jet_corr_JEC2_ = Jet_corr_JEC2[i];	
			Jet_corr_JEC3_ = Jet_corr_JEC3[i];	
	//		Jet_corr_JER_ = Jet_corr_JER[i];	
		//	Jet_rawPtAfterSmearing_ = Jet_rawPtAfterSmearing[i];
			Jet_ptd_ = Jet_ptd[i];	
//			Jet_axis2_ = Jet_axis2[i];	
			Jet_leptonPdgId_ = Jet_leptonPdgId[i];
			Jet_leptonPtRelInv_ = Jet_leptonPtRelInv[i];
	
			Jet_numDaughters_pt03_ = Jet_numDaughters_pt03[i];
			Jet_numberOfDaughters_ = Jet_numberOfDaughters[i];


			hJ0.SetPtEtaPhiM(Jet_pt[i],Jet_eta[i],Jet_phi[i],Jet_mass[i]);
			Jet_e_=hJ0.E();
       	Jet_rawFactor_ = Jet_rawFactor[i];
       	Jet_rawEnergy_ = Jet_e_*(1.-Jet_rawFactor_);
			Jet_corr_JEC_ = 1./(1. - Jet_rawFactor_);	


			Jet_energyRing_dR0_neut_Jet_rawEnergy_ = Jet_energyRing_dR0_neut[i]/Jet_rawEnergy_;
			Jet_energyRing_dR1_neut_Jet_rawEnergy_ = Jet_energyRing_dR1_neut[i]/Jet_rawEnergy_;
			Jet_energyRing_dR2_neut_Jet_rawEnergy_ = Jet_energyRing_dR2_neut[i]/Jet_rawEnergy_;
			Jet_energyRing_dR3_neut_Jet_rawEnergy_ = Jet_energyRing_dR3_neut[i]/Jet_rawEnergy_;
			Jet_energyRing_dR4_neut_Jet_rawEnergy_ = Jet_energyRing_dR4_neut[i]/Jet_rawEnergy_;
			Jet_energyRing_dR5_neut_Jet_rawEnergy_ = Jet_energyRing_dR5_neut[i]/Jet_rawEnergy_;

			Jet_energyRing_dR0_ch_Jet_rawEnergy_ = Jet_energyRing_dR0_ch[i]/Jet_rawEnergy_;
			Jet_energyRing_dR1_ch_Jet_rawEnergy_ = Jet_energyRing_dR1_ch[i]/Jet_rawEnergy_;
			Jet_energyRing_dR2_ch_Jet_rawEnergy_ = Jet_energyRing_dR2_ch[i]/Jet_rawEnergy_;
			Jet_energyRing_dR3_ch_Jet_rawEnergy_ = Jet_energyRing_dR3_ch[i]/Jet_rawEnergy_;
			Jet_energyRing_dR4_ch_Jet_rawEnergy_ = Jet_energyRing_dR4_ch[i]/Jet_rawEnergy_;
			Jet_energyRing_dR5_ch_Jet_rawEnergy_ = Jet_energyRing_dR5_ch[i]/Jet_rawEnergy_;
			
			Jet_energyRing_dR0_em_Jet_rawEnergy_ = Jet_energyRing_dR0_em[i]/Jet_rawEnergy_;
			Jet_energyRing_dR1_em_Jet_rawEnergy_ = Jet_energyRing_dR1_em[i]/Jet_rawEnergy_;
			Jet_energyRing_dR2_em_Jet_rawEnergy_ = Jet_energyRing_dR2_em[i]/Jet_rawEnergy_;
			Jet_energyRing_dR3_em_Jet_rawEnergy_ = Jet_energyRing_dR3_em[i]/Jet_rawEnergy_;
			Jet_energyRing_dR4_em_Jet_rawEnergy_ = Jet_energyRing_dR4_em[i]/Jet_rawEnergy_;
			Jet_energyRing_dR5_em_Jet_rawEnergy_ = Jet_energyRing_dR5_em[i]/Jet_rawEnergy_;
	
			Jet_energyRing_dR0_mu_Jet_rawEnergy_ = Jet_energyRing_dR0_mu[i]/Jet_rawEnergy_;
			Jet_energyRing_dR1_mu_Jet_rawEnergy_ = Jet_energyRing_dR1_mu[i]/Jet_rawEnergy_;
			Jet_energyRing_dR2_mu_Jet_rawEnergy_ = Jet_energyRing_dR2_mu[i]/Jet_rawEnergy_;
			Jet_energyRing_dR3_mu_Jet_rawEnergy_ = Jet_energyRing_dR3_mu[i]/Jet_rawEnergy_;
			Jet_energyRing_dR4_mu_Jet_rawEnergy_ = Jet_energyRing_dR4_mu[i]/Jet_rawEnergy_;
			Jet_energyRing_dR5_mu_Jet_rawEnergy_ = Jet_energyRing_dR5_mu[i]/Jet_rawEnergy_;






			Jet_mt_=hJ0.Mt();
	//		Jet_chMult_=Jet_chMult[i];
	//		Jet_nhMult_=Jet_nhMult[i];
			Jet_vtx3dL_=std::max(float(0.),Jet_vtx3DVal[i]);
			Jet_vtxMass_=std::max(float(0.),Jet_vtxMass[i]);
			Jet_vtx3deL_=std::max(float(0.),Jet_vtx3DSig[i]);
			Jet_vtxNtrk=std::max(float(0.),Jet_vtxNtracks[i]);
			Jet_vtxPt_=std::max(float(0.),Jet_vtxPt[i]);
         Jet_mcPt_ = -999.;
	//		Jet_mcPt_= GenJet_wNuPt[Jet_mcIdx[i]];
			Jet_mcPt_= GenJet_wNuPt[i]; //in nanoAod already matched
	/*		dR_ =999;
			Jet_mcPtq_=-999.;
			Jet_mcE_=-999.;
			Jet_mcEta_=-999.;
			Jet_mcPhi_=-999.;
			Jet_mcM_= -999.;
			double minDr = 0.4;
			for(int m=0; m<nGenBQuarkFromTop; m++){
				hJ1.SetPtEtaPhiM(GenBQuarkFromTop_pt[m],GenBQuarkFromTop_eta[m],GenBQuarkFromTop_phi[m],GenBQuarkFromTop_mass[m]);       
				if(hJ1.DeltaR(hJ0)<minDr){

					Jet_mcE_=hJ1.E();
					Jet_mcPtq_ = GenBQuarkFromTop_pt[m];
					Jet_mcEta_=  GenBQuarkFromTop_eta[m];
					Jet_mcPhi_=  GenBQuarkFromTop_phi[m];
					Jet_mcM_= GenBQuarkFromTop_mass[m];
					minDr = hJ1.DeltaR(hJ0);         
					dR_ = minDr;

				}
			}
*/



			Jet_mcFlavour_=Jet_mcFlavour[i];
			Jet_btagDeepC_=Jet_btagDeepC[i];
			Jet_btagDeepB_=Jet_btagDeepB[i];
			Jet_btagCMVA_=Jet_btagCMVA[i];
			outtree->Fill();
		}
	}
	outtree->Write();
	outfile->Close();
//	hist_file->Close();
}

