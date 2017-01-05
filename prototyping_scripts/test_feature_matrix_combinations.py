from GAFER import generate_feature_df
from GAFER.generate_feature_matrix import add_combined_features
import os
import inspect

db_id = 'GeneListDB'
feature_list = ['chen2014_phyA_induced','chen2014_phyA_chip_seq']
genes_of_interest = [u'AT5G20070', 'AT3G51240', u'AT1G05170', u'AT3G21700', u'AT5G65460', u'AT1G15960', u'AT5G02270', u'AT5G10230', u'AT3G51240', u'AT1G56670']

excluded_features = None

m = generate_feature_df(genes_of_interest,feature_list,excluded_features,db_id)

list_of_combinations = [('chen2014_phyA_induced','chen2014_phyA_chip_seq')]

m = add_combined_features(m,list_of_combinations)