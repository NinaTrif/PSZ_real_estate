from enum import Enum


class REGRESSION_SETTINGS(Enum):
    DIRECTORY = '..\\models\\linear_regression'
    COEFF = 'coeff.txt'
    MODEL = 'linear_regression.pickle'
    ENCODER = 'ohe.pickle'
    SCALER = 'scaler.pickle'

class CLASSIFICATION_SETTINGS(Enum):
    DIRECTORY = '..\\models\\knn'
    MODEL = 'knn.pickle'
    ENCODER = 'ohe.pickle'
    SCALER = 'scaler.pickle'

class MODELS(Enum):
    LINEAR_REGRESSION = 'Linear Regression'
    CLASSIFICATION = 'Classification (K Nearest Neighbors)'
