import sys; sys.path.append("~/HHbbgg_ETH_devel/Training/python")
import matplotlib.pyplot as plt
import os


import random as rnd

from sklearn.utils.extmath import cartesian
import scipy.stats as stats

import random



# ---------------------------------------------------------------------------------------------------
class IO:
    ldata = os.path.expanduser("/shome/nchernya/HHbbgg_ETH_devel/root_files/")
    xdata = "/shome/nchernya//HHbbgg_ETH_devel/Training/output_files/"
    plotFolder = os.path.expanduser("/shome/nchernya//HHbbgg_ETH_devel/Training/plots/")
    signalName = []
    signalUseMixOfNodes = False
    signalWhichMixOfNodes = []
    signalMixOfNodesNormalizations = dict()
    signalTreeName = []
    backgroundName = []
    bkgTreeName = []
    dataName = []
    dataTreeName = []
    sigProc = []
    bkgProc = []
    dataProc = []
    sigYear = []  ### year : 0-2016,1-2017,2-2018. Categorical var
    bkgYear = []
    dataYear = []
    nSig=0
    nBkg=0
    nData=0
    signal_df = []
    background_df = []
    data_df= []
    
    cross_sections = {}

    @staticmethod
    def use_signal_nodes(useNodes,whichNodes,normalizations):
        if useNodes :
            IO.signalMixOfNodes = True
            IO.signalWhichMixOfNodes = whichNodes
            IO.signalMixOfNodesNormalizations = normalizations

            
   
    @staticmethod
    def add_signal(ntuples,sig, proc, treeName,year=0):
        IO.signalName.append(IO.ldata+ntuples+"/"+''.join(sig))
        IO.sigProc.append(proc)
        IO.nSig+=1
        IO.signalTreeName.append(treeName)
        IO.sigYear.append(year)

        
    @staticmethod
    def add_background(ntuples,bkg,proc,treeName,year=0):
        IO.backgroundName.append(IO.ldata+ntuples+"/"+''.join(bkg))
        IO.bkgProc.append(proc)
        IO.nBkg+=1
        IO.bkgTreeName.append(treeName)
        IO.bkgYear.append(year)


    
    @staticmethod
    def add_data(ntuples,data,proc,treeName,year=0):
        IO.dataName.append(IO.ldata+ntuples+"/"+''.join(data))
        IO.dataProc.append(proc)
        IO.nData+=1
        IO.dataTreeName.append(treeName)
        IO.dataYear.append(year)





    


