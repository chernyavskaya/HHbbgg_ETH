# Training NN on CSCS cluster in Lugano

### Setting up the environment 
Connecting to CSCS
```
ssh username@ela.cscs.ch
ssh daint
```
Copy /users/musella/env.sh in '~ /env.sh'. In the copied file '~' has to be changed into "~musella" in order to be able to source Pasquale's environment. 

Source Pasqaule's environment :
```
source /users/musella/my-env/bin/activate
```
Close daint. To check out the repo first generate the key by 'ssh-keygen' and add it to github. Then checko-out repo
```
git clone -b ETH_regression git@github.com:chernyavskaya/HHbbgg_ETH.git
```
Create jupyter folder and link it notebooks(or python maybe better) to bregression project inside
```
mkdir jupyter
cd jupyter
ln -s ../HHbbgg_ETH/bregression/notebooks/ bregression
```
Inside bin/ create bin/start_jupyter . Change the port number to something else.
```
#!/bin/bash 
source ~/env.sh
cd ~/jupyter 
jupyter notebook --port 9999 --no-browser
 ```
 Make start_jupyter executable
 ```
 chmod 755 bin/start_jupyter
 ```
 
 
 Create .ssh/config. The port numbers inside this confid should be the same as in the one above.
 ```
Host daint*
LocalForward 9999 localhost:9999
LocalForward 6666 localhost:6666

Host *
ControlMaster auto
ControlPath ~/.ssh/master-%r@%h:%p
```

On your own laptop create .ssh/config. The port numbers inside this confid should be the same as in the one above.
```
Host cscs
LocalForward 9999 localhost:9999
LocalForward 6666 localhost:6666
User username
HostName ela.cscs.ch
```
To be able to access the jupyter notebook later from the web-interface connect to local host:
```
ssh cscs
```

Now back to cscs:
```
mkdir -p ~/.ipython/profile_default/startup/
```
Adding basic python config ~/.ipython/profile_default/startup/00-basics.ipy :
```
cat ~/.ipython/profile_default/startup/00-basics.ipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

try:
    reload  # Python 2.7
except NameError:
    try:
        from importlib import reload  # Python 3.4+
    except ImportError:
        from imp import reload  # Python 3.0 - 3.3


try:
    %matplotlib inline
except:
    pass
matplotlib.style.use('seaborn-poster')
plt.rcParams['image.cmap'] = 'bwr'
plt.rcParams['figure.figsize'] = '10,10'
```
Nice screen set up to see the tabs inside
```
~musella/.screenrc
```
Start jupyter in screen :
```
start_jupyter
```
Open the notebook in the browser with the printed by jupyter token.

Add config file to run jobs 'my_jobs.sh' in the bregression directory(where you run the training), in this case the directory is '~/jupyter/bregression'
```
cat my_job.sh
#!/bin/bash -l
#SBATCH --job-name=job_name
#SBATCH --mail-type=ALL
#SBATCH --mail-user=username@cern.ch   ## Change the email
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --partition=normal
#SBATCH --constraint=gpu
#SBATCH -A d78

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export CRAY_CUDA_MPS=1

source $HOME/env.sh

cd $HOME/jupyter/bregression
srun $@
```


## Training NN

#### First of all, each time source the environment :
```
source env.sh
```

Training file :
./train_ffwd.py --help

To train locally : 
train_ffwd.py --inp-dir=/scratch/snx3000/musella/bregression --out-dir test --loss mse

To submit a job and run interactively on the resources allocated by the job:
```
salloc -C gpu
srun ./train_ffwd.py --inp-dir=/scratch/snx3000/musella/bregression --out-dir test --loss mse
```
To stop the interactive process ctr+C ctrl+C twice
To exit the job : exit

To submit a proper batch job:
```
sbatch my_job.sh -J <name> <command> <options>
```
e.g
```
sbatch my_job.sh -J  test_job  train_ffwd.py --inp-dir=/scratch/snx3000/musella/bregression --out-dir test2 --loss mse 
```
To check allocated job resources:
```
sacct 
```
The log file is writen in the same directory unless it is changed by giving the option -o 'where_to_write_log'

```
tail -f slurm-5610450.out
```
After the job is done (or during the job) all the hdf5 files and metrics.csv and config.json with all hyper parameters of the NN are written to the output directory specified in the command option


#### To prepare a json file with hyperparameters and architecture  
Prepare a grid of parameters of interest in the script 'prepare_NN_setup.py'
```
python prepare_NN_setup.py
```
Print command to submit jobs
```
python submit_jobs.py --njobs 1 --jdir 2018-02-03_17_55_01
```
This will print the command that runs the jobs on GPUs. Copy and paste the output to run the jobs. Script can be modified very easily to submit jobs directly, I just prefer to have a look before I submit

# Prepare plots for paper

### Input files for 2016 :
/scratch/nchernya/HHbbgg/paper/output_root
### Commands to make plots :
ipython plot_IQR2_paper.py -- --inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5 --sample-name ttbar
ipython plot_IQR2_paper.py -- --inp-file applied_res_2018-07-20_ZHbbll_morevar.hd5 --sample-name ZHbbll
ipython plot_IQR2_paper.py -- --inp-file applied_res_2018-07-20_HHres700_morevar.hd5 --sample-name HHbbgg700
ipython plot_IQR2_paper.py -- --inp-file applied_res_2018-07-20_HHres500_morevar.hd5 --sample-name HHbbgg500
ipython plot_IQR2_paper.py -- --inp-file applied_res_2018-07-20_HHresSM_morevar.hd5 --sample-name HHbbggSM

ipython plots_for_paper_improvement.py -- --inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5 --sample-name ttbar --labels 'DNN'

ipython plot_resEstimatorFunc_paper.py -- --inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5 --sample-name ttbar

#### Check effect of regression on semi-leptonic and hadronic decays separately
ipython plot_IQR2_paper.py -- --inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5 --sample-name ttbar --where 'isOther==1'
ipython plot_IQR2_paper.py -- --inp-file applied_res_2018-07-20_ttbar_full_RegressionPerJet_heppy_energyRings_testing_morevar.hd5 --sample-name ttbar --where 'isOther==0'

