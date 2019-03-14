import training_utils as utils
import os
import numpy as np
import pandas as pd
import root_pandas as rpd
from ROOT import TFile, TH1F


def cleanOverlapDiphotons(name,dataframe):
    dataframe['overlapSave']  = np.ones_like(dataframe.index).astype(np.int8)
    if ('DiPhotonJetsBox_MGG' in name) : 
      #for data this wont be called anyway
      for index, df in dataframe.iterrows(): 
        cflavLeading = 0 #correct flavours
        hflav = df['leadingJet_hflav'] #4 if c, 5 if b, 0 if light jets
        pflav = df['leadingJet_pflav']
        if  hflav != 0 :
            cflavLeading = hflav
        else : #not a heavy jet
            if abs(pflav) == 4 or abs(pflav) == 5 :
                cflavLeading = 0 
            else : cflavLeading = pflav
        
        cflavSubLeading = 0 
        hflav = df['subleadingJet_hflav'] #4 if c, 5 if b, 0 if light jets
        pflav = df['subleadingJet_pflav']
        if  hflav != 0 :
            cflavSubLeading = hflav
        else : #not a heavy jet
            if abs(pflav) == 4 or abs(pflav) == 5 :
                cflavSubLeading = 0 
            else : cflavSubLeading = pflav
            
            
        if abs(cflavSubLeading)==5 or abs(cflavLeading)==5 :
            dataframe.at[index,'overlapSave']=0
        else : dataframe.at[index,'overlapSave']=1
  #  dataframe["weight"] *= dataframe['overlapSave']

    
        


def define_process_weight(df,proc,name,treename='bbggSelectionTree',cleanSignal=True,cleanOverlap=False):
    df['proc'] = ( np.ones_like(df.index)*proc ).astype(np.int8)
    if treename=='bbggSelectionTree':
        df['weight'] = ( np.ones_like(df.index)).astype(np.float32)
        input_df=rpd.read_root(name,treename, columns = ['genTotalWeight', 'lumiFactor','isSignal','puweight'])
        w = np.multiply(input_df[['lumiFactor']],input_df[['genTotalWeight']])
        w = np.multiply(w,input_df[['puweight']])
        df['lumiFactor'] = input_df[['lumiFactor']]
        df['genTotalWeight'] = input_df[['genTotalWeight']]
        df['isSignal'] = input_df[['isSignal']]
        if cleanSignal:#some trees include also the control region,select only good events
            df['weight']= np.multiply(w,input_df[['isSignal']])
        else:
            df['weight']=w

    if cleanOverlap : cleanOverlapDiphotons(name,df)
 

        
def reweight_MX():
    df0, df1 = utils.IO.signal_df
    m0, bins = np.histogram(df0['MX'],bins=np.linspace(200.,2000.,101),weights=df0["weight"],normed=True)
    m1, _ = np.histogram(df1['MX'],bins=bins,weights=df1["weight"],normed=True)
    weights = m0.astype(np.float32) / m1.astype(np.float32)
    weights[np.where(bins[:-1]>1000)] = 1.
    weights[np.isnan(weights)] = 1.
    bins[-1] = df1["MX"].max()+1.
    df1["MXbin"] = pd.cut(df1["MX"],bins,labels=range(0,bins.shape[-1]-1))
    rewei = df1[["MXbin","weight"]].apply(lambda x: weights[x[0]]*x[1], axis=1, raw=True)
    df1["weight"] = rewei * df1["weight"].sum() / rewei.sum()


def reweight(what,df0,df1):
    m0, bins = np.histogram(df0[what],bins=np.linspace(200,2000,101),weights=df0["weight"],normed=True)
    m1, _ = np.histogram(df1[what],bins=bins,weights=df1["weight"],normed=True)
    weights = m0.astype(np.float32) / m1.astype(np.float32)
    weights[np.isnan(weights)] = 1.
    bins[-1] = df1[what].max()+1.
    df1["%s_bin"%what] = pd.cut(df1[what],bins,labels=range(0,bins.shape[-1]-1))
    rewei = df1[["%s_bin"%what,"weight"]].apply(lambda x: weights[x[0]]*x[1], axis=1, raw=True)
    df1["weight"] = rewei * df1["weight"].sum() / rewei.sum()
    
    
    
    
def reweight_gen_mhh(what,df0,df1,df_reweight,what2):
    m0, bins = np.histogram(df0[what],bins=np.linspace(200,2000,101),weights=df0["weight"],normed=True)
    m1, _ = np.histogram(df1[what],bins=bins,weights=df1["weight"],normed=True)
    weights = m0.astype(np.float32) / m1.astype(np.float32)
    weights[np.where(bins[:-1]>1800)] = 1.
    weights[np.isnan(weights)] = 1.
    bins[-1] = df_reweight[what2].max()+1.
    df_reweight["%s_bin"%what2] = pd.cut(df_reweight[what2],bins,labels=range(0,bins.shape[-1]-1))
    rewei = df_reweight[["%s_bin"%what2,"weight"]].apply(lambda x: weights[x[0]]*x[1], axis=1, raw=True)
    df_reweight["weight"] = rewei * df_reweight["weight"].sum() / rewei.sum()
    
    
    

def reweight_MX_old(dataframe):
    dataframe['tmp']  = np.ones_like(dataframe.index).astype(np.int8)
    file = TFile("/mnt/t3nfs01/data01/shome/nchernya/HHbbgg_ETH_devel/root_files/ntuples_2017data_20181023/Node_reweighting_hist.root")
    hist = file.Get("ratio")
    integral_before = dataframe['weight'].sum()
    for index, df in dataframe.iterrows(): 
        MX = df['MX']
        weight = df['weight']
        if (MX<1000):
            print dataframe['weight']
            dataframe.at[index,'weight']=weight*hist.GetBinContent(hist.FindBin(MX))
            print dataframe['weight']
            #dataframe.at[index,'weight']=weight*hist.GetBinContent(hist.FindBin(MX))
        break
    print dataframe['weight']
    integral_after = dataframe['weight'].sum()
    print 'Reweighting MX : '
    print 'Integral before, after and ratio = ',integral_before,integral_after,integral_before/integral_after
    dataframe['weight'] *= integral_before/integral_after


def scale_lumi(dataframe):
    print 'Weighting with lumi : '
    dataframe['weight'] *= 41.5/35.9  #scale with lumi 2017
    
    
def define_process_weight_CR(df,proc,name,treename='bbggSelectionTree'):
    df['proc'] = ( np.ones_like(df.index)*proc ).astype(np.int8)
    df['weight'] = ( np.ones_like(df.index)).astype(np.float32)
    input_df=rpd.read_root(name,treename, columns = ['isPhotonCR'])
    w = input_df[['isPhotonCR']]
    df['weight']=w

    
def clean_signal_events(x_b, y_b, w_b,x_s,y_s,w_s,event_num_bkg = None, event_num_sig = None):#some trees include also the control region,select only good events
    if (event_num_bkg is None and event_num_sig is None) : return x_b[np.where(w_b!=0),:][0],y_b[np.where(w_b!=0)],w_b[np.where(w_b!=0)], x_s[np.where(w_s!=0),:][0], np.asarray(y_s)[np.where(w_s!=0)],np.asarray(w_s)[np.where(w_s!=0)]
    else : 
        return x_b[np.where(w_b!=0),:][0],y_b[np.where(w_b!=0)],w_b[np.where(w_b!=0)],event_num_bkg[np.where(w_b!=0)], x_s[np.where(w_s!=0),:][0], y_s[np.where(w_s!=0)],w_s[np.where(w_s!=0)],event_num_sig[np.where(w_s!=0)]

    
    
def clean_signal_events_single_dataset(x_b, y_b, w_b):#some trees include also the control region,select only good events
    return x_b[np.where(w_b!=0),:][0],np.asarray(y_b)[np.where(w_b!=0)],np.asarray(w_b)[np.where(w_b!=0)]

   
    
    
def normalize_process_weights_split_all(w,y):
    sum_weights_b = 0
    sum_weights_s = 0
    proc_considered = []
    for proc in np.unique(y):
        if proc!=1:  #fist bkg
            w_proc = np.asarray(w[np.asarray(y) == proc])
            sum_weights_b += float(np.sum(w_proc))
        else : 
            w_proc = np.asarray(w[np.asarray(y) == proc])
            sum_weights_s += float(np.sum(w_proc))
        proc_considered.append(proc)
    w[np.where(y==1)] = np.divide(w[np.where(y==1)],sum_weights_s)
    w[np.where(y!=1)] = np.divide(w[np.where(y!=1)],sum_weights_b)

    return w



                     
def normalize_process_weights_split(w_b,y_b,w_s,y_s):
    sum_weights = 0
    proc_considered = []
    for proc in np.unique(y_b):
        w_proc = np.asarray(w_b[np.asarray(y_b) == proc])
        sum_weights += float(np.sum(w_proc))
        proc_considered.append(proc)
    w_bkg = np.divide(w_b,sum_weights)


    sum_weights = 0
    proc_considered = []
    for proc in np.unique(y_s):
        w_proc = np.asarray(w_s[np.asarray(y_s) == proc])
        sum_weights += float(np.sum(w_proc))
        proc_considered.append(proc)
    w_sig = np.divide(w_s,sum_weights)

    return w_bkg,w_sig


    
    
                       
def normalize_process_weights(w_b,y_b,w_s,y_s):
    proc=999
    proc_considered = []
    sum_weights = 1
    w_bkg = []
    for i in range(utils.IO.nBkg):
        if utils.IO.bkgProc[i] not in proc_considered :
            #w_proc = np.asarray(np.absolute(w_b[np.asarray(y_b) == utils.IO.bkgProc[i]]))#absolute is important to normalize in case of negative weights
            w_proc = np.asarray(w_b[np.asarray(y_b) == utils.IO.bkgProc[i]])
            sum_weights = float(np.sum(w_proc))
            proc = utils.IO.bkgProc[i]
            proc_considered.append(proc)
            if i==0:
                w_bkg = np.divide(w_proc,sum_weights)
            else:
                w_bkg = np.concatenate((w_bkg, np.divide(w_proc,sum_weights)))
           
        utils.IO.background_df[i][['weight']] = np.divide(utils.IO.background_df[i][['weight']],sum_weights)


    proc=999
    proc_considered = []
    sum_weights = 1
    w_sig = []
    for i in range(utils.IO.nSig):
        if utils.IO.sigProc[i] not in proc_considered:
            w_proc = np.asarray(w_s[np.asarray(y_s) == utils.IO.sigProc[i]])
            sum_weights = np.sum(w_proc)
            proc = utils.IO.sigProc[i]
            proc_considered.append(proc)
            if i==0:
                w_sig = np.divide(w_proc,sum_weights)
            else:
                w_sig = np.concatenate((w_sig, np.divide(w_proc,sum_weights)))
        utils.IO.signal_df[i][['weight']] = np.divide(utils.IO.signal_df[i][['weight']],sum_weights)

    return w_bkg,w_sig




#def normalize_process_weights_all():
#    sum_weights = 1
#    
#    for proc in np.unique(utils.IO.bkgProc):
#        for i in range(utils.IO.nBkg):
#            if utils.IO.bkgProc[i]==proc:
#                sum_weights+=sum(utils.IO.background_df[i]['weight'])
#        for i in range(utils.IO.nBkg):
#            if utils.IO.bkgProc[i]==proc: 
#                utils.IO.background_df[i][['weight']] = np.divide(utils.IO.background_df[i][['weight']],sum_weights)
#
#    sum_weights = 1
#        
#    for proc in np.unique(utils.IO.sigProc):
#        for i in range(utils.IO.nSig):
#            if utils.IO.sigProc[i]==proc:
#                sum_weights+=sum(utils.IO.signal_df[i]['weight'])
#        for i in range(utils.IO.nSig):
#            if utils.IO.sigProc[i]==proc: 
#                utils.IO.signal_df[i][['weight']] = np.divide(utils.IO.signal_df[i][['weight']],sum_weights)
        
        

def scale_process_weight(w_b,y_b,proc,sf):
    w_bkg = []
    process=999
    for i in range(utils.IO.nBkg):
        if utils.IO.bkgProc[i] == proc:
            utils.IO.background_df[i][['weight']] = np.multiply(utils.IO.background_df[i][['weight']],sf)
            w_proc = np.asarray(utils.IO.background_df[i][['weight']])
        else:
            if process == utils.IO.bkgProc[i]: #don't do twice multiple samples of same process, like GJet
                continue
            process =  utils.IO.bkgProc[i]
            w_b = np.reshape(w_b,(len(w_b),1))


            w_proc = np.asarray(w_b[np.asarray(y_b) == utils.IO.bkgProc[i]])
            w_proc = np.reshape(w_proc,(len(w_proc),1))
            
        if i == 0:
            w_bkg = w_proc
        else:
            w_bkg =  np.concatenate((w_bkg,w_proc))

    return w_bkg.reshape(len(w_bkg),1) 


def weight_signal_with_resolution_all(branch='sigmaMOverMDecorr'):
    for i in range(utils.IO.nSig):
        utils.IO.signal_df[i][['weight']] = np.divide(utils.IO.signal_df[i][['weight']],utils.IO.signal_df[i][[branch]])

def weight_signal_with_resolution(w_s,y_s,branch='sigmaMOverMDecorr'):
    w = []
    proc=999
    for i in range(utils.IO.nSig):
        w_sig = np.asarray(w_s[np.asarray(y_s) == utils.IO.sigProc[i]])
        proc = utils.IO.sigProc[i]
        utils.IO.signal_df[i][['weight']] = np.divide(utils.IO.signal_df[i][['weight']],utils.IO.signal_df[i][[branch]])
        w.append(utils.IO.signal_df[i][['weight']])
    #return utils.IO.signal_df[i][['weight']]
    all_signal = pd.concat([w[i] for i in range(0,len(w))],ignore_index=True)
    return all_signal

def weight_signal_with_resolution_bjet(w_s,y_s,branch='(sigmaMJets*1.4826)'):
    w = []
    proc=999
    for i in range(utils.IO.nSig):
        w_sig = np.asarray(w_s[np.asarray(y_s) == utils.IO.sigProc[i]])
        proc = utils.IO.sigProc[i]
        utils.IO.signal_df[i][['weight']] = np.divide(utils.IO.signal_df[i][['weight']],utils.IO.signal_df[i][[branch]])
        w.append(utils.IO.signal_df[i][['weight']])
    #return utils.IO.signal_df[i][['weight']]
    all_signal = pd.concat([w[i] for i in range(0,len(w))],ignore_index=True)
    return all_signal


def weight_background_with_resolution(w_b,y_b,proc,branch='sigmaMOverMDecorr'):
    w_bkg = []
    process=999
    for i in range(utils.IO.nBkg):
        if utils.IO.bkgProc[i] == proc:
            
            utils.IO.background_df[i][['weight']] = np.divide(utils.IO.background_df[i][['weight']],utils.IO.background_df[i][[branch]])
            w_proc = np.asarray(utils.IO.background_df[i][['weight']])
            np.reshape(w_proc,(len(utils.IO.background_df[i][['weight']]),))
        else:
            if process == utils.IO.bkgProc[i]: #don't do twice multiple samples of same process, like GJet
                continue
            process =  utils.IO.bkgProc[i]
            w_proc = np.asarray(w_b[np.asarray(y_b) == utils.IO.bkgProc[i]])

        if i == 0:
            w_bkg = w_proc
        else:
            w_bkg =  np.concatenate((w_bkg,np.asarray(w_proc.ravel())))
        
            
    return w_bkg.reshape(len(w_bkg),1)




def get_training_sample(x,splitting=0.5):
    halfSample = int((x.size/len(x.columns))*splitting)
    return np.split(x,[halfSample])[0]


def get_test_sample(x,splitting=0.5):
    halfSample = int((x.size/len(x.columns))*splitting)
    return np.split(x,[halfSample])[1]

    
def get_total_training_sample(x_sig,x_bkg,splitting=0.5):
    x_s=pd.DataFrame(x_sig)
    x_b=pd.DataFrame(x_bkg)
    halfSample_s = int((x_s.size/len(x_s.columns))*splitting)
    halfSample_b = int((x_b.size/len(x_b.columns))*splitting)
    return np.concatenate([np.split(x_s,[halfSample_s])[0],np.split(x_b,[halfSample_b])[0]])

    
def get_total_test_sample(x_sig,x_bkg,splitting=0.5):
    x_s=pd.DataFrame(x_sig)
    x_b=pd.DataFrame(x_bkg)
    halfSample_s = int((x_s.size/len(x_s.columns))*splitting)
    halfSample_b = int((x_b.size/len(x_b.columns))*splitting)
    return np.concatenate([np.split(x_s,[halfSample_s])[1],np.split(x_b,[halfSample_b])[1]])

def get_total_test_sample_event_num(x_sig,x_bkg,event_sig,event_bkg):
    x_s = x_sig[np.where(event_sig%2==0)]
    x_b = x_bkg[np.where(event_bkg%5==0)]
    return np.concatenate((x_s,x_b))

def get_total_training_sample_event_num(x_sig,x_bkg,event_sig,event_bkg):
    x_s = x_sig[np.where(event_sig%2!=0)]
    x_b = x_bkg[np.where(event_bkg%5!=0)]
    return np.concatenate((x_s,x_b))



def set_signals(branch_names,shuffle,cuts='event>=0'):
    for i in range(utils.IO.nSig):
        treeName = utils.IO.signalTreeName[i]
        print "using tree:"+treeName
        utils.IO.signal_df.append((rpd.read_root(utils.IO.signalName[i],treeName, columns = branch_names)).query(cuts))
        define_process_weight(utils.IO.signal_df[i],utils.IO.sigProc[i],utils.IO.signalName[i],treeName)
        utils.IO.signal_df[i]['year'] = (np.ones_like(utils.IO.signal_df[i].index)*utils.IO.sigYear[i] ).astype(np.int8)

        if shuffle:
            utils.IO.signal_df[i]['random_index'] = np.random.permutation(range(utils.IO.signal_df[i].index.size))
            utils.IO.signal_df[i].sort_values(by='random_index',inplace=True)
            
#         adjust_and_compress(utils.IO.signal_df[i]).to_hdf('/tmp/micheli/signal.hd5','sig',compression=9,complib='bzip2',mode='a')

       
    

def set_backgrounds(branch_names,shuffle,cuts='event>=0'):
    for i in range(utils.IO.nBkg):
        treeName = utils.IO.bkgTreeName[i]
        print "using tree:"+treeName
        utils.IO.background_df.append((rpd.read_root(utils.IO.backgroundName[i],treeName, columns = branch_names)).query(cuts))
        define_process_weight(utils.IO.background_df[i],utils.IO.bkgProc[i],utils.IO.backgroundName[i],treeName)
        utils.IO.background_df[i]['year'] = (np.ones_like(utils.IO.background_df[i].index)*utils.IO.bkgYear[i] ).astype(np.int8)

        if shuffle:
            utils.IO.background_df[i]['random_index'] = np.random.permutation(range(utils.IO.background_df[i].index.size))
            utils.IO.background_df[i].sort_values(by='random_index',inplace=True)

#         adjust_and_compress(utils.IO.background_df[i]).to_hdf('/tmp/micheli/background.hd5','bkg',compression=9,complib='bzip2',mode='a')



def set_data(branch_names,cuts='event>=0'):
    treeName = utils.IO.dataTreeName[0]
    utils.IO.data_df.append((rpd.read_root(utils.IO.dataName[0],treeName, columns = branch_names)).query(cuts))
    utils.IO.data_df[0]['proc'] =  ( np.ones_like(utils.IO.data_df[0].index)*utils.IO.dataProc[0] ).astype(np.int8)
    utils.IO.data_df[0]['year'] = (np.ones_like(utils.IO.data_df[0].index)*utils.IO.dataYear[0] ).astype(np.int8)

    if treeName=='bbggSelectionTree':
       input_df=rpd.read_root(utils.IO.dataName[0],treeName, columns = ['isSignal'])
       w = (np.ones_like(utils.IO.data_df[0].index)).astype(np.int8)
       utils.IO.data_df[0]['weight'] = np.multiply(w,input_df['isSignal'])


def set_variables_data(branch_names):
    y_data = utils.IO.data_df[0][['proc']]
    w_data = utils.IO.data_df[0][['weight']]
    for j in range(len(branch_names)):
        if j == 0:
            X_data = utils.IO.data_df[0][[branch_names[j].replace('noexpand:','')]]
        else:
            X_data = np.concatenate([X_data,utils.IO.data_df[0][[branch_names[j].replace('noexpand:','')]]],axis=1)
    
    return np.round(X_data,5),y_data,w_data
    
    

def set_signals_and_backgrounds(branch_names,shuffle=True,cuts='event>=0'):
    #signals will have positive process number while bkg negative ones
    set_signals(branch_names,shuffle,cuts)
    set_backgrounds(branch_names,shuffle,cuts)

    
def set_signals_and_backgrounds_drop(branch_names,shuffle=True,cuts='event>=0'):
    #signals will have positive process number while bkg negative ones
    set_signals_drop(branch_names,shuffle,cuts)
    set_backgrounds(branch_names,shuffle,cuts)
    
    

def randomize(X,y,w,event_num=None,seed=0):
    randomize=np.arange(len(X))
    np.random.seed(seed)
    np.random.shuffle(randomize)
    X = X[randomize]
    y = np.asarray(y)[randomize]
    w = np.asarray(w)[randomize]
    if event_num is None :
        event_num = np.asarray(event_num)[randomize]
        return X,y,w
    else : 
        return X,y,w,event_num
    
    
    
def set_variables(branch_names,use_event_num=False):
    for i in range(utils.IO.nSig):
        if i ==0:
            y_sig = utils.IO.signal_df[i][['proc']]
            w_sig = utils.IO.signal_df[i][['weight']]
            if use_event_num :  event_sig = utils.IO.signal_df[i][['event']]
            for j in range(len(branch_names)):
                if j == 0:
                    X_sig = utils.IO.signal_df[i][[branch_names[j].replace('noexpand:','')]]
                else:
                    X_sig = np.concatenate([X_sig,utils.IO.signal_df[i][[branch_names[j].replace('noexpand:','')]]],axis=1)
        else:
            y_sig = np.concatenate((y_sig,utils.IO.signal_df[i][['proc']]))
            w_sig = np.concatenate((w_sig,utils.IO.signal_df[i][['weight']]))
            if use_event_num : event_sig = np.concatenate((event_sig,utils.IO.signal_df[i][['event']]))
            for j in range(len(branch_names)):
                if j == 0:
                    X_sig_2 = utils.IO.signal_df[i][[branch_names[j].replace('noexpand:','')]]
                else:
                    X_sig_2 = np.concatenate([X_sig_2,utils.IO.signal_df[i][[branch_names[j].replace('noexpand:','')]]],axis=1)
            X_sig=np.concatenate((X_sig,X_sig_2))

    for i in range(utils.IO.nBkg):
        if i ==0:
            y_bkg = utils.IO.background_df[i][['proc']]
            w_bkg = utils.IO.background_df[i][['weight']]
            if use_event_num : event_bkg = utils.IO.background_df[i][['event']]
            for j in range(len(branch_names)):
                if j == 0:
                    X_bkg = utils.IO.background_df[i][[branch_names[j].replace('noexpand:','')]]
                else:
                    X_bkg = np.concatenate([X_bkg,utils.IO.background_df[i][[branch_names[j].replace('noexpand:','')]]],axis=1)
        else:
            y_bkg = np.concatenate((y_bkg,utils.IO.background_df[i][['proc']]))
            w_bkg = np.concatenate((w_bkg,utils.IO.background_df[i][['weight']]))
            if use_event_num : event_bkg = np.concatenate((event_bkg,utils.IO.background_df[i][['event']]))
            for j in range(len(branch_names)):
                if j == 0:
                    X_bkg_2 = utils.IO.background_df[i][[branch_names[j].replace('noexpand:','')]]
                else:
                    X_bkg_2 = np.concatenate([X_bkg_2,utils.IO.background_df[i][[branch_names[j].replace('noexpand:','')]]],axis=1)
            X_bkg=np.concatenate((X_bkg,X_bkg_2))

    if not use_event_num :  return np.round(X_bkg,5),y_bkg,w_bkg,np.round(X_sig,5),y_sig,w_sig
    else :   return np.round(X_bkg,5),y_bkg,w_bkg,event_bkg,np.round(X_sig,5),y_sig,w_sig,event_sig

   

def check_for_nan(df,branch_name='event'):
    print df.isnull().sum()
    index = df[branch_name].index[df[branch_name].apply(np.isnan)]
    print 'event numbers for nan events : ', df['event'][index]
    new_df = df.drop(df.index[index])
    return new_df


    
def drop_from_df(df,index):
    return df.drop(df.index[index])

def drop_nan(df):
    return df.dropna()

def profile(target,xvar,bins=10,range=None,uniform=False,moments=True,
            quantiles=np.array([0.25,0.5,0.75])):

    if range is None:
        if type(bins) is not int:
            xmin, xmax = bins.min(), bins.max()
        else:
            xmin, xmax = xvar.min(),xvar.max()
    else:
        xmin, xmax = range
    mask = ( xvar >= xmin ) & ( xvar <= xmax )
    xvar = xvar[mask]
    target = target[mask]
    if type(bins) == int:
        if uniform:
            bins = np.linspace(xmin,xmax,num=bins+1)
        else:
            ## print(xmin,xmax)
            ## xvar = np.clip( xvar, xmin, xmax )
            bins = np.percentile( xvar, np.linspace(0,100.,num=bins+1) )
            bins[0] = xmin
            bins[-1] = xmax
    print bins.shape 
    ibins = np.digitize(xvar,bins)-1
    categories = np.eye(np.max( ibins ) + 1)[ibins]

    ret = [bins]
    if moments:
        mtarget = target.reshape(-1,1) * categories
        weights = categories
        mean = np.average(mtarget,weights=categories,axis=0)
        mean2 = np.average(mtarget**2,weights=categories,axis=0)
        ret.extend( [mean, np.sqrt( mean2 - mean**2)] )
    if quantiles is not None:
        values = []
        print(categories.shape[1])
        for ibin in np.arange(categories.shape[1],dtype=int):
            values.append( np.percentile(target[categories[:,ibin].astype(np.bool)],quantiles*100.,axis=0).reshape(-1,1) )
            ## print(values)
        ret.append( np.concatenate(values,axis=-1) )
    return tuple(ret)
