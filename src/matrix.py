import pandas as pd
import numpy as np


class CorrelationMatrix(object):

    def __init__(self, matrix=None, calculate=False):

        self._rows = None
        self._columns = None
        if calculate:
            matrix = matrix.corr()

        self.matrix = matrix

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, dataframe):
        if (abs(dataframe) > 1).any().any():
            raise ValueError("Not a valid correlation matrix. Correlation coefficients needs to be less than 1")
        self._rows = dataframe.index.tolist()
        self._columns = dataframe.columns.tolist()
        self._matrix = dataframe

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, val):
        raise ValueError('Property cannot be set')

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, val):
        raise ValueError('Property cannot be set')

    def get_submatrix(self, target, threshold=0.75):

        idx = self.matrix[target].sort_values(ascending=False) >= threshold

        idx = idx.index[idx == True].tolist()

        m = self.matrix[idx].loc[idx]

        return m
