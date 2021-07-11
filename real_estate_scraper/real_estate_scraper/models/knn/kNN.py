from math import sqrt
import numpy as np


class KNearestNeighbors(object):
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
            self.f = self.euclidean_distance
        else:
            self.f = self.manhattan_distance

    def fit(self, X, y):
        """
        Model fitting based on provided training set.

        :param X: train set feature vectors
        :param y: train set outputs
        :return: /
        """

        self.X = X
        self.y = y

        self.rows, self.columns = X.shape

        if self.k == 0:
            self.k = int(sqrt(np.ceil(self.rows) // 2 * 2 + 1))

    def predict(self, X):
        """
        Makes output class prediction.

        :param X: array of feature vectors
        :return: list of predictions for each feature vector in X
        """

        predictions = list()
        for row in X:
            distances = self.calculate_distances(row, self.f)
            neighbors = self.get_neighbors(distances)
            y_pred = self.make_prediction(neighbors)
            predictions.append(y_pred)
        return predictions

    def calculate_distances(self, v, f):
        """
        Calculates distances between given row and each vector in X.

        :param v: feature vector
        :param f: distance function
        :return: list of distances
        """

        distances = list()
        for i in range(self.rows):
            distances.append((self.y[i], f(self.X[i], v)))
        return distances

    def euclidean_distance(self, v1, v2):
        """
        Calculates Euclidean distance between two vectors.

        :param v1: first feature vector
        :param v2: second feature vector
        :return: distance between v1 and v2
        """

        distance = 0.0
        for i in range(len(v1)):
            distance += (v1[i] - v2[i]) ** 2
        return sqrt(distance)

    def manhattan_distance(self, v1, v2):
        """
        Calculates Manhattan distance between two vectors.

        :param v1: first feature vector
        :param v2: second feature vector
        :return: distance between v1 and v2
        """

        distance = 0.0
        for i in range(len(v1)):
            distance += abs(v1[i] - v2[i])
        return distance

    def get_neighbors(self, distances):
        """
        Finds k nearest neighbors based on given distances.

        :param distances: array of distances for current input from each feature vector in train set
        :return: k nearest neighbors
        """

        distances.sort(key=lambda tup: tup[1])
        neighbors = list()
        for i in range(self.k):
            neighbors.append(distances[i][0])
        return neighbors

    def make_prediction(self, neighbors):
        """
        Predicts the output class.

        :param neighbors: k nearest neighbors
        :return: output class based on majority voting
        """

        # predicted_classes = [row[-1] for row in neighbors]
        prediction = max(set(neighbors), key=neighbors.count)
        return prediction
