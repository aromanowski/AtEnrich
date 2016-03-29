from sklearn.ensemble import ExtraTreesClassifier
import numpy as np
from generate_feature_matrix import generate_feature_matrix
from matplotlib.pyplot import *

def rank_features(input_gene_list,binary_classification,feature_matrix,n_estimators=400,max_features=None):
    
    X = feature_matrix
    y = binary_classification
    
    nF = feature_matrix.shape[1]
    if not max_features:
        #set default value used by ExtraTreesClassifier
        max_features = int(nF**0.5)
    
    forest = ExtraTreesClassifier(n_estimators=n_estimators,
                                  max_features=max_features,
                                  random_state=0)
    
    forest.fit(X,y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)
    
    
    # Print the feature ranking
    print("Feature ranking:")
    
    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
    
    return importances,std,indices