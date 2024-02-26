import streamlit as st 
import json
import requests
import pandas as pd 
import datetime
data = pd.read_csv('properties.csv')

st.title("Price predictor") # display text in title format

# taking user inputs
subproperty_type = st.selectbox('Select the type of property',
                      (data['subproperty_type'].unique())) # display select widget

region = st.selectbox('Select the region',
                      ('Flanders', 'Brussels-Capital', 'Wallonia', 'MISSING'))

province = st.selectbox('Select the province',(data['province'].unique()))

allowed_values = data['zip_code'].unique()
selected_value = st.number_input("Enter the zip code", min_value=min(allowed_values), max_value=max(allowed_values), step=1)
# Validate input
if selected_value not in allowed_values:
    st.error("Please enter a valid zip code")

today = datetime.date.today()

construction_year = st.number_input("Enter the construction year", min_value=data['construction_year'].min().astype('int'), max_value=today.year, step=1)

total_area_sqm = st.slider('Living space area in square meter', 0, data['total_area_sqm'].max().astype('int'), 1) # display slider widget

surface_land_sqm = st.slider('Total surface area in square meter', 0, data['surface_land_sqm'].max().astype('int'), 1) # display slider widget

nbr_frontages = st.slider('Number of frontages', 0, data['nbr_frontages'].max().astype('int'), 1) # display slider widget

equipped_kitchen = st.selectbox('Select the most appropriate description of the kitchen equipment',(data['equipped_kitchen'].unique()))

fl_furnished = st.radio("Is the apartment furnished?",["No", "Yes"])

fl_open_fire = st.radio("Is there an open fire?",["No", "Yes"])

fl_terrace = st.radio("Is there a terrace?",["No", "Yes"])

if fl_terrace == "Yes":
    terrace_sqm = st.slider('Terrace surface area', 0, data['terrace_sqm'].max().astype('int'), 1)

fl_garden = st.radio("Is there a garden?",["No", "Yes"])

if fl_garden == "Yes":
    garden_sqm = st.slider('Garden surface area', 0, data['garden_sqm'].max().astype('int'), 1)

fl_swimming_pool = st.radio("Is there a swimming pool?",["No", "Yes"])

fl_floodzone = st.radio("Is the property in a flood zone?",["No", "Yes"])

state_building = st.selectbox('Select the most appropriate description of the building condition',(data['state_building'].unique()))

primary_energy_consumption_sqm  = st.slider('Primary energy consumption per square meter', 
                                            0.0, data['primary_energy_consumption_sqm'].max(), 0.01) # display slider widget

epc = st.radio("In which EPC class is the property?",sorted(data['epc'].unique()))

heating_type = epc = st.radio("Which type of heating is used?",sorted(data['heating_type'].unique()))

fl_double_glazing = st.radio("Does the property have double glazing?",["No", "Yes"])

cadastral_income = st.slider('Cadastral income:', 
                                            0.0, data['cadastral_income'].max(), 0.01) # display slider widget
# convert inputs to json
inputs = {
    "subproperty_type": subproperty_type,
    "region": region,
    "province": province,
    "zip_code": selected_value,
    "construction_year": construction_year,
    "total_area_sqm": total_area_sqm,
    "surface_land_sqm": surface_land_sqm,
    "nbr_frontages": nbr_frontages,
    "equipped_kitchen": equipped_kitchen,
    "fl_furnished": fl_furnished,
    "fl_open_fire": fl_open_fire,
    "fl_terrace": fl_terrace,
    "terrace_sqm": terrace_sqm,
    "fl_garden": fl_garden,
    "garden_sqm": garden_sqm,
    "fl_swimming_pool": fl_swimming_pool,
    "fl_floodzone": fl_floodzone,
    "state_building": state_building,
    "primary_energy_consumption_sqm": primary_energy_consumption_sqm,
    "epc": epc,
    "heating_type": heating_type,
    "fl_double_glazing": fl_double_glazing,
    "cadastral_income": cadastral_income
}

# fetch api when button is clicked
if st.button('calculate'): #display button widget
    r = requests.post(url = 'http://127.0.0.1:8000/calculate', data = json.dumps(inputs))

    st.subheader(f'Response from API =  {r.text}')