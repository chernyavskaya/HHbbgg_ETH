Prepare b-jet regerssion training, check perfomance, fit the distibutions, make plots

All notebooks were written only as a starting point, once a notebook is written to some working level , I convert them to python scripts for speed reasons. All code here makes use of functions written in ../python directory 
### To make plots for paper
```
python bjet_pt_eta.py
```

```
ipython plot_IQR2_paper.py -- --inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5 --sample-name ttbar
```

```
ipython plots_for_paper_improvement.py -- --inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5 --sample-name ttbar --labels DNN
```

```
ipython plot_resEstimatorFunc_paper.py -- --inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5
```
Info for the plots above :  --inp-dir /scratch/nchernya/HHbbgg/paper/output_root/   --sample-name ttbar —training 2018-04-06_job23_2016 -inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5 --sample-name ttbar

### Training Regression
```
ipython trainBreg_jobs.py
ipython trainBreg_quatile.py alpha
where alpha equals to the qunatile you want to train to
```
This will save the weight '.pkl' file in the ../output_files/ directory
### Applying Regression

For quantile regerssion then we need to add 3 BDT outputs (3 quantiles 0.2,0.4,0.7) to the tree
```
ipython applyRegQuantile.py
```
Other 3 scripts are availbale with different python or ROOT minimization and fiing packages:
```
applyRegQuantile_advanced.py  applyRegQuantile_curve.py  applyRegQuantile.py  applyRegQuantile_root.py
```
### Evaluating and comparing performance of the regression

Once this is done we can make compare the performance of different regressions :
```
ipython compare.py sample_name
where samplename = ttbar or ZHbbll or for DiHiggs sm, res500 and res700
```
For all of the 3 samples one need to change the root file name unfotnately at this moment
This compare script will fit Bukin funciton to the Jet_mcPt/Jet_regerssed_pt in all given pt and eta regions

Then to compare the Bukin sigma and peak value Xp:
```
ipython chooseTheBest.py sample_name
where sample_name= ttbar or ZHbbll or for DiHiggs sm, res500 and res700
```
To create Bukin fits in the bins of resolution obtained with Quantile regression
```
ipython resolution.py sample_name
```
Then to compare the Bukin sigma and peak value Xp:
ipython sigma_resolution.py ttbar

To create inclusive plots to compare all samples at the same time :
```
sigma_resolution_all.py
chooseTheBest_all.py  -  need to recomment things , because this script can make 2 plots : inclusive sigma for all samples and different regressions and also al sample pT regions for only 1 regression
```

### Study that was done with quantiles
```
ipython plotQuantiles.py
```

### Plotting
## Plot inputs features
```
plotFeatures.py
```
## Plot regerssion profile
```
RegressionProfile.py
```
## Helping scripts that were used only as intermediary 
```
CaterinaComparison.py
compareScale.py
```


## Plotting results of NN

#### Evaluate NN on different files
```
ipython -i predict_fit_ffwd.py -- --training mse,HybridLoss --inp-file ggHHbbgg_sm_RegressionPerJet_heppy_energyRings3_forTraining_Large0.hd5
ipython -i predict_fit_ffwd.py -- --inp-file ttbar_RegressionPerJet_heppy_energyRingsFloat78_forTesting.hd5 --inp-dir /scratch/snx3000/nchernya/bregression/for_test/ --target-dir /scratch/snx3000/nchernya/bregression/NN_output//2018-02-13_13_25_54_job23/

```
####
Fit evaluated regression with Bukin 
```
python fit_ffwd.py --training mse,HybridLoss --sample-name ggHHbbgg_sm --inp-file applied_ggHHbbgg_sm_RegressionPerJet_heppy_energyRings3_forTraining_Large0.hd5
```
Plot money plots using Bukin Fits. (there is a possibility to compare with scikit, first parameter new name of file and second for old scikit naming convention -> better rewrite at some point)
```
ipython chooseTheBestNN.py ggHHbbgg_sm DiHiggs_sm
```

#### Plot quantiles vs pt and eta, IQR/2 vs sigma/pt, IQR/2 vs eta and pt
```
ipython plot_IQR2.py -- --sample-name ZHbbll --inp-file applied_res_ZHbbll_RegressionPerJet_heppy_energyRings3_forTraining_LargeAll3.hd5
ipython plot_IQR2.py -- --sample-name ggHHbbgg_res700  --inp-file applied_res_ggHHbbgg_res700_RegressionPerJet_heppy_energyRings3_forTraining_Large0.hd5
```

### Plot comparison between two different trainings (for example training without JER,JER and on top of JEC)
```
ipython plot_comparisonReg.py -- --sample-name ttbar --inp-file applied_res_2018-02-06_ttbar_RegressionPerJet_heppy_energyRings3_forTesting.hd5,applied_res_2018-02-13_ttbar_RegressionPerJet_heppy_energyRingsFloat78_forTesting.hd5 --training 2018-02-06_12_22_19_job23,HybridLoss --labels raw,onJEC

ipython plot_comparisonReg.py -- --training 2018-02-13_13_25_54_job23,2018-02-27_job40_2,2018-02-27_job23 --inp-file applied_res_2018-02-28_ttbar_full_RegressionPerJet_heppy_energyRings_testing.hd5,applied_res_2018-02-28_ttbar_full_RegressionPerJet_heppy_energyRings_testing.hd5,applied_res_2018-02-28_ttbar_full_RegressionPerJet_heppy_energyRings_testing.hd5 --sample-name ttbar --labels 5M_job23,100M_job40v2,100M_job23
```
Binned in eta bins:
```
ipython plot_comparisonReg.py -- --sample-name ZHbbll --inp-file  applied_res_2018-02-06_ZHbbll_RegressionPerJet_heppy_energyRings3_forTraining_LargeAll3.hd5,applied_res_2018-02-13_ZHbbll_RegressionPerJet_heppy_energyRings3_forTraining_LargeAll3.hd5 --training 2018-02-06_12_22_19_job23,HybridLoss --labels raw,onJEC --where '(Jet_eta<1.75&Jet_eta>1.)|(-Jet_eta<1.75&-Jet_eta>1.0)'
```

### Plot comparsion of training/validation for different jobs (one job only, change of learning rate, dropout or just diffenrent jobs)
plot_epoch.py,plot_xvalepoch_learningrate.py,plot_xvalepoch_dropout.py,best_score_jobs.py and just for different jobs : best_score_compare.py
```
ipython best_score_compare.py -- --training 2018-02-27_job40_2,2018-02-27_job23 --inp-dir /scratch/snx3000/nchernya/bregression/NN_output/ --metrics loss,mae0,mae100,mae200,mae50,mse0,mse100,mse200,mse50,r2_score0 --out-dir /users/nchernya/HHbbgg_ETH/bregression/plots/NN_epochs/2018-02-27/
```

