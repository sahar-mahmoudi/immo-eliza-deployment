import json

import folium
from PIL import Image
from streamlit_extras.switch_page_button import switch_page
from streamlit_folium import st_folium
from zipcodes import get_lat, get_long
from streamlit_extras.app_logo import add_logo

import streamlit as st

lat, lon = "50.4564", "4.1851"
coords = [lat, lon]

# Load the image for the page icon
page_icon_image = Image.open('streamlit/images/Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(layout="wide", page_title="Location", page_icon=page_icon_image)

# Sidebar header
st.sidebar.header("Location")

# Main title
st.title("Location")

# Load unique property data from JSON files
with open('streamlit/uniques.json', 'r') as f:
    unique_properties = json.load(f)

with open('streamlit/uniques_formatted.json','r') as f2:
    unique_properties_formatted = json.load(f2)  

with open('streamlit/localities.json','r') as f3:
    localities2 = json.load(f3) 

# Hide default Streamlit format for cleaner UI
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://media.discordapp.net/attachments/1192782231551348796/1212746688218009620/welcome_image_clean.png?ex=65f2f55e&is=65e0805e&hm=9006958d613228a7c4720ece9246a1e03b5903fa3e4beafd8e28af67625d2ac7&=&format=webp&quality=lossless&width=2022&height=1138");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: right;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

add_logo('streamlit/images/Price_Real_Estate_Logo_small.png', height=200)

# Define the layout in two columns
left_column, right_column = st.columns([1, 1])  # Adjust the column widths as needed

# Left column for the image
with left_column:
    # Select property type
    display_subproperty_types = sorted(unique_properties_formatted['subproperty_type'])
    selected_subproperty_type = st.selectbox('Select the type of property', display_subproperty_types)
    st.session_state.subproperty_type = selected_subproperty_type.upper().replace(' ', '_')

    # Select locality
    localities = sorted(unique_properties['locality'])
    selected_locality = st.selectbox('Select the locality', localities)
    st.session_state.locality = selected_locality

    # Select zip code
    zip_codes = localities2[selected_locality]
    selected_zip_code = st.selectbox("Enter the zip code", sorted(zip_codes))
    st.session_state.zip_code = selected_zip_code
    
    if selected_zip_code:
        lat, lon = get_lat(selected_zip_code), get_long(selected_zip_code)
        coords = [lat, lon]

# Right column for the input fields and prediction result
with right_column:
    
    st.markdown('The algorithm estimates the coordinates based on the provided zip code.')
    st.markdown('If you want to use more accurate coordinates, select the position on the map.')
    # Create folium map using openstreetmap
    m = folium.Map(location=coords, zoom_start=17)
    
    # Add LocateControl to the map
    # folium.plugins.LocateControl().add_to(m)

    # Add LatLngPopup plugin
    folium.LatLngPopup().add_to(m)

    # Call to render Folium map in Streamlit
    osm_data = st_folium(m, width=750, height=400)

    if osm_data["last_clicked"]:
        lat, lon = osm_data["last_clicked"]["lat"], osm_data["last_clicked"]["lng"]
    
    st.session_state["lat"] = lat
    st.session_state["lon"] = lon

    

    # Determine property type based on subproperty type
    if st.session_state.subproperty_type in unique_properties['house_subtypes']:
        st.session_state.property_type = 'HOUSE'
    else:
        st.session_state.property_type = 'APARTMENT'

# Button to proceed to the next step
next_button = st.button("Next")
if next_button:
    switch_page("exterior")
