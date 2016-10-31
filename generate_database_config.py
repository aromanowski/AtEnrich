import os
import json

home_dir = os.getenv('HOME')

config = dict()

data_dir = home_dir+'/Dropbox/Work/Data analysis/GeneListDB/'
config['GeneListDB'] = dict()
config['GeneListDB']['database_file'] = data_dir+'GeneListDB.db'
config['GeneListDB']['table_name'] = 'gene_lists'
config['GeneListDB']['feature_id_column'] = 'list_name'
config['GeneListDB']['target_id_column'] = 'locus_id'

data_dir = home_dir+'/Dropbox/Work/Circadian/Data/OMalley2016, DAP-seq data/'
config['DAPseqDB'] = dict()
config['DAPseqDB']['database_file'] = data_dir+'DAPseqDB.db'
config['DAPseqDB']['table_name'] = 'TF_TG_associations'
config['DAPseqDB']['feature_id_column'] = 'TF_locus_id'
config['DAPseqDB']['target_id_column'] = 'TG_locus_id'

with open('db_config.json', 'w') as f:
    json.dump(config, f)