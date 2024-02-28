import streamlit as st
import json
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

# Load the image for the page icon
page_icon_image = Image.open('Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(layout="wide", page_title="Exterior", page_icon=page_icon_image)

# Sidebar header
st.sidebar.header("Exterior")

# Main title
st.title("Exterior")

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
    # Take user inputs for exterior features
    total_area_sqm = st.number_input('Living space area in square meter', min_value=1, max_value=int(unique_properties['total_area_sqm']), step=1)
    st.session_state.total_area_sqm = total_area_sqm
    
    surface_land_sqm = st.number_input('Total surface area in square meter', min_value=1, max_value=int(unique_properties['surface_land_sqm']), step=1)
    st.session_state.surface_land_sqm = surface_land_sqm
    
    nbr_frontages = st.number_input('Number of frontages', min_value=1, max_value=int(unique_properties['max_frontages']), step=1)
    st.session_state.nbr_frontages = nbr_frontages
    
    fl_terrace = st.radio("Is there a terrace?", ["No", "Yes"], horizontal=True)
    st.session_state.fl_terrace = fl_terrace
    
    if fl_terrace == "Yes":
        terrace_sqm = st.number_input('Terrace surface area', min_value=1, max_value=int(unique_properties['terrace_sqm']), step=1)
        st.session_state.terrace_sqm = terrace_sqm
    else:
        st.session_state.terrace_sqm = 0

    fl_garden = st.radio("Is there a garden?", ["No", "Yes"], key='fl_garden', horizontal=True)
    
    if fl_garden == "Yes":
        garden_sqm = st.number_input('Garden surface area', min_value=0, max_value=int(unique_properties['garden_sqm']), step=1)
        st.session_state.garden_sqm = garden_sqm
    else:
        st.session_state.garden_sqm = 0
    
    fl_swimming_pool = st.radio("Is there a swimming pool?", ["No", "Yes"], horizontal=True)
    st.session_state.fl_swimming_pool = fl_swimming_pool

    # Convert radio button choices to integer values (0 for No, 1 for Yes)
    fl_terrace_int = 1 if fl_terrace == "Yes" else 0
    fl_garden_int = 1 if fl_garden == "Yes" else 0
    fl_swimming_pool_int = 1 if fl_swimming_pool == "Yes" else 0
    
    # Store integer values in session state
    st.session_state.fl_terrace_int = fl_terrace_int
    st.session_state.fl_garden_int = fl_garden_int
    st.session_state.fl_swimming_pool_int = fl_swimming_pool_int

# Button to proceed to the next step
next_button = st.button("Next")
if next_button:
    switch_page("interior")
