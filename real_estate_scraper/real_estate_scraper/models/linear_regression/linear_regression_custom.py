import pandas as pd
import importlib
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.sparse import csr_matrix
import pickle
# import sys

linear_regression = importlib.import_module('linear_regression')
data = pd.read_csv('../../resources/real_estate_pp.csv')
data = data[['district', 'size', 'floor', 'registration', 'rooms', 'parking', 'balcony', 'state', 'price']]

X = np.array(data.iloc[:, 0:-1])
y = np.array(data.iloc[:, -1:])

# ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse=False), [0, 4, 8])], remainder='passthrough')
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse=False), [0, 7])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

# scaler = StandardScaler()
# X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X.tolist(), y, test_size=0.2, random_state=0)
X_train = csr_matrix(X_train).toarray()
X_test = csr_matrix(X_test).toarray()

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# np.set_printoptions(threshold=sys.maxsize)
# res = [max(idx) for idx in zip(*X_train)]
# print(res)

# ct2 = ColumnTransformer([('standard_scaler', StandardScaler(), [-3, -5, -6])], remainder='passthrough')
# X_train = ct2.fit_transform(X_train)
# X_test = ct2.transform(X_test)

regressor = linear_regression.LinearRegression(alpha=0.01, n_epoch=300)
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)
np.set_printoptions(precision=2)

print('RMSE: \n', mean_squared_error(y_test, y_pred, squared=False))
print('R2: \n', r2_score(y_test, y_pred))

with open('/models/linear_regression/linear_regression.pickle', 'wb') as out:
    pickle.dump(regressor, out)

with open('/models/linear_regression/ohe.pickle', 'wb') as out:
    pickle.dump(ct, out)

with open('/models/linear_regression/scaler.pickle', 'wb') as out:
    pickle.dump(scaler, out)

with open("/models/linear_regression/coeff.txt", 'w') as output:
    for c in regressor.coeff:
        output.write(str(c) + '\n')
