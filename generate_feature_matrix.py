import pandas as pd
import numpy as np
import re
from connect_to_db import connect_to_db

db = connect_to_db()
cursor = db.cursor()

def generate_feature_matrix(input_gene_list,gene_list_names):
    feature_matrix = []
    
    for list_name in gene_list_names:
        sql_query = """SELECT locus_id FROM gene_lists WHERE list_name=%s;"""
        cursor.execute(sql_query,[list_name])
        result = cursor.fetchall()
        returned_gene_list = [x[0] for x in result]
        
        #features for this list
        binary_feature_vector = [int(x in returned_gene_list) for x in input_gene_list]
        
        feature_matrix.append(binary_feature_vector)
    
    feature_matrix = np.array(feature_matrix).transpose()
    return feature_matrix