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
    
#    db = sqlite3.connect("GeneListDB.db")
    db = sqlite3.connect("DAPseqDB.db")
    cursor = db.cursor()
    
    if not gene_list_names:
        #get default list of gene_list_names i.e. all gene lists
#        cursor.execute("""SELECT list_name FROM list_info;""")
        cursor.execute("SELECT TF_locus_id FROM TF_TG_associations GROUP BY TF_locus_id;")
        feature_list = [x[0] for x in cursor.fetchall()]
#        feature_names = [x for x in feature_list if not re.search('seaton2015',x)]
    
    
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
#    feature_matrix = generate_feature_matrix(gene_list,gene_list_names)
    feature_matrix = generate_feature_matrix(genes_of_interest,feature_list,cursor,sql_query="""SELECT TG_locus_id FROM TF_TG_associations WHERE TF_locus_id=?;""")
        
    FR_df = pd.DataFrame(index=feature_list,columns=cluster_indices)
    
    for cluster_idx in cluster_indices:
        classification = clustering_classifications[cluster_idx]
        importances,std,indices = rank_features(genes_of_interest,classification,
                                                feature_matrix,
                                                n_estimators=1200,
                                                max_features=7,
                                                max_depth=7)
        FR_df[cluster_idx] = pd.Series(importances,index=feature_list)
    
    FR_df.to_csv(output_filename,sep='\t')
    
    db.close()
    
clustering_file_location = os.getenv('HOME')+'/Dropbox/Work/Circadian/Other projects/PhyA signalling/phya_data_analysis/whole_genome_clustering/'+'diurnal_clustering_090616.json'
output_filename = 'DAPseq_GAFER_on_cluster_5_PIF_regulated.csv'
gene_list_names = None
cluster_indices = [5]

analyse_clustering(clustering_file_location,output_filename,gene_list_names,cluster_indices=cluster_indices)