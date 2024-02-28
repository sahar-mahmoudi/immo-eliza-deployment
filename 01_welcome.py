import streamlit as st
from PIL import Image
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

# Display header text
st.write("# Welcome to PRICE Real Estate Predictor 👋")

# Display success message in the sidebar
st.sidebar.success("Welcome")

# Display introduction text
st.markdown(
    """
    This app helps you estimate the price range for buying a house or apartment. 
    You'll see a simple form where you can enter details about the property you're interested in, like its type, size, location, and features. 
    Don't worry, it's easy—just pick options from drop-down menus and sliders.

    Once you've filled in the details, click the "Predict!" button, and voila! 
    The app will crunch the numbers for you and show you an estimated price range based on similar properties. 
    It's like having your own real estate expert right at your fingertips!

    If you ever get stuck or have questions, don't worry. 
    Just click the button, and the app will guide you through the process. 
    
    Happy house hunting!
    """
)

# Define options for navigation
navigation_options = ['Welcome', 'Location', 'Exterior', 'Interior', 'Energy', 'Predict!']

# Button to initiate contributing
start_contributing_button = st.button("Get started!")
if start_contributing_button:
    switch_page("Location")
