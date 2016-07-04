import numpy as np
import pandas as pd
from convert_clustering_to_classification import convert_clustering_to_classification
from rank_features import rank_features
from generate_feature_matrix import generate_feature_matrix
import os
import json
import re
import sqlite3

###TODO - make into function, and call it from a script
#def analyse_clustering(file,clusters_to_plot=None,gene_list_names=None,cluster_indices=None):

db = sqlite3.connect("GeneListDB.db")
cursor = db.cursor()


with open(os.getenv('HOME')+'/Dropbox/Work/Circadian/Other projects/PhyA signalling/phya_data_analysis/whole_genome_clustering/'+'diurnal_clustering_090616.json') as data_file:    
    cluster_data = json.load(data_file)

gene_list = cluster_data['gene_list']
cluster_list = cluster_data['labels']


#get a binary classification vector for each cluster
clustering_classifications = convert_clustering_to_classification(cluster_list)

#use all available lists
cursor.execute("""SELECT list_name FROM list_info;""")
gene_list_names = [x[0] for x in cursor.fetchall()]
gene_list_names = [x for x in gene_list_names if not re.search('seaton2015',x)]


feature_matrix = generate_feature_matrix(gene_list,gene_list_names)

cluster_indices = [5,8,14,68]

FR_df = pd.DataFrame(index=gene_list_names,columns=cluster_indices)

for cluster_idx in cluster_indices:
    #68 and 5 are phyA and PIFs respectively
    classification = clustering_classifications[cluster_idx]
    #for idx,classification in enumerate(clustering_classifications[72:73]):
    importances,std,indices = rank_features(gene_list,classification,
                                            feature_matrix,
                                            n_estimators=800,
                                            max_features=6,
                                            max_depth=6)
    FR_df[cluster_idx] = pd.Series(importances,index=gene_list_names)

FR_df.to_csv('cluster_analysis_test.csv',sep='\t')


# Plot the feature importances of the forest
nF = 12
FS = 20
figure()

for idx,cluster_idx in enumerate(cluster_indices):
    subplot(2,2,idx+1)
    top_values = FR_df[cluster_idx].nlargest(nF)
    barh(range(nF),top_values,color="r",align="center")
    yticks(range(nF), top_values.index)
    ylim([-1, nF])


db.close()