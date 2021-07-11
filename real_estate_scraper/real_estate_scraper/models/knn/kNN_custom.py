import importlib
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pickle

knn = importlib.import_module('kNN')
data = pd.read_csv('../../resources/real_estate_pp.csv')

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

X = np.array(data.iloc[:, 1:-1])
y = np.array(data.iloc[:, -1:])

ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(sparse=False), [0, 4, 8])], remainder='passthrough')
X = np.array(ct.fit_transform(X))

X_train, X_test, y_train, y_test = train_test_split(X.tolist(), y, test_size=0.2, random_state=0)
X_train = csr_matrix(X_train).toarray()
X_test = csr_matrix(X_test).toarray()

ct2 = ColumnTransformer([('standard_scaler', StandardScaler(), [-3, -5, -6])], remainder='passthrough')
X_train = ct2.fit_transform(X_train)
X_test = ct2.transform(X_test)

classifier = knn.KNearestNeighbors()
classifier.fit(X_train, y_train.ravel())
y_pred = classifier.predict(X_test)

print(classification_report(y_test, y_pred))

with open('knn.pickle', 'wb') as out:
    pickle.dump(classifier, out)

with open('ohe.pickle', 'wb') as out:
    pickle.dump(ct, out)

with open('scaler.pickle', 'wb') as out:
    pickle.dump(ct2, out)
