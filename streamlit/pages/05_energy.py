import streamlit as st
import json
from PIL import Image
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo


# Load the image for the page icon
page_icon_image = Image.open('streamlit/images/Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(page_title="Energy", page_icon=page_icon_image)

# Sidebar header
st.sidebar.header("Energy")

# Main title
st.title("Energy")

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

add_logo('streamlit\images\Price_Real_Estate_Logo_small.png', height=200)


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
