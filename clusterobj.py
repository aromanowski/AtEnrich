import json

class ClusterObj:
    """A cluster object."""
    
    def __init__(self,data=None):
        if data is None:
            keys = [u'datasets',
            u'description',
            u'labels',
            'cluster_gene_lists',
            u'cluster_method',
            u'cluster_centers',
            u'cluster_parameters',
            u'gene_list',
            u'label_set',
            u'cluster_gene_lists']
            self.data = dict([x,[]] for x in keys)
        else:
            self.data = data

    @classmethod
    def from_json(cls,clustering_file_location):
        with open(clustering_file_location) as data_file:
            data = json.load(data_file)
        
        data['label_set'] = sorted(list(set(data['labels'])))
        data['cluster_gene_lists'] = dict([(x,[]) for x in data['label_set']])
        for label,gene_name in zip(data['labels'],data['gene_list']):
            data['cluster_gene_lists'][label].append(gene_name)
        
        cluster_obj = cls(data)
        return cluster_obj
    
    def __getitem__(self,key):
        return self.data[key]
        
    def get_cluster_label(self,gene_name):
        idx = self['gene_list'].index(gene_name)
        return self['labels'][idx]