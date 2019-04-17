#source $VO_CMS_SW_DIR/cmsset_default.sh
# shopt -s expand_aliases is needed if you want to use the alias 'cmsenv' created by $VO_CMS_SW_DIR/cmsset_default.sh instead of the less mnemonic eval `scramv1 runtime -sh`

source $VO_CMS_SW_DIR/cmsset_default.sh
source /swshare/psit3/etc/profile.d/cms_ui_env.sh  # for bash

export MYCMSENVDIR=/work/nchernya/CMSSW_9_4_5_cand1/src/
cd $MYCMSENVDIR
eval `scramv1 runtime -sh`
shopt -s expand_aliases 
cmsenv
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/dcap 

export MYBATCHDIR=/work/nchernya/HHbbgg_ETH_devel/submit_jobs/2018/
cd $MYBATCHDIR

#./test_root $1 $2 $3 $TMPDIR/$4 
./a_root $1 $2 $3 $TMPDIR/$4 

#xrdfs t3se01.psi.ch rm  /store/user/nchernya/HHbbgg/b_regression/ttbar_2017_nanoAOD_v3_newJEC/${4}_RegressionPerJet_nanoAOD_2017_${3}.root

xrdcp -f $TMPDIR/${4}_RegressionPerJet_nanoAOD_2018_${3}.root  root://t3dcachedb.psi.ch:1094//pnfs/psi.ch/cms/trivcat//store/user/nchernya/HHbbgg/b_regression/ttbar_2018_16April2019/

#$ -o /mnt/t3nfs01/data01/shome/nchernya/batch_logs/
#$ -e /mnt/t3nfs01/data01/shome/nchernya/batch_logs/
