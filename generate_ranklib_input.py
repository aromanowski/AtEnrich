import numpy as np

def generate_ranklib_input(candidate_reg,eData,cData,fDF,output_filepath):
    '''Generate input for RankLib from expression clustering
    
    Args:
        candidate_reg: List of tuples of the form (gene_id,cluster_id)
        eData: ExpressionData object
        cData: ClusterData object
        fDF: feature enrichment dataframe
            (feature_name,cluster_id) MultiIndex on the columns
            gene_id as the index on the rows
        output_filepath: Location to print output
    
    Returns:
        bool: True if successful.
    

    The function generates a text file in the format:
    
    <line> .=. <target> qid:<qid> <feature>:<value> <feature>:<value> ... <feature>:<value> # <info>
    <target> .=. <float>
    <qid> .=. <positive integer>
    <feature> .=. <positive integer>
    <value> .=. <float>
    <info> .=. <string>
    The target value and each of the feature/value pairs are separated by a space character. Feature/value pairs MUST be ordered by increasing feature number. Features with value zero can be skipped. The target value defines the order of the examples for each query. Implicitly, the target values are used to generated pairwise preference constraints as described in [Joachims, 2002c]. A preference constraint is included for all pairs of examples in the example_file, for which the target value differs. The special feature "qid" can be used to restrict the generation of constraints. Two examples are considered for a pairwise preference constraint only if the value of "qid" is the same. For example, given the example_file
    
    3 qid:1 1:1 2:1 3:0 4:0.2 5:0 # 1A
    2 qid:1 1:0 2:0 3:1 4:0.1 5:1 # 1B 
    1 qid:1 1:0 2:1 3:0 4:0.4 5:0 # 1C
    1 qid:1 1:0 2:0 3:1 4:0.3 5:0 # 1D  
    1 qid:2 1:0 2:0 3:1 4:0.2 5:0 # 2A  
    2 qid:2 1:1 2:0 3:1 4:0.4 5:0 # 2B 
    1 qid:2 1:0 2:0 3:1 4:0.1 5:0 # 2C 
    1 qid:2 1:0 2:0 3:1 4:0.2 5:0 # 2D  
    2 qid:3 1:0 2:0 3:1 4:0.1 5:1 # 3A 
    3 qid:3 1:1 2:1 3:0 4:0.3 5:0 # 3B 
    4 qid:3 1:1 2:0 3:0 4:0.4 5:1 # 3C 
    1 qid:3 1:0 2:1 3:1 4:0.5 5:0 # 3D
    
    For our purposes, qid should be equal for all entries (we allow comparisons
    between any pair of regulation candidates).'''
    
    #For each pair, calculate the abs(mean_similarity) coefficient for expression
    # (if not possible, set to zero).
    with open(output_filepath,'w') as f:
        feature_list = fDF.columns.levels[0]
        for reg in candidate_reg:
            regulator_id,cluster_idx = reg
            try:
                similarity = abs(eData.mean_similarity(regulator_id,cData['cluster_gene_lists'][cluster_idx]))
                if np.isnan(similarity):
                    similarity = 0.0
            except KeyError:
                similarity = 0.0
            feature_data = [fDF.loc[regulator_id,(x,cluster_idx)] for x in feature_list]
            #Get into the right format
            feature_data_string = [str(x+1)+':'+str(y) for x,y in enumerate(feature_data)]
            f.write(' '.join([str(similarity),'qid:1']+feature_data_string)+'\n')
    return True