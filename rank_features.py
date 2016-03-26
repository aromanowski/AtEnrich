from sklearn.ensemble import ExtraTreesClassifier
import numpy as np
from generate_feature_matrix import generate_feature_matrix
from matplotlib.pyplot import *

def rank_features(input_gene_list,binary_classification,gene_list_names):
    
    X = generate_feature_matrix(input_gene_list,gene_list_names)
    y = binary_classification
    
    forest = ExtraTreesClassifier(n_estimators=350,
                                  random_state=0)
    
    forest.fit(X,y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    
    
    # Print the feature ranking
    print("Feature ranking:")
    
    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
    
    # Plot the feature importances of the forest
    figure()
    title("Feature importances")
    bar(range(X.shape[1]), importances[indices],
        color="r", yerr=std[indices], align="center")
    xticks(range(X.shape[1]), [gene_list_names[x] for x in indices],rotation=90)
    xlim([-1, X.shape[1]])
    tight_layout()
    
    return importances,std,indices