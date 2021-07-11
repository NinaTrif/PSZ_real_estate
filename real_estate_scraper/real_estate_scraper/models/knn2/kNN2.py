from math import sqrt
import numpy as np
import scipy


class kNN(object):
    """
    Custom k nearest neighbors classifier.
    """

    def __init__(self, k=0, f=0):
        """
        Model parameter initialization.

        :param k: number of neighbors
        :param f: distance function (0 -> Euclidean, 1 -> Manhattan)
        """

        self.k = k
        if f == 0:
            self.f = 'euclidean'
        else:
            self.f = 'hamming'

    def fit(self, X, y):
        """
        Model fitting based on provided training set.

        :param X: train set feature vectors
        :param y: train set outputs
        :return: /
        """

        self.X = X
        self.rows, self.columns = X.shape
        self.classes_, self.y = scipy.unique(y, return_inverse=True)

        if self.k == 0:
            self.k = int(sqrt(np.ceil(self.rows) // 2 * 2 + 1))

    def predict(self, X):
        """
        Makes output class prediction.

        :param X: array of feature vectors
        :return: list of predictions for each feature vector in X
        """

        dist_mat = scipy.spatial.distance.cdist(X, self.X, metric=self.f)
        neighbors_ind = scipy.argsort(dist_mat, axis=1)[:, : self.k]
        neighbors = scipy.stats.mode(self.y[neighbors_ind], axis=1)[0].flatten()
        y_pred = self.classes_[neighbors]
        return y_pred
