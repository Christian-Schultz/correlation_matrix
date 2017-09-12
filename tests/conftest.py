import pytest
import numpy as np
import pandas as pd
import corrmat

@pytest.fixture(scope="function")
def default_rand_mat():
    np.random.seed(0)
    return pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list('ABCD'))


@pytest.fixture(scope="function")
def default_corr_mat():
    values = np.array([[1, -0.9, 0.5, 0.8], [-0.9, 1, 0.6, 0.4], [0.5, 0.6, 1, -0.4], [0.8, 0.4, -0.4, 1]])
    df = pd.DataFrame(values, columns=list('ABCD'), index=list('ABCD'))
    return corrmat.CorrelationMatrix(df)