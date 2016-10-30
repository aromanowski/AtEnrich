import scipy.stats
import numpy as np

class ExpressionData:
    """A set of expression dataframes.
    
    Attributes:
        data_dict: A dictionary containing expression dataframes (eDFs).
        sim_fcn: A function that calculates gene-gene similarities for individual eDFs.
        weight_dict: A dictionary of weights for summing similarities.
        
        _using_default_weights: Boolean indicating whether weights have been user-specified.
    
    Methods:
        similarity(gene1,gene2): Calculate similarity between gene1 and gene2
        mean_similarity(gene1,gene_list): Mean similarity between gene1 and gene_list
    
        _set_default_weights
        _normalise_weights
    """

    def __init__(self,data_dict=dict(),sim_fcn=lambda x,y: scipy.stats.pearsonr(x,y)[0],weight_dict=None):
        self.data_dict = data_dict
        self.sim_fcn = sim_fcn
        if weight_dict is None:
            #Default to equal weighting
            self._set_default_weights()
        else:
            #Normalise input weights
            self._normalise_weights()
            self._using_default_weights = False
        
        assert(all([x>=0 for x in self.weight_dict.values()]))
    
    def _set_default_weights(self):
        """Set default weights (i.e. equal for all eDFs)"""
        self.weight_dict = dict([(x,1.0) for x in self.data_dict.keys()])
        self._normalise_weights()
        self._using_default_weights = True

    def _normalise_weights(self):
        """Normalise weights to sum to 1"""
        norm_factor = float(len(self.weight_dict))
        for key in self.weight_dict.keys():
            self.weight_dict[key] = self.weight_dict[key]/norm_factor
        
    def __getitem__(self, key):
        return self.data_dict[key]
    
    def __setitem__(self, key, item):
        self.data_dict[key] = item
        #New dataset being added - reset weights to default
        self._set_default_weights()
    
    def similarity(self,gene1,gene2):
        """Calculate similarity between gene1 and gene2"""
        sim = 0.0
        for key in self.data_dict.keys():
            w = self.weight_dict[key]
            sim += w*self.sim_fcn(self.data_dict[key].loc[gene1,:],self.data_dict[key].loc[gene2,:])
        return sim
    
    def mean_similarity(self,gene1,gene_list):
        """Calculate mean similarity between gene1 and gene_list"""
        similarities = []
        for gene2 in gene_list:
            similarities.append(self.similarity(gene1,gene2))
        return np.mean(similarities)
    
    def similar_genes(self,gene1,threshold):
        """Return a list of transcripts with similarity > threshold to a given transcript (gene1)."""
        assert(threshold>=-1)
        assert(threshold<=1)
        return [x for x in self.gene_list if self.mean_similarity(gene1,x)>=threshold]            