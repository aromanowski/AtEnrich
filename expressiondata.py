import scipy.stats
import numpy as np
import pandas as pd

class ExpressionData:
    """A set of expression dataframes.
    
    Attributes:
        sim_fcn: A function that calculates gene-gene similarities for individual eDFs.
        weight_dict: A dictionary of weights for summing similarities.
        similarity_matrix: A dataframe of all gene-gene similarities.
        
        _data_dict: A dictionary containing expression dataframes (eDFs).
        _using_default_weights: Boolean indicating whether weights have been user-specified.
    
    Methods:
        similarity(gene1,gene2): Calculate similarity between gene1 and gene2
        mean_similarity(gene1,gene_list): Mean similarity between gene1 and gene_list
        similar_genes(gene1,threshold): Return a list of transcripts with similarity > threshold to a given transcript (gene1).
        select_gene_subset(gene_subset): Only keep data for a subset of genes.
        generate_similarity_matrix(): Generate similarity matrix for all gene-gene pairs.

        _set_gene_list
        _set_default_weights
        _normalise_weights
    """

    def __init__(self,data_dict,sim_fcn=lambda x,y: scipy.stats.pearsonr(x,y)[0],weight_dict=None):
        self._data_dict = data_dict
        self.sim_fcn = sim_fcn
        self.similarity_matrix = None
        self._similarity_matrix_generated = False
        self._set_gene_list()
        if weight_dict is None:
            #Default to equal weighting
            self._set_default_weights()
        else:
            #Normalise input weights
            self.weight_dict = weight_dict
            self._normalise_weights()
            self._using_default_weights = False
        
        assert(all([x>=0 for x in self.weight_dict.values()]))

    def __getitem__(self, key):
        return self.data_dict[key]


    def _set_default_weights(self):
        """Set default weights (i.e. equal for all eDFs)"""
        self.weight_dict = dict([(x,1.0) for x in self._data_dict.keys()])
        self._normalise_weights()
        self._using_default_weights = True

    def _normalise_weights(self):
        """Normalise weights to sum to 1"""
        norm_factor = float(len(self.weight_dict))
        for key in self.weight_dict.keys():
            self.weight_dict[key] = self.weight_dict[key]/norm_factor
    
    def _set_gene_list(self):
        """Identify valid gene ids, found in all contained datasets."""
        if len(self._data_dict)>0:
            self.gene_list = list(set.intersection(*[set(eDF.index) for eDF in self._data_dict.values()]))
        else:
            self.gene_list = []




    
    def similarity(self,gene1,gene2):
        """Calculate similarity between gene1 and gene2"""
        if self._similarity_matrix_generated:
            return self.similarity_matrix.loc[gene1,gene2]
        else:
            sim = 0.0
            for key in self._data_dict.keys():
                w = self.weight_dict[key]
                sim += w*self.sim_fcn(self._data_dict[key].loc[gene1,:],self._data_dict[key].loc[gene2,:])
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
        return [x for x in self.gene_list if self.similarity(gene1,x)>=threshold]
    
    def generate_similarity_matrix(self):
        self.similarity_matrix = pd.DataFrame(index=self.gene_list,columns=self.gene_list)
        for idx,g1 in enumerate(self.gene_list):
            for g2 in self.gene_list[idx:]:
                sim = self.similarity(g1,g2)
                self.similarity_matrix.loc[g1,g2] = sim
                self.similarity_matrix.loc[g2,g1] = sim
        self._similarity_matrix_generated = True
                
    def select_gene_subset(self,gene_subset):
        """Only keep data for a subset of genes."""
        gene_subset = list(set(gene_subset)&set(self.gene_list))
        for key in self._data_dict.keys():
            self._data_dict[key] = self._data_dict[key].loc[gene_subset,:]
        self.gene_list = gene_subset