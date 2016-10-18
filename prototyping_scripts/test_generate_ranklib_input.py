from GAFER import analyse_clustering,clusterobj,expressiondata,generate_ranklib_input
import sqlite3
import os
import inspect
import pandas as pd
import re

main_dir = os.path.dirname(inspect.getfile(analyse_clustering))
data_dir = os.path.join(main_dir,'tests','test_data_files')

#database_file = os.path.join(data_dir,'DAPseqDB_test_subset.db')
database_file = os.getenv('HOME')+'/Dropbox/Work/Circadian/Data/OMalley2016, DAP-seq data/DAPseqDB.db'
table_name = 'TF_TG_associations'
feature_id_column = 'TF_locus_id'
target_id_column = 'TG_locus_id'

clustering_file_location = os.path.join(data_dir,'diurnal_clustering_300916.json')

cluster_indices = None

db = sqlite3.connect(database_file)
cursor = db.cursor()

method = 'pval'
FR_df_pval = analyse_clustering(clustering_file_location,cursor,feature_id_column,target_id_column,table_name,method=method,feature_list=None,excluded_features=None,cluster_indices=cluster_indices)
#FR_df_pval.loc['chen2014_phyA_induced',85]
print '1'

method = 'FE'
FR_df_FE = analyse_clustering(clustering_file_location,cursor,feature_id_column,target_id_column,table_name,method=method,feature_list=None,excluded_features=None,cluster_indices=cluster_indices)
#FR_df_FE.loc['chen2014_phyA_induced',85]
print '2'

db.close()

FR_df_pval.columns = pd.MultiIndex.from_tuples([('pval',x) for x in FR_df_pval.columns])
FR_df_FE.columns = pd.MultiIndex.from_tuples([('FE',x) for x in FR_df_FE.columns])

FR_df = pd.concat([FR_df_pval,FR_df_FE],axis=1)

candidate_reg = []
#select top 5 regulators for each cluster
nReg = 8
for cluster_idx in list(set(FR_df.columns.labels[1])):
    top_regulators = FR_df['pval',cluster_idx].nlargest(nReg).index.tolist()
    for regulator in top_regulators:
        candidate_reg.append((regulator,cluster_idx))


# Correlation judged based on subset of all data
home_dir = os.getenv('HOME')
data_dir = home_dir+'/Dropbox/Work/Circadian/Data/'

file_dict = {
'Rugnone2013':'Rugnone2013, LNK1 LNK2 RNASeq/GSE43865_processed.csv',
'Diurnal_photoperiod':'Diurnal (Mockler)/shortday_longday_processed.csv',
'Diurnal_lux':'Diurnal (Mockler)/COL_LDHH_lux-2_LDHH_processed.csv',
'Diurnal_lhyox':'Diurnal (Mockler)/LER_SD_lhyox_SD_processed.csv',
'Diurnal_phyb':'Diurnal (Mockler)/COL_SD_phyB9_SD_processed.csv'}

loeData = expressiondata.ExpressionData()
datasets = dict()
for key in file_dict.keys():
    filename = file_dict[key]
    eDF = pd.read_csv(data_dir+filename,index_col=0)
    all_data_cols = [x for x in eDF.columns if re.search('AVG',x)]
    eDF = eDF.loc[:,all_data_cols]
    datasets[key] = eDF
    eData[key] = eDF

cData = clusterobj.ClusterObj(clustering_file_location)

generate_ranklib_input.generate_ranklib_input(candidate_reg,eData,cData,FR_df,'test_data_files/ranklib_test_input.txt')

#feature_list = FR_df.columns.levels[0]
#for reg in candidate_reg:
#    regulator,cluster_idx = reg
#    try:
#        similarity = eData.mean_similarity(regulator,cData['cluster_gene_lists'][cluster_idx])
#    except KeyError:
#        similarity = 0.0
#    feature_data = [FR_df.loc[regulator,(x,cluster_idx)] for x in feature_list]
#    #Get into the right format
#    feature_data_string = [str(x+1)+':'+str(y) for x,y in enumerate(feature_data)]
#    print ' '.join([str(similarity),'qid:1']+feature_data_string)


#database_file = os.path.join(data_dir,'GeneListDB.db')
#table_name = 'gene_lists'
#feature_id_column = 'list_name'
#target_id_column = 'locus_id'
