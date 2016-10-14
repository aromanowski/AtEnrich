import numpy as np
import pandas as pd
from convert_clustering_to_classification import convert_clustering_to_classification
import rank_features
from generate_feature_matrix import generate_feature_matrix
import json

def analyse_clustering(clustering_file_location,cursor,feature_id_column,target_id_column,table_name,method='pval',feature_list=None,excluded_features=None,cluster_indices=None):
    """Generate enrichment statistics for a given set of clusters.
    
    >>> import sqlite3
    >>> import os
    >>> import inspect
    >>> 
    >>> main_dir = os.path.dirname(inspect.getfile(analyse_clustering))
    >>> data_dir = os.path.join(main_dir,'tests','test_data_files')
    >>> database_file = os.path.join(data_dir,'GeneListDB.db')
    >>> table_name = 'gene_lists'
    >>> feature_id_column = 'list_name'
    >>> target_id_column = 'locus_id'
    >>> 
    >>> clustering_file_location = os.path.join(data_dir,'diurnal_clustering_300916.json')
    >>> 
    >>> cluster_indices = [85]
    >>> 
    >>> db = sqlite3.connect(database_file)
    >>> cursor = db.cursor()
    >>> 
    >>> method = 'pval'
    >>> FR_df = analyse_clustering(clustering_file_location,cursor,feature_id_column,target_id_column,table_name,method=method,feature_list=None,excluded_features=None,cluster_indices=cluster_indices)
    >>> FR_df.loc['chen2014_phyA_induced',85]
    23.982050404665358
    >>> 
    >>> method = 'FE'
    >>> FR_df = analyse_clustering(clustering_file_location,cursor,feature_id_column,target_id_column,table_name,method=method,feature_list=None,excluded_features=None,cluster_indices=cluster_indices)
    >>> FR_df.loc['chen2014_phyA_induced',85]
    4.0285602503912354
    >>>
    >>> db.close()"""
    

    with open(clustering_file_location) as data_file:
        cluster_data = json.load(data_file)
    
    genes_of_interest = cluster_data['gene_list']
    cluster_list = cluster_data['labels']
    
    if not cluster_indices:
        #use default - analyse all clusters
        cluster_indices = list(set(cluster_list))
    
    #get a binary classification vector for each cluster
    clustering_classifications = convert_clustering_to_classification(cluster_list)
    
    #generate feature matrix
    feature_matrix,feature_list = generate_feature_matrix(genes_of_interest,feature_list,excluded_features,feature_id_column,target_id_column,table_name,cursor)
    
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
            pvals,FE = rank_features.hypergeometric(classification,feature_matrix)
            FR_df[cluster_idx] = pd.Series(-np.log10(pvals),index=feature_list)
        elif method=='FE':
            pvals,FE = rank_features.hypergeometric(classification,feature_matrix)
            FR_df[cluster_idx] = pd.Series(FE,index=feature_list)
        
    return FR_df

if __name__ == "__main__":
    import doctest
    doctest.testmod()