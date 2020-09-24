"""
Created on Sept 23 2020
@author: Ruoying Xu
"""

import numpy as np
import pickle
import pandas as pd
# from flasgger import Swagger
import streamlit as st

from PIL import Image

# app=Flask(__name__)
# Swagger(app)

# import model pickle
pickle_in = open("premitive_model.pkl", "rb")
prediction_model = pickle.load(pickle_in)


# @app.route('/')
def welcome():
    return "Welcome to use this app"


# @app.route('/predict',methods=["Get"])
def predict_fire_risk(yrbuilt, total_sqft, total_sqft_used, cie, mips, visitors, pdr, retail, med, resunits):
    """Let's Authenticate the Banks Note
    This is using docstrings for specifications.
    ---
    parameters:
      - name: variance
        in: query
        type: number
        required: true
      - name: skewness
        in: query
        type: number
        required: true
      - name: curtosis
        in: query
        type: number
        required: true
      - name: entropy
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values

            'yrbuilt','bldgsqft','total_uses','cie','mips','visitor', 'pdr', 'retail', 'med','resunits'
            yrbuilt, total_sqft, total_sqft_used, cie, mips, visitors, pdr, retail, med, resunits
    """

    prediction = prediction_model.predict([[yrbuilt, total_sqft, total_sqft_used, cie, mips, visitors, pdr, retail, med, resunits]])
    print(prediction)
    return prediction


def main():
    st.title("Fire risk prediction")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit fire risk ML App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    yrbuilt = st.text_input("Year built", "1990")
    total_sqft = st.text_input("total building area, sqft", "0")
    total_sqft_used = st.text_input("all business sqft", "0")
    resunits = st.text_input("number of residential units", "0")
    retail = st.text_input("retail sqft", "0")
    mips = st.text_input("general office, sqft", "0")
    visitors = st.text_input("hotel sqft", "0")
    pdr = st.text_input("industrial and production, sqft", "0")
    med = st.text_input("medical sqft", "0")
    cie = st.text_input("school and institution, sqft", "0")

    result = ""
    if st.button("Predict"):
        result = predict_fire_risk(yrbuilt, total_sqft, total_sqft_used, cie, mips, visitors, pdr, retail, med, resunits)
    st.success('The number of incidents is {}'.format(result))

    if st.button("About"):
        st.text("MVP version")
        st.text("Built with Streamlit")


if __name__ == '__main__':
    main()
