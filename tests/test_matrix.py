import pytest
import corrmat


def test_non_unity_diagonal_breaks(default_rand_mat):
    df = default_rand_mat.corr()
    df.iloc[0, 0] = 0.9

    with pytest.raises(ValueError):
        corrmat.CorrelationMatrix(df)


def test_non_symmetric_breaks(default_rand_mat):
    df = default_rand_mat.corr()
    df.iloc[0, 1] += 1

    with pytest.raises(ValueError):
        corrmat.CorrelationMatrix(df)


def test_large_values_breaks(default_rand_mat):
    df = default_rand_mat.corr()
    df.iloc[0, 1] = 2

    with pytest.raises(ValueError):
        corrmat.CorrelationMatrix(df)


def test_get_submatrix(default_corr_mat):
    cm = default_corr_mat

    sm = cm.get_submatrix('A', threshold=0.8)
    assert sm.matrix.equals(default_corr_mat.matrix[['A','D','B']].loc[['A','D','B']])
