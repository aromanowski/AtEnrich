import numpy as np
import pandas as pd
from convert_clustering_to_classification import convert_clustering_to_classification
from rank_features import rank_features
from connect_to_db import connect_to_db

db = connect_to_db()
cursor = db.cursor()

#input cluster file
cluster_df = pd.read_csv('phya_clustering.csv',header=None)

gene_list = cluster_df[0].tolist()
cluster_list = cluster_df[1].tolist()

#get a binary classification vector for each cluster
clustering_classifications = convert_clustering_to_classification(cluster_list)

#use all available lists
cursor.execute("""SELECT list_name FROM list_info;""")
gene_list_names = [x[0] for x in cursor.fetchall()]

#for idx,classification in enumerate(clustering_classifications):
#    rank_features(gene_list,classification,gene_list_names,n_estimators=1000)
#    title(idx)

importances,std,indices = rank_features(gene_list,clustering_classifications[9],
                                        gene_list_names,
                                        n_estimators=2500,
                                        max_features=4)

# Plot the feature importances of the forest
figure()
title("Feature importances")
barh(range(len(indices)), importances[indices],
     color="r", xerr=std[indices], align="center")
yticks(range(len(indices)), [gene_list_names[x] for x in indices])
ylim([-1, len(indices)])
tight_layout()

db.close()