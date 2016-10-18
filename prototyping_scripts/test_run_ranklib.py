import pandas as pd
import numpy as np

"java -jar ~/Programs/RankLib/RankLib-2.1-patched.jar -train ranklib_test_input.txt -test ranklib_test_input.txt -ranker 2 -save mymodel.txt"

"java -jar ~/Programs/RankLib/RankLib-2.1-patched.jar -load mymodel.txt -rank ranklib_test_input.txt -score myscorefile.txt"


#TODO add column labels
inDF = pd.read_csv('test_data_files/ranklib_test_input.txt',sep=' ',header=None)
outDF = pd.read_csv('test_data_files/myscorefile.txt',sep='\t',header=None)

sort_prediction = sorted(range(1111),key = lambda x: outDF.loc[x,2])

corr_ordering = inDF.loc[sort_prediction,0]

N = 30
print np.mean(abs(corr_ordering[-N:]))
print np.mean(abs(corr_ordering))

#windowN = 40
#moving_average = np.convolve(corr_ordering, np.ones((windowN,))/windowN, mode='valid')
#
#plot(moving_average,'-o')