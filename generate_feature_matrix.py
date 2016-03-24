import pandas as pd
import numpy as np
import re
import MySQLdb

db = MySQLdb.connect("localhost","root","zoomzoom","GeneListDB")
cursor = db.cursor()

#input gene list
input_gene_list = ['AT1G09570','AT5G67560', 'AT5G67620', 'AT5G67620']

#annotate these according to presence/absence in gene lists
gene_list_names = ['chen2014_phyA_chip_seq']

gene_list_name = gene_list_names[0]

def generate_feature_matrix(input_gene_list,gene_list_names):
    feature_matrix = []
    
    for list_name in gene_list_names:
        sql_query = """SELECT locus_id FROM gene_lists WHERE list_name=%s;"""
        cursor.execute(sql_query,list_name)
        result = cursor.fetchall()
        returned_gene_list = [x[0] for x in result]
        
        #features for this list
        binary_feature_vector = [int(x in returned_gene_list) for x in input_gene_list]
        
        feature_matrix.append(binary_feature_vector)
    
    feature_matrix = np.array(feature_matrix).transpose()
    return feature_matrix

#print generate_feature_matrix(input_gene_list,gene_list_names)