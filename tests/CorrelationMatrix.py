import sys
import pandas as pd
import numpy as np
sys.path.append('../src')

from src.matrix import CorrelationMatrix

df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

corr_mat = CorrelationMatrix(df, calculate=True)


sm = corr_mat.get_submatrix('A', threshold=0.05)

print sm

print "Done"