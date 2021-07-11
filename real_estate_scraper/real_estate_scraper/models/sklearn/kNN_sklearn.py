import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from math import sqrt
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler


def round_up_to_odd(f):
    return np.ceil(f) // 2 * 2 + 1


data = pd.read_csv('../../resources/real_estate_pp.csv')
data = data[['district', 'size', 'floor', 'registration', 'rooms', 'parking', 'balcony', 'state', 'price']]

classes = list()
for i, d in data.iterrows():
    if d['price'] <= 49999:
        classes.append('<= 49.999')
    elif d['price'] <= 99999:
        classes.append('50.000 - 99.999')
    elif d['price'] <= 149999:
        classes.append('100.000 - 149.999')
    elif d['price'] <= 199999:
        classes.append('150.000 - 199.999')
    else:
        classes.append('>= 200.000')

data.drop(labels=['price'], axis=1, inplace=True)
data = data.assign(target=classes)

X = np.array(data.iloc[:, 0:-1])
y = np.array(data.iloc[:, -1:])

ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse=False), [0, 7])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

n_neigh = len(X_train)
n_neigh = int(round_up_to_odd(sqrt(n_neigh)))

ct2 = ColumnTransformer([('standard_scaler', StandardScaler(), [-3, -5, -6])], remainder='passthrough')
X_train = ct2.fit_transform(X_train)
X_test = ct2.transform(X_test)

classifier = KNeighborsClassifier(n_neighbors=n_neigh)
classifier.fit(X_train, y_train.ravel())
y_pred = classifier.predict(X_test)

print(classification_report(y_test, y_pred))
