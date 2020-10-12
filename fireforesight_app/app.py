"""
Created on Sept 23 2020
@author: Ruoying Xu
"""
import pickle
import os
import numpy as np
import streamlit.components.v1 as components
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
    clicked_coords = my_component()
    #st.markdown(clicked_coords)  # this is to display the coor as a separate line


# import model pickle
pickle_in = open("XGBoost_internal.sav", "rb")
prediction_model = pickle.load(pickle_in)


# @app.route('/')
def welcome():
    return "Welcome to use this app"


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

    # temporary
    fire_count_last_year = 0
    year = 2019

    cie = 0
    mips = 0
    visitor = 0
    pdr = 0
    retail = 0
    med = 0

    complaints_count = 0
    violation_count = 0
    building_permit = 0
    arson_count = 0
    other_crime_count = 10  #
    nodes_population_1500m = 0
    block_groups_total_jobs = 0
    block_groups_median_income = 0
    prop_tenure_1 = 0  #
    pumas_density_residential_units = 0
    nodes_du_800m = 0
    block_groups_median_rent = 0


    mode_input = [fire_count_last_year, year,
                  yrbuilt, bldgsqft, total_uses, cie, mips, visitor, pdr, retail, med, resunits,
                  complaints_count, violation_count, building_permit,
                  arson_count, other_crime_count,
                  nodes_population_1500m, block_groups_total_jobs, block_groups_median_income,
                  prop_tenure_1, pumas_density_residential_units, nodes_du_800m, block_groups_median_rent]

    display = ""  # need to assign first as the the app would initialized that result
    if st.button("Predict"):
        result = prediction_model.predict([mode_input])
        prediction_value = result.item(0)  # get the value
        if prediction_value == 1:
            display = 'The fire risk of this building is HIGH'
        else:
            display = 'The fire risk of this building is LOW'
    st.success('Output:  {}'.format(display))

    if st.button("About"):
        st.text("MVP version")
        st.text("Built with Streamlit")


if __name__ == '__main__':
    main()