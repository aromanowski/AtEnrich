import json

class ClusterData:
    """A cluster object.
    
    >>> import os.path, inspect
    >>> main_dir = os.path.dirname(inspect.getfile(ClusterData))
    >>> data_dir = os.path.join(main_dir,'tests','test_data_files')
    >>> 
    >>> clustering_file_location = os.path.join(data_dir,'diurnal_clustering_300916.json')
    >>> 
    >>> cData = ClusterData.from_json(clustering_file_location)
    >>> 
    >>> cData.get_cluster_label('AT3G51240')
    85
    >>> cData.get_cluster_label('AT1G09570')
    6
    """
    
    _required_keys = [u'datasets',
    u'description',
    u'labels',
    u'cluster_gene_lists',
    u'cluster_method',
    u'cluster_centers',
    u'cluster_parameters',
    u'gene_list',
    u'label_set',
    u'cluster_gene_lists']
    
    def __init__(self,data=None):
        if data is None:
            keys = ClusterData._required_keys
            self.data = dict([x,None] for x in keys)
        else:
            if not all([x in data for x in ClusterData._required_keys]):
                raise ValueError('Not all of the required keys are contained in the input data dictionary')
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
    
    def to_file(self,filename,sep='\t'):
        '''Print list of gene names and cluster labels to a file.'''
        with open(filename,'w') as f:
            f.write(sep.join(['locus_id','cluster_label'])+'\n')
            for x,y in zip(self['gene_list'],self['labels']):
                f.write(sep.join([x,str(y)])+'\n')            
                

if __name__ == "__main__":
    import doctest
    doctest.testmod()