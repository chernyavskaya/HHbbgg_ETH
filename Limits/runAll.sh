#!/bin/bash

# A POSIX variable
OPTIND=0         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
year=$1 #0 for 2016, 1 for 2017
#ntup=ntuples_20191501/ntuples_${year}_20191501/
ntup=ntuples_20192401/ntuples_${year}_20192401/
#outTag=20191218_wo_Mjj_${year}
#outTag=20191812_btag_upd_${year}
#outTag=20191812_btag_wo_Mjj_upd_${year}
#outTag=20191802_wo_Mjj_leptonveto_flashgg_${year}
#outTag=20191802_wo_Mjj_leptonveto_flashgg_SMsignal_${year}
outTag=test_output_soumya



addHHTagger=0  #0 if you want to add it, 1 if it is already present
#addHHTagger=1  #0 if you want to add it, 1 if it is already present
flashggNames=1 #if flashggnames

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

#training="training_with_18_12_2019_training"$training_year #christmas full run 2 training
training="training_with_18_12_2019_wo_Mjj_training"$training_year #christmas full run 2 training

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
   # #python /work/nchernya//HHbbgg_ETH_devel/Limits/python/createReducedTrees.py -n $ntup -t $training  -o $outTag -a -y $year  -d 1  #with data
    python /work/nchernya//HHbbgg_ETH_devel/Limits/python/cleanCreateReducedTrees.py -n $ntup -t $training  -o $outTag -a -y $training_year  --flashggNames  $flashggNames

else
    python /work/nchernya//HHbbgg_ETH_devel/Limits/python/cleanCreateReducedTrees.py -n $ntup -t $training  -o $outTag -y $training_year -k 0 --flashggNames  $flashggNames    #with data add -d 1
fi
    
####transform MVA output
#python /work/nchernya//HHbbgg_ETH_devel/Limits/macros/transformMVAOutput.py -i '/work/nchernya//HHbbgg_ETH_devel/outfiles/'$outTag'/Total_preselection_diffNaming_2016_2017.root'

## For both years
## python /work/nchernya//HHbbgg_ETH_devel/Limits/macros/transformMVAOutputCommon.py -i '/work/nchernya/HHbbgg_ETH_devel/outfiles/20181210_common_2016/Total_preselection_diffNaming.root,/work/nchernya/HHbbgg_ETH_devel/outfiles/20181210_common_2017/Total_preselection_diffNaming.root'

## python /work/nchernya//HHbbgg_ETH_devel/Limits/macros/applyTransformMVAOutput.py -i '/work/nchernya/HHbbgg_ETH_devel/outfiles/20181210_common_2016_forcheck/Total_preselection_diffNaming.root' -g '/work/nchernya/HHbbgg_ETH_devel/Limits/macros/plots/cumulatives/cumulativeTransformation_20181210_common_2016_2017.root'
