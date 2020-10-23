## FireForesight
Fire risk prediction for buildings in San Francisco

This repository is my insight project at the insight data science Fall 2020 session. I developed an app that can predict building's fire risks in San francisco.
The app's user interface is as follows.

![Quickstart Success](app_gif.gif)

## Sumamry
- 1. Built an app that allows insurance companies and city governments to predict a building’s fire risk based on occupancy, year, and location
- 2. Used XGBoost and up-weighting positive cases (as only 3% of the buildings experienced fire)
- 3. Increased performance by 300% - 500% from current industry standard


## Data
Building data, fire incident data, permit data, census data, crime data etc.
These data are mostly publicly available. Due their large file sizes, I did not upload them in this repository.

## Map access
Map access in the app used mapbox API. There are quota restrictions, so it may run out when you login the app.
https://fireforesight-app.herokuapp.com/

