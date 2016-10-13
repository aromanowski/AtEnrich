### This function analyses a single gene list - substantial duplication with analyse_clustering - to combine in future

import numpy as np
import pandas as pd
from convert_clustering_to_classification import convert_clustering_to_classification
import rank_features
from generate_feature_matrix import generate_feature_matrix
import os
import json
import re
import sqlite3

def analyse_gene_list(gene_list,background_gene_list,output_filename,cursor,feature_id_column,target_id_column,table_name,method='pval',feature_list=None,excluded_features=None):
    """Generate enrichment statistics for a given set of clusters."""
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
    
    genes_of_interest = background_gene_list
        
    #get a binary classification vector for the list
    classification = [int(x in gene_list) for x in genes_of_interest]
    
    #generate the accompanying feature matrix for all genes in the gene list
    sql_query = """SELECT {0} FROM {1} WHERE {2}=?;""".format(target_id_column,table_name,feature_id_column)
    feature_matrix = generate_feature_matrix(genes_of_interest,feature_list,cursor,sql_query=sql_query)

    if method=='RF':
        importances,std,indices = rank_features.random_forest(genes_of_interest,classification,
                                                feature_matrix,
                                                n_estimators=1200,
                                                max_features=7,
                                                max_depth=7)
        FR_df = pd.Series(importances,index=feature_list)
    elif method=='pval':
        pvals,FE = rank_features.hypergeometric(classification,feature_matrix)
        FR_df = pd.Series(-np.log10(pvals),index=feature_list)
    elif method=='FE':
        pvals,FE = rank_features.hypergeometric(classification,feature_matrix)
        FR_df = pd.Series(FE,index=feature_list)
    
    FR_df.to_csv(output_filename,sep='\t')
    
    return FR_df
    