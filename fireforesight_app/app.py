"""
Created on Sept 23 2020
@author: Ruoying Xu
"""
import pickle
import os
import numpy as np
import pandas as pd
import streamlit.components.v1 as components
from math import cos, asin, sqrt
import streamlit as st

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "my_component",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)


def my_component(key=None):
    component_value = _component_func(key=key, default=0)
    return component_value

# leaflet mapbox api key: https://account.mapbox.com/

if not _RELEASE:

    import streamlit as st

    html_temp = """
        <div style="background-color:tomato;padding:10px">
        <h2 style="color:white;text-align:center;">Fire risk prediction </h2>
        </div>
        """
    st.markdown(html_temp, unsafe_allow_html=True)

    st.subheader("Please find your building's location on the map")
    click_coor = my_component()

    if click_coor !=0:

        input_coor = {}
        input_coor['lng'] = click_coor['lng']
        input_coor['lat'] = click_coor['lat']
    #st.markdown(click_coor)  # this is to display the coor as a separate line


# import model pickle
pickle_in = open("XGBoost_internal.sav", "rb")
prediction_model = pickle.load(pickle_in)


# @app.route('/')
def welcome():
    return "Welcome to use this app"


#calculate distance
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, input_num):
    return min(data, key=lambda p: distance(input_num['lat'],input_num['lng'],p['lat'],p['lng']))


# @app.route('/predict',methods=["Get"])
def predict_fire_risk(yrbuilt, bldgsqft, total_uses, resunits, other_crime_count, prop_tenure_1, fire_count_last_year, year):
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
            yrbuilt, bldgsqft, total_uses, resunits, other_crime_count, prop_tenure_1, fire_count_last_year, year
    """

    prediction = prediction_model.predict([[yrbuilt, bldgsqft, total_uses, resunits, other_crime_count, prop_tenure_1, fire_count_last_year, year]])
    print(prediction)
    return prediction

def main():

    html_temp = """
    <div style="background-color:orange;padding:6px">
    <h3 style="color:white;text-align:center;">Please enter your building info below </h3>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    yrbuilt = st.text_input("Year built", "1990")
    bldgsqft = st.text_input("total building area, sqft", "0")
    total_uses = st.text_input("all business sqft", "0")
    resunits = st.text_input("number of residential units", "0")

    retail = st.text_input("Areas for retail, sqft", "0")
    mips = st.text_input("Areas for offices, sqft", "0")
    visitor = st.text_input("Areas for hotel, sqft", "0")
    pdr = st.text_input("Areas for manufacturing, sqft", "0")
    med = st.text_input("Areas for medical services, sqft", "0")
    cie = st.text_input("Areas for schoold/institution, sqft", "0")

    html_temp_2 = """
        <div style="background-color:orange;padding:5px">
        <h4 style="color:white;text-align:center;">Please enter your building fire records</h4>
        </div>
        """
    st.markdown(html_temp_2, unsafe_allow_html=True)

    fire_count_last_year = st.text_input("number of fire incidents previoius year", "0")
    complaints_count = st.text_input("How many fire-related complaints last year", "0")
    violation_count = st.text_input("How many fire-related violations last year", "0")
    building_permit = st.text_input("How many building permits", "0")

    year = 2019

    x_input = [fire_count_last_year, year,
               yrbuilt, bldgsqft, total_uses, cie, mips, visitor, pdr, retail, med, resunits,
               complaints_count, violation_count, building_permit]



    # find the blk that are closest to input
    # input data first
    df_blk_avg = pd.read_pickle('location_data.pkl')
    df_blk_coor = df_blk_avg.iloc[:, :2]
    list_blk_coor = df_blk_coor.to_dict('records')  # change to list

    i = list_blk_coor.index(closest(list_blk_coor, input_coor))  # data name
    # match the other features
    x_plus = np.array(df_blk_avg.iloc[i, 2:])  # data name

    # concat x
    x = (np.concatenate((x_input, x_plus), axis=0)).reshape(1, 24)

    display = ""  # need to assign first as the the app would initialized that result
    if st.button("Predict"):
        result = prediction_model.predict(x)
        prediction_value = result.item(0)  # get the value
        display = 'The fire risk of this building is HIGH' if prediction_value == 1 else 'The fire risk of this building is LOW'
    st.success('Output:  {}'.format(display))

    if st.button("About"):
        st.text("MVP version")
        st.text("Built with Streamlit")


if __name__ == '__main__':
    main()