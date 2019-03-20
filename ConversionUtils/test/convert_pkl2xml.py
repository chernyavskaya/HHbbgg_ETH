#import FWCore.ParameterSet.Config as cms
from time import time,ctime
import sys,os
from tree_convert_pkl2xml import tree_to_tmva, BDTxgboost, BDTsklearn
import sklearn
from collections import OrderedDict
from sklearn.externals import joblib
#print('The scikit-learn version is {}.'.format(sklearn.__version__))
import pandas
#print('The pandas version is {}.'.format(pandas.__version__))
import cPickle as pickle
#print('The pickle version is {}.'.format(pickle.__version__))
import numpy as np
#print('The numpy version is {}.'.format(np.__version__))
#sys.path.insert(0, '/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/py2-pippkgs_depscipy/3.0-njopjo7/lib/python2.7/site-packages')
import xgboost as xgb
#print('The xgb version is {}.'.format(xgb.__version__))
import subprocess
from sklearn.externals import joblib
from itertools import izip
from optparse import OptionParser, make_option
from  pprint import pprint

#features = ['leadingJet_bDis', 'subleadingJet_bDis', 'leadingPhotonSigOverE', 'subleadingPhotonSigOverE', 'sigmaMOverMDecorr', 'PhoJetMinDr']
#features = ['leadingJet_bDis','subleadingJet_bDis','noexpand:fabs(CosThetaStar_CS)','noexpand:fabs(CosTheta_bb)','noexpand:fabs(CosTheta_gg)','noexpand:diphotonCandidate.Pt()/diHiggsCandidate.M()','noexpand:dijetCandidate.Pt()/diHiggsCandidate.M()','customLeadingPhotonIDMVA','customSubLeadingPhotonIDMVA','leadingPhotonSigOverE','subleadingPhotonSigOverE','sigmaMOverMDecorr','PhoJetMinDr']
#features = 'leadingJet_bDis,subleadingJet_bDis,absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverMDecorr,PhoJetMinDr,noexpand:(leadingJet_bRegNNResolution*1.4826),noexpand:(subleadingJet_bRegNNResolution*1.4826),noexpand:(sigmaMJets*1.4826)'.split(',')
features = 'Mjj,leadingJet_DeepCSV,subleadingJet_DeepCSV,absCosThetaStar_CS,absCosTheta_bb,absCosTheta_gg,diphotonCandidatePtOverdiHiggsM,dijetCandidatePtOverdiHiggsM,customLeadingPhotonIDMVA,customSubLeadingPhotonIDMVA,leadingPhotonSigOverE,subleadingPhotonSigOverE,sigmaMOverM,PhoJetMinDr,rho,noexpand:(leadingJet_bRegNNResolution*1.4826),noexpand:(subleadingJet_bRegNNResolution*1.4826),noexpand:(sigmaMJets*1.4826)'.split(',')

#this is just for testing if you want to check on one event, be careful, you have to put the correct variables
#new_dict = OrderedDict([('leadingJet_bDis',0.9889938831329346),('subleadingJet_bDis',0.0648464784026146),('leadingPhotonSigOverE',0.005494383163750172),('subleadingPhotonSigOverE',0.0067262412048876286),('sigmaMOverMDecorr',0.006000000052154064),('PhoJetMinDr',1.1405941247940063)])
#new_dict = OrderedDict([('Mjj',124.533355713 ), ('leadingJet_DeepCSV',0.972642123699 ), ('subleadingJet_DeepCSV',0.999983489513 ), ('absCosThetaStar_CS',0.45063740015 ), ('absCosTheta_bb',0.940612137318 ), ('absCosTheta_gg',0.0112659092993 ), ('diphotonCandidatePtOverdiHiggsM',0.240908399224 ), ('dijetCandidatePtOverdiHiggsM',0.367229014635 ), ('customLeadingPhotonIDMVA',0.887370824814 ), ('customSubLeadingPhotonIDMVA',0.856965243816 ), ('leadingPhotonSigOverE',0.0125171979889 ), ('subleadingPhotonSigOverE',0.0151416249573 ), ('sigmaMOverM',0.0138915274292 ), ('PhoJetMinDr',1.9266756773 ), ('rho',7.73644113541 ), ('noexpand:(leadingJet_bRegNNResolution*1.4826)',0.14936208725 ), ('noexpand:(subleadingJet_bRegNNResolution*1.4826)',0.14936208725 ), ('noexpand:(sigmaMJets*1.4826)',0.0911846831441 )])
new_dict = OrderedDict([('Mjj',124.533 ), ('leadingJet_DeepCSV',0.972642  ), ('subleadingJet_DeepCSV',0.999983 ), ('absCosThetaStar_CS',0.450637 ), ('absCosTheta_bb',0.940612 ), ('absCosTheta_gg',0.0112659 ), ('diphotonCandidatePtOverdiHiggsM', 0.240908), ('dijetCandidatePtOverdiHiggsM', 0.367229), ('customLeadingPhotonIDMVA',0.887371 ), ('customSubLeadingPhotonIDMVA',0.856965 ), ('leadingPhotonSigOverE', 0.0125172), ('subleadingPhotonSigOverE',0.0151416 ), ('sigmaMOverM',0.0138915 ), ('PhoJetMinDr',1.92668 ), ('rho',7.73644 ), ('noexpand:(leadingJet_bRegNNResolution*1.4826)',0.149362 ), ('noexpand:(subleadingJet_bRegNNResolution*1.4826)',0.103986 ), ('noexpand:(sigmaMJets*1.4826)',0.0911847 )])


def main(options,args):

    inputFile = options.inFile
    outputFile = inputFile.split('/')[-1].replace('.pkl','.weights.xml')

    result=-20
    fileOpen = None
    try:
        fileOpen = open(inputFile, 'rb')
    except IOError as e:
        print('Couldnt open or write to file (%s).' % e)
    else:
        print ('file opened')
        try:
#            pkldata = pickle.load(fileOpen)
            pkldata = joblib.load(fileOpen)
            print pkldata
        except :
            print('Oops!',sys.exc_info()[0],'occured.')
        else:
            print ('pkl loaded')
            print (pkldata)

            bdt = BDTxgboost(pkldata, features, ["Background","Background2", "Signal"])
            bdt.to_tmva(outputFile)
            print "xml file is created with name : ", outputFile

            if options.test:#this is just for testing if you want to check on one event uncomment here
                proba = pkldata.predict_proba([[ new_dict[feature] for feature in features]])
                #proba = pkldata.predict_proba([[ new_dict[feature] for feature in features]])[:,pkldata.n_classes_-1].astype(np.float64)
                print "proba= ",proba
                result = proba[:,1][0]
                print ('predict BDT to one event',result)
                

             #   test_eval = bdt.eval([ new_dict[feature] for feature in features])
             #   print "XGboost test_eval = ", test_eval
             #   test_eval_tmva = bdt.eval_tmva([ new_dict[feature] for feature in features])
             #   print "TMVA test_eval = ", test_eval_tmva

            fileOpen.close()
    return result

if __name__ == "__main__":
    parser = OptionParser(option_list=[
            make_option("-i", "--infile",
                        action="store", type="string", dest="inFile",
                        default="",
                        help="input file",
                        ),
            make_option("-t", "--test",
                        action="store_true", dest="test",
                        default=False,
                        help="test on one event",
                        ),
            ]
                          )

    (options, args) = parser.parse_args()
    sys.argv.append("-b")

    
    pprint(options.__dict__)

    import ROOT

    main(options,args)

