import pandas as pd
import numpy as np
import re
import sqlite3

def generate_feature_matrix(genes_of_interest,feature_list,sql_query="""SELECT locus_id FROM gene_lists WHERE list_name=?;""",database_file="GeneListDB.db"):
    feature_matrix = []
    
    for feature_name in feature_list:
        returned_gene_list = query_database(sql_query,feature_name,database_file)
        #features for this list
        binary_feature_vector = [int(x in returned_gene_list) for x in genes_of_interest]
        feature_matrix.append(binary_feature_vector)
    
    feature_matrix = np.array(feature_matrix).transpose()
    return feature_matrix

db = sqlite3.connect("GeneListDB.db")
cursor = db.cursor()

def query_database(sql_query,list_name,database_file):
    cursor.execute(sql_query,[list_name])
    result = cursor.fetchall()
    returned_gene_list = [x[0] for x in result]
    return returned_gene_list