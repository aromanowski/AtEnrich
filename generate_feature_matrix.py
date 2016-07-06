import pandas as pd
import numpy as np
import re
import sqlite3
from db_connection import db_connection

def generate_feature_matrix(genes_of_interest,feature_list,sql_query="""SELECT locus_id FROM gene_lists WHERE list_name=?;""",database_file="GeneListDB.db"):
    feature_matrix = []
    
    db = db_connection(database_file)
    for feature_name in feature_list:
        query_result = db.query(sql_query,[feature_name])
        feature_hits = [x[0] for x in query_result]
        #features for this list
        binary_feature_vector = [int(x in feature_hits) for x in genes_of_interest]
        feature_matrix.append(binary_feature_vector)
    
    feature_matrix = np.array(feature_matrix).transpose()
    return feature_matrix