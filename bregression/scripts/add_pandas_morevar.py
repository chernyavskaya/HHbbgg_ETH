import os
import pandas as pd
import numpy as np
import sys

start = int(sys.argv[1])
end = int(sys.argv[2])

#targetdir='/scratch/nchernya/HHbbgg/ttbar_morevariables/'
#targetdir = '/scratch/nchernya/HHbbgg/ttbar_2017_v2/'
#targetdir = '/scratch/nchernya/HHbbgg/othersamples_morevar/'
#targetdir = '/scratch/nchernya/HHbbgg/'
targetdir = '/scratch/nchernya/HHbbgg/ttbar_2016_legacy_JECv11/'
#list the files
#file_list=[0,1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,55,56,57,58,59,61,62,64,65,66,67,68,69,73,75,78,79,80,81,82,83,84,85,86,87,88,90,91,92,93,94,95,96,97,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,154]
#file_list=[0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 91 , 92 , 93 , 94 , 95 , 96 , 97 , 98 , 99 , 100 , 101 , 102 , 103 , 105 , 106 , 107 , 108 , 109 , 111 , 112 , 113 , 114 , 115 , 116 , 117 , 118 , 119 , 120 , 121 , 122 , 123 , 124 , 125 , 126 , 127 , 128 , 129 , 130 , 131 , 132 , 133 , 134 , 135 , 136 , 137 , 138 , 139 , 140 , 141 , 142 , 143 , 144 , 145 , 146 , 147 , 148 , 149 , 150 , 151 , 152 , 153 , 154 , 155 , 156 , 157 , 158 , 159 , 160 , 161 , 162 , 163 , 164]
#filelist = [targetdir+'/ttbar_full_jobs_RegressionPerJet_heppy_energyRings_forTraining_%d_full.hd5'%num for num in file_list]
#file_list = [  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,        13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,        26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,        39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,        52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,        65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,        78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,        91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103,       104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,       117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,       130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,   143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155,       156, 157, 158, 159, 160, 161, 162, 163]
file_list = 'con020_allvar,con100120_allvar,con2040_allvar,con4060_allvar,con6080_allvar,con80100_allvar,spare_allvar,testing_allvar,testingsmall_allvar,validation_allvar'.split(',')
#name='ZHbbll'
#name='nano_variables3_RegressionPerJet_nanoAOD_2017_5'
name='TTbar_legacy2016_JECv11_RegressionPerJet_heppy_energyRings_forTraining_legacy_2ptds'
#filelist=[targetdir+'%s.hd5'%name]
#filelist = [targetdir+'/TTbar_nanoAOD_RegressionPerJet_nanoAOD_2017_%d.hd5'%num for num in file_list]
filelist = [targetdir+'/%s_%s.hd5'%(name,num) for num in file_list]
##read them into pandas
df_list = [pd.read_hdf(file,columns=None) for file in filelist[start:end]]
#print 'list done'
###concatenate them together
big_df = pd.concat([df_list[i] for i in range(0,len(df_list))],ignore_index=True)
big_df.loc[big_df.Jet_leptonPtRelInv < 0 ,'Jet_leptonPtRelInv' ] = 0  #2016
#big_df['Jet_vtx3deL_significance'] = big_df['Jet_vtx3dL']/big_df['Jet_vtx3deL']
big_df['Jet_vtx3deL_significance'] = np.where(big_df['Jet_vtx3deL']==0, 0, big_df['Jet_vtx3dL']/big_df['Jet_vtx3deL'])
#big_df['isEle'] = np.zeros( (big_df.shape[0],1) )
#big_df['isMu'] = np.zeros( (big_df.shape[0],1) )
#big_df['isOther'] = np.zeros( (big_df.shape[0],1) )
#big_df['Jet_withPtd'] = big_df['Jet_ptd']
#big_df.loc[abs(big_df.Jet_leptonPdgId) == 11,'isEle'] = 1
#big_df.loc[abs(big_df.Jet_leptonPdgId) == 13,'isMu'] = 1
##big_df.loc[big_df.Jet_leptonPdgId == -99,'isOther'] = 1  #2016
#big_df.loc[big_df.Jet_leptonPdgId == 0,'isOther'] = 1  #2017
#big_df.loc[big_df.Jet_ptd < 0 ,'Jet_withPtd' ] = big_df[ big_df['Jet_ptd'] > 0 ]['Jet_ptd'].median()  #2016
#big_df.loc[big_df.Jet_leptonPtRelInv < 0 ,'Jet_leptonPtRelInv' ] = 0  #2016
#big_df.to_hdf(targetdir+'/ttbar_full_jobs_RegressionPerJet_heppy_energyRings_forTraining_con%d%d_morevar.hd5'%(start,end)  ,'w')
#big_df.to_hdf(targetdir+'/ZHbbll_RegressionPerJet_heppy_energyRings_forTesting_morevar.hd5','w')
#big_df.to_hdf(targetdir+'/TTbar_nanoAOD_RegressionPerJet_nanoAOD_2017_v2_con%d%d_allvar.hd5'%(start,end)  ,'w')
#big_df.to_hdf(targetdir+'/%s_morevar.hd5'%(name)  ,'w')
big_df.to_hdf(filelist[start].replace('.hd5','_morevar.hd5')  ,'w')
