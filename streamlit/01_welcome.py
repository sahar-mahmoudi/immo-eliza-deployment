import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.app_logo import add_logo

# Load the image for the page icon
page_icon_image = Image.open('streamlit/images/Price_Real_Estate_Logo.png')

# Configure Streamlit page settings
st.set_page_config(
    page_title="Welcome",
    page_icon=page_icon_image,
    layout='wide'
)

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



    <small>Enthousiastically created by Sebastiaan, Sahar, Nithyaraaj, Archana and Maarten
    
    [Repository](https://github.com/sahar-mahmoudi/immo-eliza-deployment/tree/main)</small>                                
    [API](https://immoelizapredictor.onrender.com/docs)</small>

    """,
    unsafe_allow_html=True
)


# Define options for navigation
navigation_options = ['Welcome', 'Location', 'Exterior', 'Interior', 'Energy', 'Predict!']

# Button to initiate contributing
start_contributing_button = st.button("Get started!")
if start_contributing_button:
    switch_page("Location")
