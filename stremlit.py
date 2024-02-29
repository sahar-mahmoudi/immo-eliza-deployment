import streamlit as st
import json
import requests
import pandas as pd
import datetime
from PIL import Image

im = Image.open('streamlit/images/Price_Real_Estate_Logo.png')

st.set_page_config(layout="wide", page_title="Real Estate Price Predictor", page_icon=im)

with open('streamlit/uniques.json', 'r') as f:
    uniques = json.load(f)

with open('streamlit/uniques_formatted.json', 'r') as f2:
    uniques_formatted = json.load(f2)

hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# Define the layout in two columns
col1, col2 = st.columns([1, 2])  # Adjust the column widths as needed

# Left column for the image
with col1:
    st.image(im)

# Right column for the input fields and prediction result
with col2:
    data = pd.read_csv('streamlit/properties.csv')

    st.title("Real Estate Price Predictor")

    # Page 1: Choose Location
    if st.session_state.page == 1 or 'page' not in st.session_state:
        st.header('Choose Location')

        # Region
        region = st.selectbox('Select the region', data['region'].unique())

        # Province
        provinces_options = data[data['region'] == region]['province'].unique()
        province = st.selectbox('Select the province', provinces_options)

        # Locality
        localities_options = data[(data['region'] == region) & (data['province'] == province)]['locality'].unique()
        locality = st.selectbox('Select the Locality', localities_options)

        st.write('---')
        st.write('Go to next page:')
        if st.button('Next'):
            st.session_state.page = 2

    # Page 2: Enter Property Details
    elif st.session_state.page == 2:
        st.header('Enter Property Details')

        # Define columns for better layout
        col1, col2 = st.columns(2)

        # Number of Frontages
        nbr_frontages = col1.slider('Number of Frontages', min_value=0, max_value=10, value=0)

        # Construction Year
        current_year = datetime.datetime.now().year
        construction_year = col1.number_input('Construction Year', min_value=0, max_value=current_year, value=0)

        # Total Area
        total_area_sqm = col1.slider('Total Area (sqm)', min_value=0, max_value=500, value=0)

        # Surface Land
        surface_land_sqm = col1.slider('Surface Land (sqm)', min_value=0, max_value=500, value=0)

        # Number of Bedrooms
        nbr_bedrooms = col1.slider('Number of Bedrooms', min_value=0, max_value=10, value=0)

        # Terrace
        fl_terrace_present = col2.radio('Is there a Terrace?', ('Yes', 'No'))
        if fl_terrace_present == 'Yes':
            terrace_sqm = col2.slider('Terrace Area (sqm)', min_value=0, max_value=100, value=0)
        else:
            terrace_sqm = 0

        # Garden
        garden_present = col2.radio('Is there a Garden?', ('Yes', 'No'))
        if garden_present == 'Yes':
            garden_sqm = col2.slider('Garden Area (sqm)', min_value=0, max_value=500, value=0)
        else:
            garden_sqm = 0

        st.write('---')
        st.write('Go to next page:')
        if st.button('Next'):
            st.session_state.page = 3

    # Page 3: Enter Additional Details
    elif st.session_state.page == 3:
        st.header('Enter Additional Details')

        # State of Building
        state_building = st.selectbox('Building State', ['New', 'Good', 'To Renovate', 'To Restore'])

        # Primary Energy Consumption
        primary_energy_consumption_sqm = st.slider('Primary Energy Consumption (sqm)', min_value=0, max_value=500, value=0)

        # Open Fire
        fl_open_fire = st.radio('Has Open Fire', ('Yes', 'No'))

        # Swimming Pool
        fl_swimming_pool = st.radio('Has Swimming Pool', ('Yes', 'No'))

        # Flood Zone
        fl_floodzone = st.radio('Is in Flood Zone', ('Yes', 'No'))

        # Double Glazing
        fl_double_glazing = st.radio('Has Double Glazing', ('Yes', 'No'))

        # Energy Performance Certificate
        epc = st.selectbox('Energy Performance Certificate', ['A', 'B', 'C', 'D', 'E', 'F', 'G'])

        # Heating Type
        heating_type = st.selectbox('Heating Type', ['Gas', 'Fuel Oil', 'Electricity', 'Wood', 'Other'])

        st.write('---')
        st.write('Go to next page:')
        if st.button('Predict'):
            st.session_state.page = 4

    # Page 4: Review and Predict
    elif st.session_state.page == 4:
        st.header('Review and Predict')

        # Display selected inputs for review
        st.subheader('Selected Location:')
        st.write('Region:', region)
        st.write('Province:', province)
        st.write('Locality:', locality)

        st.subheader('Property Details:')
        st.write('Number of Frontages:', nbr_frontages)
        st.write('Construction Year:', construction_year)
        st.write('Total Area (sqm):', total_area_sqm)
        st.write('Surface Land (sqm):', surface_land_sqm)
        st.write('Number of Bedrooms:', nbr_bedrooms)
        st.write('Terrace Area (sqm):', terrace_sqm)
        st.write('Garden Area (sqm):', garden_sqm)

        st.subheader('Additional Details:')
        st.write('Building State:', state_building)
        st.write('Primary Energy Consumption (sqm):', primary_energy_consumption_sqm)
        st.write('Has Open Fire:', fl_open_fire)
        st.write('Has Swimming Pool:', fl_swimming_pool)
        st.write('Is in Flood Zone:', fl_floodzone)
        st.write('Has Double Glazing:', fl_double_glazing)
        st.write('Energy Performance Certificate:', epc)
        st.write('Heating Type:', heating_type)

        # Prepare input data
        input_data = {
            'nbr_frontages': nbr_frontages,
            'construction_year': construction_year,
            'total_area_sqm': total_area_sqm,
            'surface_land_sqm': surface_land_sqm,
            'nbr_bedrooms': nbr_bedrooms,
            'fl_terrace': 1 if fl_terrace_present == 'Yes' else 0,
            'terrace_sqm': terrace_sqm,
            'fl_garden': 1 if garden_present == 'Yes' else 0,
            'garden_sqm': garden_sqm,
            'state_building': state_building,
            'primary_energy_consumption_sqm': primary_energy_consumption_sqm,
            'fl_open_fire': 1 if fl_open_fire == 'Yes' else 0,
            'fl_swimming_pool': 1 if fl_swimming_pool == 'Yes' else 0,
            'fl_floodzone': 1 if fl_floodzone == 'Yes' else 0,
            'fl_double_glazing': 1 if fl_double_glazing == 'Yes' else 0,
            'epc': epc,
            'heating_type': heating_type
        }

        # fetch api when button is clicked
        if st.button('Predict!'):
            try:
                r = requests.post('http://localhost:8000/predict', json=input_data)
                if r.status_code == 200:
                    response_data = r.json()
                    lower_bound = response_data['price_range']['lower_bound']
                    upper_bound = response_data['price_range']['upper_bound']
                    st.subheader(f"Predicted price range: {lower_bound} - {upper_bound}")
                else:
                    st.error(f"Error: {r.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
