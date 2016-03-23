from sklearn.ensemble import ExtraTreesClassifier

#test input gene list
input_gene_list = ['AT1G09570','AT5G67560', 'AT5G67620', 'AT5G67620']
#dummy classification
y = [0,1,1,0]

#features to rank
gene_list_names = ['chen2014_phyA_chip_seq']

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
xticks(range(X.shape[1]), indices)
xlim([-1, X.shape[1]])
