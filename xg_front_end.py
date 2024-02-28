import streamlit as st
import json
import requests
from pydantic import BaseModel  # Add this import
import pandas as pd
from PIL import Image
from zipcodes import get_long, get_lat, get_province, get_region


im = Image.open('Price_Real_Estate_Logo.png')

st.set_page_config(layout="wide", page_title="Real Estate Price Predictor", page_icon=im)

with open('uniques.json', 'r') as f:
    uniques = json.load(f)

with open('uniques_formatted.json','r') as f2:
    uniques_formatted = json.load(f2)  

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Define the layout in two columns
col1, col2 = st.columns([1, 2])  # Adjust the column widths as needed

# Left column for the image
with col1:
    st.image(im)

# Right column for the input fields and prediction result
with col2:
    class Item(BaseModel):
        nbr_frontages: float
        nbr_bedrooms: float
        latitude: float
        longitude: float
        total_area_sqm: float
        surface_land_sqm: float
        terrace_sqm: float
        garden_sqm: float
        fl_terrace: int
        fl_garden: int
        fl_swimming_pool: int
        province: str
        heating_type: str
        state_building: str
        property_type: str
        epc: str
        locality: str
        subproperty_type: str
        region: str

    data = pd.read_csv('properties.csv')

    st.title("Real Estate Price Predictor")

    # taking user inputs
    display = uniques_formatted['subproperty_type']
    selected = st.selectbox('Select the type of property', display)
    subproperty_type = selected.upper().replace(' ', '_')

    allowed_values = data['zip_code'].unique()
    zip_code = st.number_input("Enter the zip code", min_value=min(allowed_values), max_value=max(allowed_values), step=1)
    if zip_code not in allowed_values:
        st.error("Please enter a valid zip code")

    locality = st.selectbox('Select the locality', uniques['locality'])


    #today = datetime.date.today()
    
    total_area_sqm = st.number_input('Living space area in square meter', min_value=1, max_value=data['total_area_sqm'].max().astype('int'), step=1)
    
    surface_land_sqm = st.number_input('Total surface area in square meter', min_value=1, max_value=data['surface_land_sqm'].max().astype('int'), step=1)
    
    nbr_frontages = st.number_input('Number of frontages', min_value=1, max_value=data['nbr_frontages'].max().astype('int'), step=1)
    
    nbr_bedrooms = st.number_input('Number of bedrooms',min_value=1, max_value=data['nbr_bedrooms'].max().astype('int'), step=1)

    equipped_kitchen_display = uniques_formatted['equipped_kitchen']
    equipped_kitchen_selected = st.selectbox('Select the most appropriate description of the kitchen equipment', equipped_kitchen_display)
    equipped_kitchen = equipped_kitchen_selected.upper().replace(' ', '_')    

    fl_terrace = st.radio("Is there a terrace?", ["No", "Yes"], horizontal=True)
    
    if fl_terrace == "Yes":
        terrace_sqm = st.number_input('Terrace surface area', min_value=1, max_value=data['terrace_sqm'].max().astype('int'), step=1)
    else:
        terrace_sqm = 0

    fl_garden = st.radio("Is there a garden?", ["No", "Yes"], key='fl_garden', horizontal=True)
    if fl_garden == "Yes":
        garden_sqm = st.number_input('Garden surface area', min_value=0, max_value=data['garden_sqm'].max().astype('int'), step=1)
    else:
        garden_sqm = 0
    fl_swimming_pool = st.radio("Is there a swimming pool?", ["No", "Yes"], horizontal=True)
    
    state_building_display = uniques_formatted['state_building']
    state_building_selected = st.selectbox('Select the most appropriate description of the building condition', state_building_display)
    state_building = state_building_selected.upper().replace(' ', '_')    

    epc_display = sorted(uniques_formatted['epc'])
    epc_selected = st.radio("In which EPC class is the property?", epc_display, horizontal=True)
    epc = epc_selected.upper().replace(' ', '_')    

    heating_type_display = uniques_formatted['heating_type']
    heating_type_selected = st.radio("Which type of heating is used?", heating_type_display, horizontal=True)
    heating_type = heating_type_selected.upper().replace(' ', '_')

    fl_terrace_int = 1 if fl_terrace == "Yes" else 0
    fl_garden_int = 1 if fl_garden == "Yes" else 0
    fl_swimming_pool_int = 1 if fl_swimming_pool == "Yes" else 0

    if subproperty_type in data[data['property_type'] == 'HOUSE']['subproperty_type'].unique():
        property_type = 'HOUSE'
    else:
        property_type = 'APARTMENT'
    # convert inputs to json
    inputs = {
        "subproperty_type": subproperty_type,
        "region": get_region(zip_code),
        "province": get_province(zip_code),
        "total_area_sqm": total_area_sqm,
        "surface_land_sqm": surface_land_sqm,
        "nbr_frontages": nbr_frontages,
        "equipped_kitchen": equipped_kitchen,
        "fl_terrace": fl_terrace_int,
        "terrace_sqm": terrace_sqm,
        "fl_garden": fl_garden_int,
        "garden_sqm": garden_sqm,
        "fl_swimming_pool": fl_swimming_pool_int,
        "state_building": state_building,
        "epc": epc,
        "heating_type": heating_type,
        "nbr_bedrooms": nbr_bedrooms,
        "latitude": get_lat(zip_code),  
        "longitude": get_long(zip_code),  
        "property_type": "APARTMENT",  # Provide a default value for property_type
        "locality": locality,  # Provide a default value for locality
    }
    for key, value in inputs.items():
        if value == 'NOT_AVAILABLE':
            inputs[key] = 'MISSING'
    # fetch api when button is clicked
    if st.button('Predict!'):
        try:
            print("Inputs: ")
            print(inputs)
            r = requests.post('https://immo-eliza-deployment-4.onrender.com/predict', json=inputs)
            if r.status_code == 200:
                response_data = r.json()
                lower_bound = response_data['price_range']['lower_bound'].replace(',', '')
                upper_bound = response_data['price_range']['upper_bound'].replace(',', '')
                formatted_lower_bound = "€{:,.0f}".format(round(int(lower_bound) / 1000) * 1000)
                formatted_upper_bound = "€{:,.0f}".format(round(int(upper_bound) / 1000) * 1000)
                st.subheader(f"Predicted price range: {formatted_lower_bound} - {formatted_upper_bound}")
            else:
                st.error(f"Error: {r.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")