import os
import re
import pandas as pd
from GAFER import *
home_dir = os.getenv('HOME')
data_dir = home_dir+'/Dropbox/Work/Circadian/Data/'

file_dict = {
'Rugnone2013':'Rugnone2013, LNK1 LNK2 RNASeq/GSE43865_processed.csv',
'Diurnal_photoperiod':'Diurnal (Mockler)/shortday_longday_processed.csv'}

#Initialise dataset in both alternative ways:

test1 = ExpressionData()
datasets = dict()
for key in file_dict.keys():
    filename = file_dict[key]
    eDF = pd.read_csv(data_dir+filename,index_col=0)
    all_data_cols = [x for x in eDF.columns if re.search('AVG',x)]
    eDF = eDF.loc[:,all_data_cols]
    datasets[key] = eDF
    test1[key] = eDF

test2 = ExpressionData(data_dict=datasets)

test1.mean_similarity('AT1G09570',['AT5G01320'])
test1.similar_genes('AT1G09570',0.9)

gene_subset = test1.gene_list[:15]
test1.select_gene_subset(gene_subset)
test1.generate_similarity_matrix()
test1.similarity(gene_subset[1],gene_subset[2])