import pandas as pd
import re
import MySQLdb

db = MySQLdb.connect("localhost","root","zoomzoom","GeneListDB")
cursor = db.cursor()

#input gene list
input_gene_list = ['AT1G09570','AT5G67560', 'AT5G67620', 'AT5G67620']

feature_matrix = []

#annotate these according to presence/absence in gene lists
gene_list_names = ['phyA_chip_seq']

gene_list_name = gene_list_names[0]
cursor.execute("""SELECT list_id FROM list_info WHERE list_name=%s;""",[gene_list_name])
result = cursor.fetchall()
assert(len(result[0])==1)
gene_list_id = result[0][0]

sql_query = """SELECT locus_id FROM gene_lists WHERE list_id=2;"""
cursor.execute(sql_query)
result = cursor.fetchall()
returned_gene_list = [x[0] for x in result]

#features for this list
binary_feature_vector = [int(x in returned_gene_list) for x in input_gene_list]

feature_matrix.append(binary_feature_vector)




feature_matrix = np.array(feature_matrix)