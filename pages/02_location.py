import streamlit as st
import json
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

# Load the image for the page icon
page_icon_image = Image.open('Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(layout="wide", page_title="Location", page_icon=page_icon_image)

# Sidebar header
st.sidebar.header("Location")

# Main title
st.title("Location")

# Load unique property data from JSON files
with open('uniques.json', 'r') as f:
    unique_properties = json.load(f)

with open('uniques_formatted.json','r') as f2:
    unique_properties_formatted = json.load(f2)  

with open('localities.json','r') as f3:
    localities2 = json.load(f3) 

# Hide default Streamlit format for cleaner UI
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Define the layout in two columns
left_column, right_column = st.columns([1, 2])  # Adjust the column widths as needed

# Left column for the image
with left_column:
    st.image(page_icon_image)

# Right column for the input fields and prediction result
with right_column:
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

    

    # Determine property type based on subproperty type
    if st.session_state.subproperty_type in unique_properties['house_subtypes']:
        st.session_state.property_type = 'HOUSE'
    else:
        st.session_state.property_type = 'APARTMENT'

# Button to proceed to the next step
next_button = st.button("Next")
if next_button:
    switch_page("exterior")
