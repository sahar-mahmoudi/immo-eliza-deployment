import streamlit as st
import json
from PIL import Image
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo


# Load the image for the page icon
page_icon_image = Image.open('streamlit/images/Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(page_title="Interior", page_icon=page_icon_image)

# Sidebar header
st.sidebar.header("Interior")

# Main title
st.title("Interior")

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
