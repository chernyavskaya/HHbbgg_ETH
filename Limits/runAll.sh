#!/bin/bash

# A POSIX variable
OPTIND=0         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
year=$1 #0 for 2016, 1 for 2017
ntup=ntuples_20190209/ntuples_${year}_20190209/
outTag=20191022_${year}

addHHTagger=0  #0 if you want to add it, 1 if it is already present

training_year=0
if [ $year -eq "2016" ]; then
	training_year=0
fi
if [ $year = 2017 ]; then
	training_year=1
fi
if [ $year = 2018 ]; then
	training_year=2
fi

#training="training_with_27_06_2018_newcode_v2"  #new code with fixed selection of jets
#training="training_with_01_10_2018_deepCSV" #deep CSV
#training="training_with_10_12_2018_commonTraining_2016" #deep CSV

#training="training_with_19_03_2019_trainingMjj_year"$year #deep CSV
training="training_with_07_10_2019_training"$training_year #first full run 2 training

echo $year,$training_year,$ntup,$outTag,$training

while getopts ":n:at:o:" opt; do
    case "${opt}" in
    n)  ntup=${OPTARG}
        ;;
    a)  addHHTagger=0
        ;;
    t)  training=${OPTARG}
        ;;
    o)  outTag=${OPTARG}
        ;;
    
    esac
done

shift $((OPTIND-1))

####create Trees
if ((addHHTagger)); then
   # #python /mnt/t3nfs01/data01/shome/nchernya//HHbbgg_ETH_devel/Limits/python/createReducedTrees.py -n $ntup -t $training  -o $outTag -a -y $year  -d 1  #with data
    python /mnt/t3nfs01/data01/shome/nchernya//HHbbgg_ETH_devel/Limits/python/cleanCreateReducedTrees.py -n $ntup -t $training  -o $outTag -a -y $training_year  
else
    python /mnt/t3nfs01/data01/shome/nchernya//HHbbgg_ETH_devel/Limits/python/cleanCreateReducedTrees.py -n $ntup -t $training  -o $outTag -y $training_year -k 0 
fi
    
####transform MVA output
#python /mnt/t3nfs01/data01/shome/nchernya//HHbbgg_ETH_devel/Limits/macros/transformMVAOutput.py -i '/mnt/t3nfs01/data01/shome/nchernya//HHbbgg_ETH_devel/outfiles/'$outTag'/Total_preselection_diffNaming_2016_2017.root'

## For both years
## python /mnt/t3nfs01/data01/shome/nchernya//HHbbgg_ETH_devel/Limits/macros/transformMVAOutputCommon.py -i '/shome/nchernya/HHbbgg_ETH_devel/outfiles/20181210_common_2016/Total_preselection_diffNaming.root,/shome/nchernya/HHbbgg_ETH_devel/outfiles/20181210_common_2017/Total_preselection_diffNaming.root'

## python /mnt/t3nfs01/data01/shome/nchernya//HHbbgg_ETH_devel/Limits/macros/applyTransformMVAOutput.py -i '/shome/nchernya/HHbbgg_ETH_devel/outfiles/20181210_common_2016_forcheck/Total_preselection_diffNaming.root' -g '/shome/nchernya/HHbbgg_ETH_devel/Limits/macros/plots/cumulatives/cumulativeTransformation_20181210_common_2016_2017.root'
