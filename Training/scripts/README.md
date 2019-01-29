### How to submit jobs with ipython cluster 

* In you shome you have to create a .ipython directory (unless it is already there)
```
/shome/$USER/.ipython
```
* Copy one profile from Nadya :
```
cp -r /shome/nchernya/.ipython/profile_gcc49_5gb_smp1_all /shome/$USER/.ipython/
```
* Change your username, name of the queue and scratch area in this file : 
```
/shome/$USER/.ipython/profile_gcc49_5gb_smp1_all/ipcluster_config.py 
```
* Change memory or how many cpus in this file :
```
/shome/$USER/.ipython/profile_gcc49_5gb_smp1_all/scripts/engines_template

```
* Always first source the environment :
```
source HHbbgg_ETH_devel/scripts/setup_scikit.sh
```
* Run the engines in screen specifying number of desired jobs:
```
ipcluster start --profile=gcc49_5gb_smp1_all -n NJOBS
```
* *Wait untill all engines are running!*
* Once all engines are running, you can run your scipts which has this line inside :
```
optimization.setupJoblib("gcc49_5gb_smp1_all") # create all.q (> 6 hours) with  1 cpu core
```
