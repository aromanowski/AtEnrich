import json
import clusterobj

class ClusterObj:
    """A cluster object."""
    
    def __init__(self,clustering_file_location):
        with open(clustering_file_location) as data_file:
            self.data = json.load(data_file)
        
        self.data['label_set'] = sorted(list(set(self['labels'])))
        self.data['cluster_gene_lists'] = dict([(x,[]) for x in self['label_set']])
        for label,gene_name in zip(self['labels'],self['gene_list']):
            self.data['cluster_gene_lists'][label].append(gene_name)
    
    def __getitem__(self,key):
        return self.data[key]
    
    def get_cluster_label(self,gene_name):
        idx = self['gene_list'].index(gene_name)
        return self['labels'][idx]