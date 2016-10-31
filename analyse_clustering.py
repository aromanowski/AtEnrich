import numpy as np
import pandas as pd
from convert_clustering_to_classification import convert_clustering_to_classification
import rank_features
from generate_feature_matrix import generate_feature_matrix

def analyse_clustering(cData,db_id,method='pval',feature_list=None,excluded_features=None,cluster_indices=None):
    """Generate enrichment statistics for a given set of clusters.
    
    >>> from GAFER import analyse_clustering,ClusterObj
    >>> import os
    >>> import inspect
    >>> 
    >>> main_dir = os.path.dirname(inspect.getfile(analyse_clustering))
    >>> data_dir = os.path.join(main_dir,'tests','test_data_files')
    >>> clustering_file_location = os.path.join(data_dir,'diurnal_clustering_300916.json')
    >>> cData = ClusterObj.from_json(clustering_file_location)
    >>> db_id = 'GeneListDB'
    >>> cluster_indices = [85]
    >>> feature_list = ['chen2014_phyA_induced']
    >>> 
    >>> method = 'pval'
    >>> FR_df = analyse_clustering(cData,db_id,method=method,feature_list=feature_list,excluded_features=None,cluster_indices=cluster_indices)
    >>> FR_df.loc['chen2014_phyA_induced',85]
    23.982050404665358
    >>> method = 'FE'
    >>> FR_df = analyse_clustering(cData,db_id,method=method,feature_list=feature_list,excluded_features=None,cluster_indices=cluster_indices)
    >>> FR_df.loc['chen2014_phyA_induced',85]
    4.0285602503912354
    """
    
    genes_of_interest = cData['gene_list']
    cluster_list = cData['labels']
    
    if not cluster_indices:
        #use default - analyse all clusters
        cluster_indices = list(set(cluster_list))
    
    #get a binary classification vector for each cluster
    clustering_classifications = convert_clustering_to_classification(cluster_list)
    
    #generate feature matrix
    feature_matrix,feature_list = generate_feature_matrix(genes_of_interest,feature_list,excluded_features,db_id)
    
    FR_df = pd.DataFrame(index=feature_list,columns=cluster_indices)
    
    for cluster_idx in cluster_indices:
        classification = clustering_classifications[cluster_idx]
        if method=='RF':
            importances,std,indices = rank_features.random_forest(genes_of_interest,classification,
                                                    feature_matrix,
                                                    n_estimators=1200,
                                                    max_features=7,
                                                    max_depth=7)
            FR_df[cluster_idx] = pd.Series(importances,index=feature_list)
        elif method=='pval':
            pvals = rank_features.hypergeometric(classification,feature_matrix)
            FR_df[cluster_idx] = pd.Series(-np.log10(pvals),index=feature_list)
        elif method=='FE':
            FE = rank_features.FE(classification,feature_matrix)
            FR_df[cluster_idx] = pd.Series(FE,index=feature_list)
        
    return FR_df

if __name__ == "__main__":
    import doctest
    doctest.testmod()