import sys
import os

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

sys.path.insert(0, os.path.abspath('../src/'))

from corrmat import CorrelationMatrix

df1 = pd.DataFrame(np.random.randint(0,100,size=(100, 10)), columns=[chr(a) for a in range(65, 75)])

values = np.array([[1, -0.9, 0.5, 0.8], [-0.9, 1, 0.6, 0.4], [0.5, 0.6, 1, -0.4], [0.8, 0.4, -0.4, 1]])
df2 = pd.DataFrame(values, columns=list('ABCD'), index=list('ABCD'))

corr_mat1 = CorrelationMatrix(df1, calculate=True)

corr_mat2 = CorrelationMatrix(df2, calculate=False)

corr_mat2 = corr_mat2.get_submatrix('A', threshold=0.5, sort=True)

fig1 = corr_mat1.plot(annot=False, shape='tril')

fig2, ax2 = plt.subplots(1, 1)
corr_mat2.plot(cmap='RdGy', ax=ax2)

plt.show()
print "Done"