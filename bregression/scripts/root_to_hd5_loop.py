import plotting_utils as plotting
reload(plotting)
import pandas as pd
import root_pandas as rpd
import sys

#start = int(sys.argv[1])
#end = int(sys.argv[2])
#file_name='ttbar_RegressionPerJet_heppy_energyRings3_forTesting.root'

#inout_dir = '/users/nchernya/HHbbgg_ETH/root_files/'
#out_dir = '/scratch/nchernya/HHbbgg/ttbar_full_hd5/'
#out_dir = '/scratch/nchernya/HHbbgg/ttbar_morevariables/'
##out_dir = '/scratch/nchernya/HHbbgg/ttbar_2017/'
#in_dir = 'root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/nchernya/HHbbgg/b_regression/ttbar_full/'
#in_dir='/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/submit_jobs/'
##in_dir = 'root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/nchernya/HHbbgg/b_regression/ttbar_2017_nanoAOD/'

#out_dir = '/scratch/nchernya/HHbbgg/othersamples_morevar/'
#in_dir = '/scratch/nchernya/HHbbgg/othersamples_morevar/'
in_dir = 'root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/nchernya/HHbbgg/b_regression/ttbar_2018_16April2019/'
#in_dir = '/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/submit_jobs/'
#out_dir = '/scratch/nchernya/HHbbgg/ttbar_2017_v2/'
#in_dir = '/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/submit_jobs/2017/'
#out_dir = '/scratch/nchernya/HHbbgg/ttbar_2017_v3_newJEC/'
out_dir = '/scratch/nchernya/HHbbgg/ttbar_2018_19April/'
rings=[
                    'Jet_energyRing_dR0_em',
                    'Jet_energyRing_dR1_em',
                    'Jet_energyRing_dR2_em',
                    'Jet_energyRing_dR3_em',
                    'Jet_energyRing_dR4_em',
                    'Jet_energyRing_dR0_neut',
                    'Jet_energyRing_dR1_neut',
                    'Jet_energyRing_dR2_neut',
                    'Jet_energyRing_dR3_neut',
                    'Jet_energyRing_dR4_neut',
                    'Jet_energyRing_dR0_ch',
                    'Jet_energyRing_dR1_ch',
                    'Jet_energyRing_dR2_ch',
                    'Jet_energyRing_dR3_ch',
                    'Jet_energyRing_dR4_ch',
                    'Jet_energyRing_dR0_mu',
                    'Jet_energyRing_dR1_mu',
                    'Jet_energyRing_dR2_mu',
                    'Jet_energyRing_dR3_mu',
                    'Jet_energyRing_dR4_mu']

branch_names = 'Jet_pt,Jet_eta,Jet_mcFlavour,Jet_mcPt,rho,Jet_mt,Jet_leadTrackPt,Jet_leptonPt,Jet_leptonPtRel,Jet_leptonDeltaR,Jet_neHEF,Jet_neEmEF,Jet_vtxPt,Jet_vtxMass,Jet_vtx3dL,Jet_vtxNtrk,Jet_vtx3deL,Jet_energyRing_dR0_em,Jet_energyRing_dR1_em,Jet_energyRing_dR2_em,Jet_energyRing_dR3_em,Jet_energyRing_dR4_em,Jet_energyRing_dR0_neut,Jet_energyRing_dR1_neut,Jet_energyRing_dR2_neut,Jet_energyRing_dR3_neut,Jet_energyRing_dR4_neut,Jet_energyRing_dR0_ch,Jet_energyRing_dR1_ch,Jet_energyRing_dR2_ch,Jet_energyRing_dR3_ch,Jet_energyRing_dR4_ch,Jet_energyRing_dR0_mu,Jet_energyRing_dR1_mu,Jet_energyRing_dR2_mu,Jet_energyRing_dR3_mu,Jet_energyRing_dR4_mu,Jet_numDaughters_pt03,Jet_pt_reg,Jet_e,Jet_rawEnergy,Jet_energyRing_dR0_em,Jet_energyRing_dR1_em,Jet_energyRing_dR2_em,Jet_energyRing_dR3_em,Jet_energyRing_dR4_em,Jet_energyRing_dR0_neut,Jet_energyRing_dR1_neut,Jet_energyRing_dR2_neut,Jet_energyRing_dR3_neut,Jet_energyRing_dR4_neut,Jet_energyRing_dR0_ch,Jet_energyRing_dR1_ch,Jet_energyRing_dR2_ch,Jet_energyRing_dR3_ch,Jet_energyRing_dR4_ch,Jet_energyRing_dR0_mu,Jet_energyRing_dR1_mu,Jet_energyRing_dR2_mu,Jet_energyRing_dR3_mu,Jet_energyRing_dR4_mu,Jet_corr_JEC,Jet_corr_JER,Jet_rawPtAfterSmearing,Jet_ptd,Jet_axis2,Jet_leptonPdgId,Jet_leptonPtRelInv,nPVs,Jet_mass,Jet_chHEF,Jet_chEmEF,Jet_chMult'
branch_names = branch_names.split(',')
for ring in rings:
    branch_names.append('%s_Jet_rawEnergy'%ring)
cuts='(Jet_pt > 15) & (Jet_eta<2.5 & Jet_eta>-2.5) & (Jet_mcFlavour==5 | Jet_mcFlavour==-5) & (Jet_mcPt>1.) & (Jet_mcPt<6000)' #all for presentaion on 23 Jan was done with pT cut at 20 GeV

file_list  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122,  124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157]
#filelist=['ZHbbll_RegressionPerJet_heppy_energyRings_forTesting']
#filelist=['HHsm','HHres500','HHres700','ZHbbll']
for i in range(0,len(file_list)):
#for i in range(start,end):
  num = file_list[i]
  filename='TTbar_nanoAOD_RegressionPerJet_nanoAOD_2018_%d'%num
#  filename=filelist[i]
#  filename='TTbar_nanoAOD_RegressionPerJet_nanoAOD_2017_%d'%num
#  filename='TTbar_2ptds_RegressionPerJet_heppy_energyRings_forTraining_10_full_2ptd'
#  filename='nano_variables3_RegressionPerJet_nanoAOD_2017_5'
#  filename='TT2lep_RegressionPerJet_nanoAOD_2017_2'
#  tmp_data_frame = (rpd.read_root(in_dir+filename+'.root','tree', columns = branch_names))
  tmp_data_frame = (rpd.read_root(in_dir+filename+'.root','tree'))
#  for ring in rings:
 #     tmp_data_frame['%s_Jet_rawEnergy'%ring]=tmp_data_frame['%s'%ring]/tmp_data_frame['Jet_rawEnergy']
  tmp_data_frame_cut = tmp_data_frame.query(cuts)
  #tmp_data_frame_cut['Jet_corr'] = tmp_data_frame_cut['Jet_corr_JEC']
  tmp_data_frame_cut.to_hdf(out_dir+filename+'.hd5'  ,'w')
