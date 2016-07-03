import numpy as np
import pandas as pd
from convert_clustering_to_classification import convert_clustering_to_classification
from rank_features import rank_features
from connect_to_db import connect_to_db
from generate_feature_matrix import generate_feature_matrix
import os
import json
import re

###TODO - make into function, and call it from a script
#def analyse_clustering(file,clusters_to_plot=None,gene_list_names=None,cluster_indices=None):

db = connect_to_db()
cursor = db.cursor()

##input cluster file
##cluster_file = 'phya_clustering.csv'
##cluster_file = os.getenv('HOME')+'/Dropbox/Work/Circadian/Data/Yadav2014, SAM transcriptomes/yadav2014_clustering.csv'
##cluster_file = os.getenv('HOME')+'/Dropbox/Work/Circadian/Data/Yadav2014, SAM transcriptomes/yadav2014_clustering_corr.csv'
#cluster_file = os.getenv('HOME')+'/Dropbox/Work/Circadian/Other projects/PhyA signalling/phya_data_analysis/whole_genome_clustering/diurnal_clustering_200416.csv'
#cluster_df = pd.read_csv(cluster_file,header=None,sep='\t')
#
#gene_list = cluster_df[0].tolist()
#cluster_list = cluster_df[1].tolist()


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
#gene_list_names = [
#'bhargava2013_CK_down',
#'bhargava2013_CK_up',
#'busch2010_WUS_chip_chip',
#'cheminant2011_ga1_DELLA_global_down',
#'cheminant2011_ga1_DELLA_global_up',
#'cheminant2011_ga1_down',
#'cheminant2011_ga1_up',
#'chen2014_FHY1_chip_seq',
#'chen2014_phyA_chip_seq',
#'chen2014_phyA_induced',
#'chen2014_phyA_repressed',
#'hornitschek2012_PIF5_chip_seq',
#'kamioka2016_CCA1_chip_seq',
#'lee2007_HY5_chip_chip',
#'liu2013_PRR7_chip_seq',
#'liu2016_PRR5_chip_seq',
#'liu2016_PRR7_chip_seq',
#'liu2016_PRR9_chip_seq',
#'liu2016_TOC1_chip_seq',
#'luo2010_GATA2ox_down',
#'luo2010_GATA2ox_up',
#'nakamichi2009_prr975_down',
#'nakamichi2009_prr975_up',
#'nakamichi2012_PRR5_chip_seq',
#'nakamichi2012_PRR5_target',
#'oh2014_ARF6_chip_seq',
#'oh2014_BR_down',
#'oh2014_BR_up',
#'oh2014_BZR1_chip_seq',
#'oh2014_iaa3_down',
#'oh2014_iaa3_up',
#'oh2014_PIF4_chip_seq',
#'ouyang2011_FHY3_chip_seq',
#'pfeiffer2014_PIF1_chip_seq',
#'pfeiffer2014_PIF4_chip_seq',
#'sun2010_BZR1_chip_chip',
#'yadav2013_WUS-GR_down',
#'yadav2013_WUS-GR_up',
#'zhang2013_PIF3_chip_seq']



feature_matrix = generate_feature_matrix(gene_list,gene_list_names)

#importances,std,indices = rank_features(gene_list,clustering_classifications[9],
#                                        feature_matrix,
#                                        n_estimators=2500,
#                                        max_features=4)
#
## Plot the feature importances of the forest
#figure()
#title("Feature importances")
#barh(range(len(indices)), importances[indices],
#     color="r", xerr=std[indices], align="center")
#yticks(range(len(indices)), [gene_list_names[x] for x in indices])
#ylim([-1, len(indices)])
#tight_layout()

#72 is PIFs
#3 is carbon and sugar

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



# Plot the feature importances of the forest

nF = 12
FS = 20
figure()
#title(clustering_idx)
#    title("Feature importances")
#    barh(range(len(indices)), importances[indices],
#         color="r", xerr=std[indices], align="center")
#bar(range(len(indices)), importances[indices])
#xticks([])
#ylabel('Importance',fontsize=FS)
#xlabel('Features',fontsize=FS)
#barh(range(len(indices)), importances[indices],
#     color="r", align="center")
#yticks(range(len(indices)), [gene_list_names[x] for x in indices])
#ylim([-1, len(indices)])
#tight_layout()

#barh(range(nF), importances[indices[-nF:]],
#     color="r", align="center")
#yticks(range(nF), [gene_list_names[x] for x in indices[-nF:]])
#ylim([-1, nF])
#tight_layout()


for idx,cluster_idx in enumerate(cluster_indices):
    subplot(2,2,idx+1)
    top_values = FR_df[cluster_idx].nlargest(nF)
    barh(range(nF),top_values,color="r",align="center")
    yticks(range(nF), top_values.index)
    ylim([-1, nF])





db.close()