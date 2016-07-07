import pandas as pd
import numpy as np

def generate_feature_matrix(genes_of_interest,feature_list,db_cursor,sql_query="""SELECT locus_id FROM gene_lists WHERE list_name=?;"""):
    feature_matrix = []
    
    for feature_name in feature_list:
        returned_gene_list = query_database(sql_query,feature_name,db_cursor)
        #features for this list
        binary_feature_vector = [int(x in returned_gene_list) for x in genes_of_interest]
        feature_matrix.append(binary_feature_vector)
    
    feature_matrix = np.array(feature_matrix).transpose()
    return feature_matrix


def query_database(sql_query,list_name,db_cursor):
    db_cursor.execute(sql_query,[list_name])
    result = db_cursor.fetchall()
    returned_gene_list = [x[0] for x in result]
    return returned_gene_list