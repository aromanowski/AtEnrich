def generate_ranklib_input(candidate_reg,exp_data,feature_data):
    '''Generate input for RankLib from expression clustering
    
    
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
    
    #1. For each pair, calculate the similarity coefficient for expression
    #   (if not possible, set to zero)
    
    #2. Output (to file?)