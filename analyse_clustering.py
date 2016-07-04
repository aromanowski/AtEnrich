import numpy as np
import pandas as pd
from convert_clustering_to_classification import convert_clustering_to_classification
from rank_features import rank_features
from generate_feature_matrix import generate_feature_matrix
import os
import json
import re
import sqlite3

def analyse_clustering(clustering_file_location,output_filename,gene_list_names=None,cluster_indices=None):
    
    db = sqlite3.connect("GeneListDB.db")
    cursor = db.cursor()
    
    if not gene_list_names:
        #get default list of gene_list_names i.e. all gene lists
        cursor.execute("""SELECT list_name FROM list_info;""")
        gene_list_names = [x[0] for x in cursor.fetchall()]
        gene_list_names = [x for x in gene_list_names if not re.search('seaton2015',x)]
    
    
    with open(clustering_file_location) as data_file:
        cluster_data = json.load(data_file)
    
    gene_list = cluster_data['gene_list']
    cluster_list = cluster_data['labels']
    
    if not cluster_indices:
        #use default - analyse all clusters
        cluster_indices = list(set(cluster_list))
    
    #get a binary classification vector for each cluster
    clustering_classifications = convert_clustering_to_classification(cluster_list)
    
    #generate the accompanying feature matrix for all genes in the gene list
    feature_matrix = generate_feature_matrix(gene_list,gene_list_names)
    
    FR_df = pd.DataFrame(index=gene_list_names,columns=cluster_indices)
    
    for cluster_idx in cluster_indices:
        classification = clustering_classifications[cluster_idx]
        importances,std,indices = rank_features(gene_list,classification,
                                                feature_matrix,
                                                n_estimators=800,
                                                max_features=6,
                                                max_depth=6)
        FR_df[cluster_idx] = pd.Series(importances,index=gene_list_names)
    
    FR_df.to_csv(output_filename,sep='\t')
    
    db.close()
    
clustering_file_location = os.getenv('HOME')+'/Dropbox/Work/Circadian/Other projects/PhyA signalling/phya_data_analysis/whole_genome_clustering/'+'diurnal_clustering_090616.json'
output_filename = 'phyA_clustering_analysis_test.csv'
gene_list_names = None
#cluster_indices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,68]

analyse_clustering(clustering_file_location,output_filename,gene_list_names)