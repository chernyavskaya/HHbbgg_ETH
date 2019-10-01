#ls -v /pnfs/psi.ch/cms/trivcat/store/user/nchernya/VBFZll/workflow/v25b/SingleElectron  > el_done.txt
#ls -v /pnfs/psi.ch/cms/trivcat/store/user/nchernya/HHbbgg/b_regression/ttbar_2016_nanoAOD_JECv11 > done.txt
import string

input = open("done.txt","rt")
output = open("present.txt","wt")
lines = input.readlines()
max_num = 140
for i in range(0,max_num+1) :
	found = 0
	num = str(i)
	search_line = "TTbar_nanoAOD_RegressionPerJet_nanoAOD_2016_JECv11_"+ num +".root\n"
	if search_line in lines:
		output.write('%i,'%i)


