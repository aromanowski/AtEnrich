import json

class ClusterObj:
    """A cluster object."""
    
    def __init__(self,data=None):
        if data is None:
            keys = [u'datasets',
            u'description',
            u'labels',
            u'cluster_gene_lists',
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
        
        cData = cls(data)
        return cData
    
    @classmethod
    def from_txt(cls,clustering_file_location,sep='\t',header=False):
        if header:
            offset = 1
        else:
            offset = 0
        
        with open(clustering_file_location) as data_file:
            gene_label_pairs = [x.strip().split(sep) for x in data_file.readlines()[offset:]]
        
        data = dict()
        data['gene_list'] = [x[0] for x in gene_label_pairs]
        data['labels'] = [x[1] for x in gene_label_pairs]
        cData = cls(data)
        return cData
    
    def __getitem__(self,key):
        return self.data[key]
        
    def get_cluster_label(self,gene_name):
        idx = self['gene_list'].index(gene_name)
        return self['labels'][idx]
    
    def keys(self):
        return self.data.keys()