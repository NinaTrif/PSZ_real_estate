import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

data = pd.read_csv('../../resources/real_estate_pp.csv')
# data = data[['district', 'size', 'floor', 'registration', 'heating', 'rooms', 'parking', 'balcony', 'state', 'price']]
data = data[['district', 'size', 'floor', 'registration', 'rooms', 'parking', 'balcony', 'state', 'price']]

X = np.array(data.iloc[:, 0:-1])
y = np.array(data.iloc[:, -1:])

# ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0, 4, 8])], remainder='passthrough')
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [0, 7])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

X_train, X_test, y_train, y_test = train_test_split(X.tolist(), y, test_size=0.2, random_state=0)

# scaler = StandardScaler(with_mean=False)
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

print('RMSE: \n', mean_squared_error(y_test, y_pred, squared=False))
print('R2: \n', r2_score(y_test, y_pred))
