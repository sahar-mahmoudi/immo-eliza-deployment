import streamlit as st
import json
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

# Load the image for the page icon
page_icon_image = Image.open('Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(layout="wide", page_title="Energy", page_icon=page_icon_image)

# Sidebar header
st.sidebar.header("Energy")

# Main title
st.title("Energy")

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

# Define the layout in two columns
left_column, right_column = st.columns([1, 2])  # Adjust the column widths as needed

# Left column for the image
with left_column:
    st.image(page_icon_image)

# Right column for the input fields and prediction result
with right_column:
    # Take user inputs for energy features
    epc_display = sorted(unique_properties_formatted['epc'])
    epc_selected = st.radio("In which EPC class is the property?", epc_display, horizontal=True)
    epc = epc_selected.upper().replace(' ', '_')
    st.session_state.epc = epc

    heating_type_display = sorted(unique_properties_formatted['heating_type'])
    heating_type_selected = st.radio("Which type of heating is used?", heating_type_display, horizontal=True)
    heating_type = heating_type_selected.upper().replace(' ', '_')
    st.session_state.heating_type = heating_type

# Button to see the prediction result
see_result_button = st.button("See my result!")
if see_result_button:
    switch_page("predict")
