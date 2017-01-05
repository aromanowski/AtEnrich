from GAFER import analyse_clustering,ClusterData
import os
import inspect

main_dir = os.path.dirname(inspect.getfile(analyse_clustering))
data_dir = os.path.join(main_dir,'tests','test_data_files')
clustering_file_location = os.path.join(data_dir,'diurnal_clustering_300916.json')
cData = ClusterData.from_json(clustering_file_location)
db_id = 'GeneListDB'
cluster_indices = [85]
feature_list = ['chen2014_phyA_induced']

method = 'pval'
FR_df = analyse_clustering(cData,db_id,method=method,feature_list=feature_list,excluded_features=None,cluster_indices=cluster_indices)
FR_df.loc['chen2014_phyA_induced',85]

method = 'FE'
FR_df = analyse_clustering(cData,db_id,method=method,feature_list=feature_list,excluded_features=None,cluster_indices=cluster_indices)
FR_df.loc['chen2014_phyA_induced',85]

feature_list = ['chen2014_phyA_induced','chen2014_phyA_chip_seq']
feature_combinations = [('chen2014_phyA_induced','chen2014_phyA_chip_seq')]

method = 'FE'
FR_df = analyse_clustering(cData,db_id,method=method,feature_list=feature_list,excluded_features=None,cluster_indices=cluster_indices,feature_combinations=feature_combinations)
FR_df.loc['chen2014_phyA_induced+chen2014_phyA_chip_seq',85]


feature_combinations = [['luo2010_GATA2ox_down','oh2014_BR_up'],
                        ['kobayashi2015_MYB3R3_chip_seq','kobayashi2015_myb3r135_up'],
['song2016_ABA_up','legnaioli2009_toc1_down'],
['baena-gonzalez2007_AKIN10_repressed','blasing2005_carbon_fixation_induced'],
['hornitschek2012_PIF5_chip_seq','oh2014_PIF4_chip_seq'],
['liu2016_PRR9_chip_seq','liu2016_PRR7_chip_seq'],
['liu2016_PRR9_chip_seq','liu2016_PRR7_chip_seq','nakamichi2009_prr975_up']]

feature_list = list(set([y for x in feature_combinations for y in x]))

method = 'pval'
cluster_indices = [3,48,94,97,100]
FR_df = analyse_clustering(cData,db_id,method=method,feature_list=feature_list,excluded_features=None,cluster_indices=cluster_indices,feature_combinations=feature_combinations)
#FR_df.loc['chen2014_phyA_induced+chen2014_phyA_chip_seq',85]
