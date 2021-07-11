import streamlit as st
import importlib
import os
import numpy as np
import pandas as pd

data = pd.read_csv('..//resources/real_estate_preprocessed.csv')
data = data[['district', 'size', 'floor', 'registration', 'rooms', 'parking', 'balcony', 'state', 'price']]
districts = data['district'].unique()
states = data['state'].unique()

st.title('Belgrade apartments for sale')
settings = importlib.import_module('settings')
helpers = importlib.import_module('helpers')

model_path = os.path.join(settings.CLASSIFICATION_SETTINGS.DIRECTORY.value, settings.CLASSIFICATION_SETTINGS.MODEL.value)
classifier = helpers.unpickle_model(model_path)
opt_k = classifier.k
dist_metric = classifier.f

method = st.sidebar.radio('Please select desired method:', options=[model.value for model in settings.MODELS])

if method == settings.MODELS.LINEAR_REGRESSION.value:
    district = st.selectbox(
        'District:',
        sorted(districts)
    )
    size = st.number_input('Size (m2):', min_value=0, value=45)
    floor = st.number_input('Floor:', min_value=0, value=1)
    registration = st.selectbox(
        'Registered:',
        [True, False]
    )
    rooms = st.number_input('Number of rooms:', min_value=1, value=1)
    parking = st.selectbox(
        'Parking:',
        [True, False]
    )
    balcony = st.selectbox(
        'Balcony:',
        [True, False]
    )
    state = st.selectbox(
        'State:',
        sorted(states)
    )

    input = helpers.populate_template(district, size, floor, registration, rooms, parking, balcony, state)

    if st.button('Predict price'):
        coeff_path = os.path.join(settings.REGRESSION_SETTINGS.DIRECTORY.value,
                                settings.REGRESSION_SETTINGS.COEFF.value)
        coeff = helpers.load_coefficients(coeff_path)
        ohe_path = os.path.join(settings.REGRESSION_SETTINGS.DIRECTORY.value,
                                settings.REGRESSION_SETTINGS.ENCODER.value)
        ohe = helpers.unpickle_ohe(ohe_path)
        scaler_path = os.path.join(settings.REGRESSION_SETTINGS.DIRECTORY.value,
                                   settings.REGRESSION_SETTINGS.SCALER.value)
        scaler = helpers.unpickle_scaler(scaler_path)
        model_path = os.path.join(settings.REGRESSION_SETTINGS.DIRECTORY.value,
                                  settings.REGRESSION_SETTINGS.MODEL.value)
        regressor = helpers.unpickle_model(model_path)
        input = np.array(ohe.transform(input))
        input = scaler.transform(input)
        prediction = regressor.predict(input)
        st.subheader(f'Predicted price: : {round(prediction[0], 2)} €.')
else:
    k = st.number_input('k (number of neighbors):', min_value=1, max_value=classifier.rows, value=opt_k)
    distance = st.selectbox(
        'Distance metric:',
        ['Euclidean distance', 'Manhattan distance']
    )
    district = st.selectbox(
        'District:',
        sorted(districts)
    )
    size = st.number_input('Size (m2):', min_value=0, value=45)
    floor = st.number_input('Floor:', min_value=0, value=1)
    registration = st.selectbox(
        'Registered:',
        [True, False]
    )
    rooms = st.number_input('Number of rooms:', min_value=1, value=1)
    parking = st.selectbox(
        'Parking:',
        [True, False]
    )
    balcony = st.selectbox(
        'Balcony:',
        [True, False]
    )
    state = st.selectbox(
        'State:',
        sorted(states)
    )

    input = helpers.populate_template(district, size, floor, registration, rooms, parking, balcony, state)

    if st.button('Predict price segment'):
        ohe_path = os.path.join(settings.CLASSIFICATION_SETTINGS.DIRECTORY.value,
                                settings.CLASSIFICATION_SETTINGS.ENCODER.value)
        ohe = helpers.unpickle_ohe(ohe_path)
        scaler_path = os.path.join(settings.CLASSIFICATION_SETTINGS.DIRECTORY.value,
                                   settings.CLASSIFICATION_SETTINGS.SCALER.value)
        scaler = helpers.unpickle_scaler(scaler_path)
        model_path = os.path.join(settings.CLASSIFICATION_SETTINGS.DIRECTORY.value,
                                  settings.CLASSIFICATION_SETTINGS.MODEL.value)
        classifier = helpers.unpickle_model(model_path)
        classifier.k = k
        if distance == 'Euclidean distance':
            classifier.f = classifier.euclidean_distance
        else:
            classifier.f = classifier.manhattan_distance
        input = np.array(ohe.transform(input))
        input = scaler.transform(input)
        prediction = classifier.predict(input)
        st.subheader(f'Predicted price segment: {prediction[0]}.')

