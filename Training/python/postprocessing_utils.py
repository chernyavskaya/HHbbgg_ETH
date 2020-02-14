import training_utils as utils

import numpy as np

# ---------------------------------------------------------------------------------------------------

def stackFeatures(df,additionalCut_names,rounding=6,SF=1,isData=0):
    vec = []
    dictVar = {}
    i = 0
    for featCounter in additionalCut_names:
        feat= featCounter.replace("noexpand:","")
        vec.append(np.round(np.asarray(df[feat]),rounding))
        dictVar [feat] = i
        i+=1

    if not isData:
        vec.append(np.multiply(np.asarray(df['weight']),SF))  
    else:
        w = (np.ones_like(utils.IO.data_df[0].index)).astype(np.int8)
        if 'bbggSelectionTree' in utils.IO.dataTreeName[0] : vec.append(np.multiply(w,df['isSignal']))
        else : vec.append(np.asarray(df['weight']))
    dictVar['weight'] = i
        


    totalVec = []
    for i in range(len(vec)):
        if i == 0:
            totalVec = vec[i]
        else:
            totalVec = np.column_stack((totalVec,vec[i]))

    return totalVec,dictVar



def applyCut(vec,varNum,cut,option='greater'):
    if option == 'greater':
        return vec[np.where(vec[:,varNum]>cut)]
    elif option == 'smaller':
        return vec[np.where(vec[:,varNum]<cut)]
    elif option == 'different':
        return vec[np.where(vec[:,varNum]!=cut)]



def cutInvariantMass(vec,varNum,xLow,xUp):
    nCleaned_massWindowDown = applyCut(vec,varNum,xLow)
    nCleaned_massWindow = applyCut(nCleaned_massWindowDown,varNum,xUp,'smaller')
    return nCleaned_massWindow


def saveTree(processPath,dictVar,vector,MVAVector=None,SF=1,nameTree="reducedTree"):
    from root_numpy import array2root
    i=0
    for key in dictVar.keys():

        if i == 0:
            writeMode='recreate'
            i=1
        else:
            writeMode='update'

        v=(np.asarray(vector[:,dictVar[key]]))
        name = key

        #if key=='CMS_hgg_mass':
        #    name = 'Mgg'
        #elif '*1.4826' in key:
        if '*1.4826' in key:
            name = key.replace('*1.4826','_gauss')
    #    elif 'event%2!=0' in key:
    #        name = key.replace('event%2!=0','event_odd')
    #    elif 'event%5!=0' in key:
    #        name = key.replace('event%5!=0','event_odd5')
     #   elif 'event%' in key:
     #       name = 'eventTrainedOn'

        if SF != 1:
            if key == 'weight':
                v = (np.multiply(np.asarray(v),SF))

        name = name.replace(".","").replace("(","").replace(")","").replace("/","_Over_").replace("Candidate","")
        v.dtype = [(name, np.float64)]


        array2root(v, processPath, nameTree, mode = writeMode)

    if MVAVector is not None: 
        v=(np.asarray(MVAVector.ravel()))
        v.dtype = [('MVAOutput', np.float64)]
        array2root(v, processPath, nameTree, mode ='update')
