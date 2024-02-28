import streamlit as st
import pandas as pd
from predict import predict
import datetime

# Function to predict price
def predict_price(input_df):
    try:
        prediction = predict(input_df)
        return prediction[0]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Title
st.title('House Price Prediction')

data = pd.read_csv("data/properties.csv")

# Input form
st.header('Input Property Details')

# Property Type
property_type = st.selectbox('Property Type', data['property_type'].unique())

# Subproperty Type
subproperty_type_options = data[data['property_type']==property_type]['subproperty_type'].unique()
subproperty_type = st.selectbox('Select the type of property', subproperty_type_options)

# Region
region = st.selectbox('Select the region', data['region'].unique())

# Province
provinces_options = data[data['region'] == region]['province'].unique()
province = st.selectbox('Select the province', provinces_options)

# Locality
localities_options = data[(data['region'] == region) & (data['province'] == province)]['locality'].unique()
locality = st.selectbox('Select the Locality', localities_options)

# Postal Code
zip_code_options = data[(data['region'] == region) & (data['province'] == province) & (data['locality'] == locality)]['zip_code'].unique()
zip_code = st.selectbox('Select the Postal Code', zip_code_options)

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

# Furnished
fl_furnished_present = col2.radio('Is the property Furnished?', ('Yes', 'No'))
if fl_furnished_present == 'Yes':
    fl_furnished = 1
else:
    fl_furnished = 0

# Equipped Kitchen
equipped_kitchen = col2.radio('Equipped Kitchen', ('Yes', 'No'))
if equipped_kitchen == 'Yes':
    kitchen_type_options = data[data['equipped_kitchen'] == 'Yes']['equipped_kitchen'].unique()
else:
    kitchen_type = None

# State of Building
state_building = st.selectbox('Building State', ['New', 'Good', 'To Renovate', 'To Restore'])

# Primary Energy Consumption
primary_energy_consumption_sqm = col2.slider('Primary Energy Consumption (sqm)', min_value=0, max_value=500, value=0)

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

# Predict button
if st.button('Predict Price'):
    # Ensure construction year is not beyond the current year
    if construction_year > current_year:
        st.error("Please enter a valid construction year.")
    else:
        # Prepare input data
        input_data = {
            'property_type': property_type,
            'subproperty_type': subproperty_type,
            'region': region,
            'province': province,
            'locality': locality,
            'zip_code': zip_code,
            'nbr_frontages': nbr_frontages,
            'construction_year': construction_year,
            'total_area_sqm': total_area_sqm,
            'surface_land_sqm': surface_land_sqm,
            'nbr_bedrooms': nbr_bedrooms,
            'fl_terrace': 1 if fl_terrace_present == 'Yes' else 0,
            'terrace_sqm': terrace_sqm,
            'fl_garden': 1 if garden_present == 'Yes' else 0,
            'garden_sqm': garden_sqm,
            'fl_furnished': fl_furnished,
            'equipped_kitchen': equipped_kitchen,
            'kitchen_type': kitchen_type,
            'state_building': state_building,
            'primary_energy_consumption_sqm': primary_energy_consumption_sqm,
            'fl_open_fire': 1 if fl_open_fire == 'Yes' else 0,
            'fl_swimming_pool': 1 if fl_swimming_pool == 'Yes' else 0,
            'fl_floodzone': 1 if fl_floodzone == 'Yes' else 0,
            'fl_double_glazing': 1 if fl_double_glazing == 'Yes' else 0,
            'epc': epc,
            'heating_type': heating_type
        }
        input_df = pd.DataFrame([input_data])

        # Make prediction
        prediction = predict_price(input_df)

        # Display prediction
        if prediction is not None:
            st.success(f'Predicted Price: {prediction:,.2f} EUR')
