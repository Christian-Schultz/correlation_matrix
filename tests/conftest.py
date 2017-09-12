import pytest
import numpy as np
import pandas as pd

@pytest.fixture(scope="function")
def default_corrmat():
    np.random.seed(0)
    return pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list('ABCD')).corr()