import pickle
import streamlit as st
import pandas as pd


def unpickle_model(path):
    model = None
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model


@st.cache
def unpickle_ohe(path):
    ohe = None
    with open(path, 'rb') as f:
        ohe = pickle.load(f)
    return ohe


@st.cache
def unpickle_scaler(path):
    scaler = None
    with open(path, 'rb') as f:
        scaler = pickle.load(f)
    return scaler


@st.cache
def load_coefficients(path):
    coeff = []
    with open(path, 'r') as f:
        for l in f:
            coeff.append(float(l))
    return coeff


def get_template_df():
    return pd.DataFrame(columns=[
        'district',
        'size',
        'floor',
        'registration',
        'rooms',
        'parking',
        'balcony',
        'state'
    ])


def populate_template(district, size, floor, registration, rooms, parking, balcony, state):
    template = get_template_df()
    template = template.append({
        'district': district,
        'size': size,
        'floor': floor,
        'registration': registration,
        'rooms': rooms,
        'parking': parking,
        'balcony': balcony,
        'state': state
    },
        ignore_index=True)
    return template
