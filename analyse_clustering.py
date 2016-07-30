import numpy as np
import pandas as pd
from convert_clustering_to_classification import convert_clustering_to_classification
import rank_features
from generate_feature_matrix import generate_feature_matrix
import os
import json
import re
import sqlite3

def analyse_clustering(clustering_file_location,output_filename,cursor,feature_id_column,target_id_column,table_name,method='pval',feature_list=None,excluded_features=None,cluster_indices=None):
    
    #protect against SQL injection
    def scrub(input_string):
        return ''.join( chr for chr in input_string if (chr.isalnum() or chr=='_'))
    table_name = scrub(table_name)
    feature_id_column = scrub(feature_id_column)
    target_id_column = scrub(target_id_column)
    
    if not feature_list:
        #create default feature list
        sql_query = "SELECT {0} FROM {1} GROUP BY {0};".format(feature_id_column,table_name)
        cursor.execute(sql_query)
        feature_list = [x[0] for x in cursor.fetchall()]
    if excluded_features:
        feature_list = [x for x in feature_list if ~any([x==y for y in excluded_features])]

    with open(clustering_file_location) as data_file:
        cluster_data = json.load(data_file)
    
    genes_of_interest = cluster_data['gene_list']
    cluster_list = cluster_data['labels']
    
    if not cluster_indices:
        #use default - analyse all clusters
        cluster_indices = list(set(cluster_list))
    
    #get a binary classification vector for each cluster
    clustering_classifications = convert_clustering_to_classification(cluster_list)
    
    #generate the accompanying feature matrix for all genes in the gene list
    sql_query = """SELECT {0} FROM {1} WHERE {2}=?;""".format(target_id_column,table_name,feature_id_column)
    feature_matrix = generate_feature_matrix(genes_of_interest,feature_list,cursor,sql_query=sql_query)
        
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
    
    FR_df.to_csv(output_filename,sep='\t')
    