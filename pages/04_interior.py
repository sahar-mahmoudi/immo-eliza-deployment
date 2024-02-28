import streamlit as st
import json
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

# Load the image for the page icon
page_icon_image = Image.open('Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(layout="wide", page_title="Interior", page_icon=page_icon_image)

# Sidebar header
st.sidebar.header("Interior")

# Main title
st.title("Interior")

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
    # Take user inputs for interior features
    nbr_bedrooms = st.number_input('Number of bedrooms', min_value=1, max_value=int(unique_properties['nbr_bedrooms']), step=1)
    st.session_state.nbr_bedrooms = nbr_bedrooms

    equipped_kitchen_display = sorted(unique_properties_formatted['equipped_kitchen'])
    equipped_kitchen_selected = st.selectbox('Select the most appropriate description of the kitchen equipment', equipped_kitchen_display)
    equipped_kitchen = equipped_kitchen_selected.upper().replace(' ', '_')    
    st.session_state.equipped_kitchen = equipped_kitchen

    state_building_display = sorted(unique_properties_formatted['state_building'])
    state_building_selected = st.selectbox('Select the most appropriate description of the building condition', state_building_display)
    state_building = state_building_selected.upper().replace(' ', '_')
    st.session_state.state_building = state_building

# Button to proceed to the next step
next_button = st.button("Next")
if next_button:
    switch_page("energy")
