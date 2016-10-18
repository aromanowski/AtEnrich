from GAFER import analyse_clustering
import sqlite3
import os
import inspect

main_dir = os.path.dirname(inspect.getfile(analyse_clustering))
data_dir = os.path.join(main_dir,'tests','test_data_files')
database_file = os.path.join(data_dir,'GeneListDB.db')
table_name = 'gene_lists'
feature_id_column = 'list_name'
target_id_column = 'locus_id'

clustering_file_location = os.path.join(data_dir,'diurnal_clustering_300916.json')

cluster_indices = [85]

db = sqlite3.connect(database_file)
cursor = db.cursor()

method = 'pval'
FR_df = analyse_clustering(clustering_file_location,cursor,feature_id_column,target_id_column,table_name,method=method,feature_list=None,excluded_features=None,cluster_indices=cluster_indices)
FR_df.loc['chen2014_phyA_induced',85]

method = 'FE'
FR_df = analyse_clustering(clustering_file_location,cursor,feature_id_column,target_id_column,table_name,method=method,feature_list=None,excluded_features=None,cluster_indices=cluster_indices)
FR_df.loc['chen2014_phyA_induced',85]

db.close()