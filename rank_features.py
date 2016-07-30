from sklearn.ensemble import ExtraTreesClassifier
from scipy.stats import hypergeom
import numpy as np
from generate_feature_matrix import generate_feature_matrix
from matplotlib.pyplot import *

def random_forest(input_gene_list,binary_classification,feature_matrix,n_estimators=400,max_features=None,max_depth=5):
    
    X = feature_matrix
    y = binary_classification
    
    nF = feature_matrix.shape[1]
    if not max_features:
        #set default value used by ExtraTreesClassifier
        max_features = int(nF**0.5)
    
    forest = ExtraTreesClassifier(n_estimators=n_estimators,
                                  max_features=max_features,
                                  max_depth=max_depth,
                                  random_state=0)
    
    forest.fit(X,y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)
    
    return importances,std,indices

def hypergeometric(binary_classification,feature_matrix):
    
    X = feature_matrix
    y = binary_classification
    nF = feature_matrix.shape[1]

    pvals = np.ones(nF) #p-values
    FE = np.ones(nF) #fold enrichment

    M = feature_matrix.shape[0] #total number of objects
    n = sum(y) #number in class
    for feature_idx in range(nF):
        N = sum(X[:,feature_idx]) #number positive for this feature
        k = sum(np.multiply(X[:,feature_idx],y))
        pvals[feature_idx] = hypergeom.sf(k,M,n,N)
        print k,n,N,M
        try:
            FE[feature_idx] = (float(k)/n)/(float(N)/M)
        except ZeroDivisionError:
            FE[feature_idx] = 1.0
    
    return pvals,FE