import streamlit as st
import json
from PIL import Image
from zipcodes import get_lat, get_long, get_province, get_region
from pydantic import BaseModel
import requests
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

# Load the image for the page icon
page_icon_image = Image.open('Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(
    page_title="Hello Streamlit",
    page_icon=page_icon_image,
)

# Hide default Streamlit format for cleaner UI
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://cdn.discordapp.com/attachments/1211692140036489246/1212707946555768832/homepage.png?ex=65f2d149&is=65e05c49&hm=916b806fc3513a19fa3227063c6685ce06953947c15d11833f7b545391c28a54&");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

#st.markdown(background_image, unsafe_allow_html=True)


# Sidebar header
st.sidebar.header("Prediction time!")

# Main title
st.title("Prediction time!")

# Load unique property data from JSON files
with open('uniques.json', 'r') as f:
    unique_properties = json.load(f)

with open('uniques_formatted.json', 'r') as f2:
    unique_properties_formatted = json.load(f2)  

# Hide default Streamlit format for cleaner UI
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


# Access session state variables set in location.py
subproperty_type = st.session_state.subproperty_type
zip_code = st.session_state.zip_code
locality = st.session_state.locality
property_type = st.session_state.property_type

# Access session state variables set in exterior.py
total_area_sqm = st.session_state.total_area_sqm
surface_land_sqm = st.session_state.surface_land_sqm
nbr_frontages = st.session_state.nbr_frontages
fl_terrace = st.session_state.fl_terrace
terrace_sqm = st.session_state.terrace_sqm
garden_sqm = st.session_state.garden_sqm
fl_swimming_pool = st.session_state.fl_swimming_pool
fl_terrace_int = st.session_state.fl_terrace_int
fl_garden_int = st.session_state.fl_garden_int 
fl_swimming_pool_int = st.session_state.fl_swimming_pool_int

# Access session state variables set in interior.py
nbr_bedrooms = st.session_state.nbr_bedrooms
equipped_kitchen = st.session_state.equipped_kitchen
state_building = st.session_state.state_building

# Access session state variables set in interior.py and energy.py
epc = st.session_state.epc
heating_type = st.session_state.heating_type

# Now you can use these variables for prediction or any other purpose

# Right column for the input fields and prediction result

# Define the input model for prediction
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

# Prepare input data for prediction
inputs = {
    "property_type": property_type,  
    "subproperty_type": subproperty_type,
    "region": get_region(zip_code),
    "province": get_province(zip_code),
    "locality": locality, 
    "total_area_sqm": total_area_sqm,
    "surface_land_sqm": surface_land_sqm,
    "nbr_frontages": nbr_frontages,
    "fl_terrace": fl_terrace_int,
    "terrace_sqm": terrace_sqm,
    "fl_garden": fl_garden_int,
    "garden_sqm": garden_sqm,
    "fl_swimming_pool": fl_swimming_pool_int,
    "nbr_bedrooms": nbr_bedrooms,
    "equipped_kitchen": equipped_kitchen,
    "state_building": state_building,
    "epc": epc,
    "heating_type": heating_type,
    "latitude": get_lat(zip_code),  
    "longitude": get_long(zip_code),  
    
     
}

# Replace 'NOT_AVAILABLE' with 'MISSING'
for key, value in inputs.items():
    if value == 'NOT_AVAILABLE':
        inputs[key] = 'MISSING'

df = pd.DataFrame(inputs, index=['Value'])
df.set_index()
df = df.transpose()
for i in df[df.iloc(0)]:
    i.str.replace('fl_','')
st.table(df)



# fetch API when button is clicked
if st.button('Predict!'):
    with st.spinner('Wait for it...'):
        try:
            r = requests.post('https://immoelizapredictor.onrender.com/predict', json=inputs)
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

# Button to initiate another prediction
want_to_contribute = st.button("Another one!")
if want_to_contribute:
    switch_page("location")
