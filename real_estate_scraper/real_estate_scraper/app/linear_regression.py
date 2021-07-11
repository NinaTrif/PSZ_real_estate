import numpy as np
from sklearn.metrics import mean_squared_error


class LinearRegression(object):
    """
    Represents multiple linear regression implementation.
    """

    def __init__(self, alpha=0.01, n_epoch=100):
        """
        Model parameter initialization.

        :param alpha: learning rate
        :param n_epoch: number of iterations
        """

        self.alpha = alpha
        self.n_epoch = n_epoch

        # rmse represents an array of Root Mean Square Error values (for each of the iterations)
        self.rmse = []

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

        # initialize coefficients to zero
        self.coeff = np.zeros(self.columns + 1)

        self.train()

    def train(self):
        """
        Model training -> iterative coefficient calculation

        :return: /
        """

        for i in range(self.n_epoch):
            y_pred = self.predict(self.X)
            self.update_coeff(y_pred)
            _rmse = mean_squared_error(self.y, y_pred, squared=False)
            self.rmse.append(_rmse)
            print(f'Iteration {i}, error: {_rmse}')

    def predict(self, X):
        """
        Makes output prediction (hypothesis) based on current coefficients.

        :param X: array of feature vectors
        :return: list of predictions for each feature vector in X
        """

        predictions = list()
        for row in X:
            y_pred = self.calc_hypothesis(row)
            predictions.append(y_pred)
        return predictions

    def update_coeff(self, y_pred):
        """
        Updates model coefficients based on predicted and expected outputs.
        Uses stochastic batch gradient descent.

        :param y_pred: predicted outputs
        :return: /
        """

        gradient = np.zeros(len(self.coeff))
        for i in range(len(self.coeff)):
            for j in range(self.rows):
                if i == 0:
                    gradient[i] = gradient[i] + (y_pred[j] - self.y[j])
                else:
                    gradient[i] = gradient[i] + (y_pred[j] - self.y[j]) * self.X[j][i - 1]
        gradient = gradient / self.rows

        self.coeff = self.coeff - self.alpha * gradient

    def root_mean_squared_error(self, y, y_pred):
        """
        Calculates Root Mean Squared Error for given expected and predicted outputs.

        :param y: expected outputs
        :param y_pred: predicted outputs
        :return: root mean squared error
        """

        # return np.sqrt(np.average((y - y_pred) ** 2))

        _rmse = 0.0
        for i in range(len(y_pred)):
            error = y[i] - y_pred[i]
            error *= error
            _rmse += error
        _rmse /= len(y_pred)
        return np.sqrt(_rmse)

    def calc_hypothesis(self, x):
        """
        Calculates hypothesis (predicted output) for the given feature vector, using current coefficients.

        :param x: input vector
        :return: hypothesis value
        """

        h = self.coeff[0]
        for i in range(len(x)):
            h = h + x[i] * self.coeff[i + 1]
        return h
