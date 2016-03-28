from sklearn.ensemble import ExtraTreesClassifier
import numpy as np
import random
from connect_to_db import connect_to_db
from generate_feature_matrix import generate_feature_matrix

db = connect_to_db()
cursor = db.cursor()

#test input gene list
#get all locus_ids appearing in gene_lists
cursor.execute("""SELECT locus_id FROM gene_lists;""")
input_gene_list = [x[0] for x in cursor.fetchall()]
#select subsample of list
nGenes = 1500
random.seed(0)
input_gene_list = random.sample(input_gene_list,nGenes)
#dummy classification
list_name = 'hornitschek2012_PIF5_chip_seq'
cursor.execute("""SELECT locus_id FROM gene_lists WHERE list_name=%s;""",[list_name])
positive_classification_list = [x[0] for x in cursor.fetchall()]
y = [int(x in positive_classification_list) for x in input_gene_list]

#get list of all other gene lists to rank
cursor.execute("""SELECT list_name FROM list_info WHERE list_name!=%s;""",[list_name])
gene_list_names = [x[0] for x in cursor.fetchall()]

X = generate_feature_matrix(input_gene_list,gene_list_names)

forest = ExtraTreesClassifier(n_estimators=350,
                              random_state=0)

forest.fit(X,y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]


# Print the feature ranking
print("Feature ranking:")

for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
figure()
title("Feature importances")
bar(range(X.shape[1]), importances[indices],
    color="r", yerr=std[indices], align="center")
xticks(range(X.shape[1]), [gene_list_names[x] for x in indices],rotation=90)
xlim([-1, X.shape[1]])
tight_layout()

db.close()