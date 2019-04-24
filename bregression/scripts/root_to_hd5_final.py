import plotting_utils as plotting
reload(plotting)
import pandas as pd
import root_pandas as rpd
import sys
import numpy as np

start = int(sys.argv[1])
end = int(sys.argv[2])

#in_dir = '/scratch/nchernya/HHbbgg/othersamples_morevar/'
#in_dir = 'root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/nchernya/HHbbgg/b_regression/ttbar_2018_16April2019/'
in_dir = 'root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat/store/user/nchernya/HHbbgg/b_regression/ttbar_2018_nanoAOD_JECv8/'
#out_dir = '/scratch/nchernya/HHbbgg/ttbar_2018_19April/'
#out_dir = '/scratch/nchernya/HHbbgg/ttbar_2017_JECv32/'
out_dir = '/scratch/nchernya/HHbbgg/ttbar_2018_JECv8/'
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

file_list  = [0 , 1 , 2 , 3 , 4 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 91 , 92 , 93 , 94 , 95 , 96 , 97 , 98 , 99 , 100 , 101 , 102 , 103 , 104 , 105 , 106 , 107 , 108 , 109 , 110 , 111 , 112 , 113 , 114 , 115 , 116 , 117 , 118 , 119 , 120 , 121 , 122 , 123 , 124 , 125 , 127 , 128 , 129 , 130 , 131 , 132 , 134 , 135 , 136 , 137 , 138 , 139 , 140 , 141 , 142 , 143 , 144 , 145 , 146 , 147 , 148 , 149 , 150 , 151 , 152 , 153 , 154 , 155 , 156 , 157 , 158]
#filelist=['ZHbbll_RegressionPerJet_heppy_energyRings_forTesting']
#filelist=['HHsm','HHres500','HHres700','ZHbbll']

#df_list = [(rpd.read_root(in_dir+'TTbar_nanoAOD_RegressionPerJet_nanoAOD_2017JECv32_%d.root'%i,'tree')).query(cuts) for i in range(start,end)]
#df_list = [(rpd.read_root(in_dir+'TTbar_nanoAOD_RegressionPerJet_nanoAOD_2017JECv32_%d.root'%file_list[i],'tree')).query(cuts) for i in range(start,end)]
df_list = [(rpd.read_root(in_dir+'TTbar_nanoAOD_RegressionPerJet_nanoAOD_2018_JECv8_%d.root'%file_list[i],'tree')).query(cuts) for i in range(start,end)]
#print 'list done'
###concatenate them together
big_df = pd.concat([df_list[i] for i in range(0,len(df_list))],ignore_index=True)
big_df['isEle'] = np.zeros( (big_df.shape[0],1) )
big_df['isMu'] = np.zeros( (big_df.shape[0],1) )
big_df['isOther'] = np.zeros( (big_df.shape[0],1) )
big_df['Jet_withPtd'] = big_df['Jet_ptd']
big_df.loc[abs(big_df.Jet_leptonPdgId) == 11,'isEle'] = 1
big_df.loc[abs(big_df.Jet_leptonPdgId) == 13,'isMu'] = 1#big_df.loc[big_df.Jet_leptonPdgId == -99,'isOther'] = 1  #2016
#big_df.loc[big_df.Jet_leptonPdgId == -99,'isOther'] = 1  #2016
big_df.loc[big_df.Jet_leptonPdgId == 0,'isOther'] = 1  #2017
#big_df.loc[big_df.Jet_ptd < 0 ,'Jet_withPtd' ] = big_df[ big_df['Jet_ptd'] > 0 ]['Jet_ptd'].median()  #2016
#big_df.loc[big_df.Jet_leptonPtRelInv < 0 ,'Jet_leptonPtRelInv' ] = 0  #2016

###Write the final hdf file
big_df.to_hdf(out_dir+'/TTbar_nanoAOD_RegressionPerJet_nanoAOD_2018_JECv8_con%d%d.hd5'%(start,end)  ,'w')
