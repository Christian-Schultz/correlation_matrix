import pytest
import corrmat


def test_non_symmetric_breaks(default_corrmat):
    default_corrmat.iloc[0, 1] += 1

    with pytest.raises(ValueError):
        corrmat.CorrelationMatrix(default_corrmat)

def test_large_values_breaks(default_corrmat):
    default_corrmat.iloc[0, 1] = 2

    with pytest.raises(ValueError):
        corrmat.CorrelationMatrix(default_corrmat)
