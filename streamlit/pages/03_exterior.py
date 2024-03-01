import streamlit as st
import json
from PIL import Image
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo


# Load the image for the page icon
page_icon_image = Image.open('streamlit/images/Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(page_title="Exterior", page_icon=page_icon_image)

# Sidebar header
st.sidebar.header("Exterior")

# Main title
st.title("Exterior")

# Load unique property data from JSON files
with open('streamlit/uniques.json', 'r') as f:
    unique_properties = json.load(f)

with open('streamlit/uniques_formatted.json', 'r') as f2:
    unique_properties_formatted = json.load(f2)

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
