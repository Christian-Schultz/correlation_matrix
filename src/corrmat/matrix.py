import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import EllipseCollection


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
        # Check if values on diagonal are 1
        if not (np.diag(dataframe.values) == 1).all():
            raise ValueError("Diagonal is not unity")

        self._rows = dataframe.index.tolist()
        self._columns = dataframe.columns.tolist()
        #Check if matrix is square
        if len(self._rows) != len(self._columns):
            raise ValueError("Matrix specified is not square")
        # Check if matrix is symmetric
        if not (dataframe.equals(dataframe.transpose())):
            raise ValueError("Matrix not symmetric")
        # Check if columns and rows are named similarly
        if self._rows != self._columns:
            raise IndexError("Columns and rows need to have identical labels")

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

    def get_submatrix(self, target, threshold=0.75, skip_negatives=False, sort=True):
        """
        This method will produce a sub-matrix with all variables that have a correlation coefficient larger than a
        specified threshold for the given target. The sub-matrix is sorted descendingly with respect to the
        correlation coefficients by default.

        :param target: The target (row or column name) to identify the correlation coefficients
        :param threshold: The specified threshold. Default: 0.75
        :param skip_negatives: If true, will skip variables that have a negative correlation smaller than the specified
        threshold. Default: False
        :param sort: Sort descendingly by correlation coeffients. Default: True
        :return: Returns new CorrelationMatrix instance
        """

        if threshold < 0:
            raise ValueError("Threshold must be non-negative")

        if sort:
            mat = self.matrix[target].sort_values(ascending=False)
        else:
            mat = self.matrix[target]

        idx = mat >= threshold

        idx2 = mat <= -threshold
        idx |= idx2

        idx = idx.index[idx].tolist()

        m = self.matrix[idx].loc[idx]

        # Use __class__ to use CorrelationMatrix constructor and not a subclass' (if the class inherits from
        # CorrelationMatrix)
        return self.__class__.from_dataframe(m, calculate=False)

    def ellipse_plot(self, ax=None, **kwargs):
        """
        Make an ellipse plot of the correlation matrix. Return the figure instance. Code modified from
        https://stackoverflow.com/a/34558488/787267

        :param ax: If specified, will plot in this axes instance, otherwise will create a new figure instance
        :param kwargs: Key word arguments to be passed to matplotlib.collections.EllipseCollection. The default clim is
        [-1,1], use clim=None if the color scaling is to be set automatically
        :return: A matplotlotlib.pyplot.figure instance
        """

        M = self.matrix.values
        if ax is None:
            fig, ax = plt.subplots(1, 1, subplot_kw={'aspect': 'equal'})
            ax.set_xlim(-0.5, M.shape[1] - 0.5)
            ax.set_ylim(-0.5, M.shape[0] - 0.5)

        # xy locations of each ellipse center
        xy = np.indices(M.shape).reshape(2, -1).T

        # set the relative sizes of the major/minor axes according to the strength of
        # the positive/negative correlation
        w = np.ones_like(M).ravel()
        h = 1 - np.abs(M).ravel()
        # Fix diagonal entries to be straight lines
        h = [0.01 if e == 0 else e for e in h]
        a = 45 * np.sign(M).ravel()

        kwargs.setdefault('cmap', 'bwr_r')
        kwargs.setdefault('clim', [-1, 1])

        ec = EllipseCollection(widths=w, heights=h, angles=a, units='x', offsets=xy,
                               transOffset=ax.transData, array=M.ravel(), **kwargs)
        ax.add_collection(ec)

        for x,y in xy:
            ax.annotate("%.1f" % M[x,y],xy=(x,y), va='center', ha='center')

        ax.set_xticks(np.arange(self.matrix.shape[1]))
        ax.set_xticklabels(self.columns)
        ax.set_yticks(np.arange(self.matrix.shape[0]))
        ax.set_yticklabels(self.rows)

        ax.invert_yaxis()
        ax.xaxis.tick_top()
        return ec.figure
