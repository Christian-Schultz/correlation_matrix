class CorrelationMatrix(object):
    """A thin wrapper on a pandas dataframe representing a correlation matrix

    This class is a thin wrapper on top of a pandas dataframe that provides some additional methods that are often
    convenient for a correlation matrix such as plotting and extracting sub-matrices.

    """
    def __init__(self, matrix=None, calculate=False):
        """Create a CorrelationMatrix instance. This object can be constructed from a pandas dataframe, as an empty
        matrix to be filled later, or as a raw dataframe on which the correlation matrix will be calculated.

        If a pandas dataframe is passed with calculate=False then it will implicitly be assumed that the dataframe is
        already a square correlation matrix. If calculate=True then the dataframe's correlation matrix will be
        calculated by the pandas corr method.

        :param matrix: The pandas dataframe that corresponds to the correlation matrix. If not specified the
        CorrelationMatrix instance will be empty.
        :param calculate: A boolean parameter that if true will calculate
        matrix.corr() and set this as the underlying correlation matrix. Defaults to False.
        """

        self._rows = None
        self._columns = None
        self._matrix = None
        if calculate:
            matrix = matrix.corr()

        self.matrix = matrix

    def __repr__(self):
        #  if cm is a correlation matrix eval(repr(cm)) does not reproduce an identical instance like it should. It is
        #  implemented here to enable a convenient representation - just like a pandas dataframe (which also violates
        #  the eval->repr rule, and hence it is not possible for this class to adhere to the rule).
        return repr(self.matrix)

    @classmethod
    def from_dataframe(cls, matrix=None, calculate=False):
        """Default constructor

        :param matrix: The pandas dataframe that corresponds to the correlation matrix. If not specified the
        CorrelationMatrix instance will be empty.
        :param calculate: A boolean parameter that if true will calculate
        matrix.corr() and set this as the underlying correlation matrix. Defaults to False.
        """
        return cls(matrix, calculate)

    @property
    def matrix(self):
        """
        The uncderlying pandas dataframe containing the correlation matrix. If set assumes a square matrix with
        entries in the range -1 <= e <= 1
        """
        return self._matrix

    @matrix.setter
    def matrix(self, dataframe):
        """
        Property that sets the underlying pandas dataframe
        :param dataframe: Dataframe to set. Should be symmetric with all coefficients in the range [-1,1]
        :return: None
        """
        # Check if coefficients are in range [-1,1]
        if (abs(dataframe) > 1).any().any():
            raise ValueError("Not a valid correlation matrix. Correlation coefficients needs to be less than or equal "
                             "to 1 (numerically)")
        self._rows = dataframe.index.tolist()
        self._columns = dataframe.columns.tolist()
        if len(self._rows) != len(self._columns):
            raise ValueError("Matrix specified is not square")
        if not dataframe.equals(dataframe.transpose()):
            raise ValueError("Matrix not symmetric")
        self._matrix = dataframe

    @property
    def columns(self):
        """
        Property that contains the columns of correlation matrix. Cannot be set
        :return: The columns of the underlying pandas dataframe as a list
        """
        return self._columns

    @columns.setter
    def columns(self, val):
        raise ValueError('Property cannot be set')

    @property
    def rows(self):
        """
        Property that contains the rows of correlation matrix. Cannot be set
        :return: The index of the underlying pandas dataframe as a list
        """
        return self._rows

    @rows.setter
    def rows(self, val):
        raise ValueError('Property cannot be set')

    def get_submatrix(self, target, threshold=0.75):
        """
        This method will produce a sub-matrix with all variables that have a correlation coefficient larger (in
        numerical terms) than a specified threshold for the given target. The sub-matrix is sorted descendingly with
        respect to the correlation coefficients.

        :param target: The target (row or column name) to identify the correlation coefficients
        :param threshold: The specified threshold. Default: 0.75
        :return: Returns new CorrelationMatrix instance
        """

        idx = self.matrix[target].sort_values(ascending=False) >= threshold

        idx = idx.index[idx].tolist()

        m = self.matrix[idx].loc[idx]

        return self.from_dataframe(m, calculate=False)
