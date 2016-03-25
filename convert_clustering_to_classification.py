import pandas as pd
import numpy as np
import random

random.seed(0)
input_cluster_labels = [0,1,2]
#input clusters
nG = 8
cluster_list = [random.choice(input_cluster_labels) for _ in range(nG)]

cluster_labels = sorted(list(set(cluster_list)))

def convert_clustering_to_classification(cluster_list):
    cluster_labels = sorted(list(set(cluster_list)))
    binary_classification = [ [int(x==label) for x in cluster_list] for label in cluster_labels]
    return np.array(binary_classification)
    

print cluster_list
print convert_clustering_to_classification(cluster_list)