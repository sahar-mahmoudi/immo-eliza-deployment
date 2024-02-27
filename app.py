import streamlit as st
import pandas as pd
from predict import predict

# Function to predict price
def predict_price(input_df):
    try:
        prediction = predict(input_df)
        return prediction[0]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to validate numeric input
def validate_numeric_input(value, field_name):
    if not isinstance(value, (int, float)):
        st.warning(f"Please provide a numerical value for '{field_name}'.")
        return None
    return value

# Title
st.title('House Price Prediction')

data = pd.read_csv("data/properties.csv")

# Get the earliest and current year from the dataset
earliest_year = data['construction_year'].min()
current_year = pd.Timestamp.now().year

# Input form
st.header('Input Property Details')
nbr_frontages = st.number_input('Number of Frontages', value=0)
construction_year = st.number_input('Construction Year', min_value=earliest_year, max_value=current_year, value=0)
total_area_sqm = st.number_input('Total Area (sqm)', value=0)
surface_land_sqm = st.number_input('Surface Land (sqm)', value=0)
nbr_bedrooms = st.number_input('Number of Bedrooms', value=0)
fl_terrace_present = st.selectbox('Is there a Terrace?', ['Yes', 'No'])
if fl_terrace_present == 'Yes':
    terrace_sqm = st.number_input('Terrace Area (sqm)', value=0)
else:
    terrace_sqm = 0

fl_furnished_present = st.selectbox('Is the property Furnished?', ['Yes', 'No'])
if fl_furnished_present == 'Yes':
    fl_furnished = 1
else:
    fl_furnished = 0

garden_present = st.selectbox('Is there a Garden?', ['Yes', 'No'])
if garden_present == 'Yes':
    garden_sqm = st.number_input('Garden Area (sqm)', value=0)
else:
    garden_sqm = 0

primary_energy_consumption_sqm = st.number_input('Primary Energy Consumption (sqm)', value=0)
fl_open_fire = st.selectbox('Has Open Fire', ['Yes', 'No'])
fl_swimming_pool = st.selectbox('Has Swimming Pool', ['Yes', 'No'])
fl_floodzone = st.selectbox('Is in Flood Zone', ['Yes', 'No'])
fl_double_glazing = st.selectbox('Has Double Glazing', ['Yes', 'No'])
equipped_kitchen = st.selectbox('Equipped Kitchen', ['Yes', 'No'])
property_type = st.selectbox('Property Type', ['House', 'Apartment', 'Other'])

# Filter subproperty types based on selected property type
subproperty_options = data[data['property_type'] == property_type]['subproperty_type'].unique()
subproperty_type = st.selectbox('Select the type of property', subproperty_options)

region = st.selectbox('Select the region', data['region'].unique())

# Filter provinces based on selected region
provinces_options = data[data['region'] == region]['province'].unique()
province = st.selectbox('Select the province', provinces_options)

# Filter localities based on selected province
localities_options = data[(data['region'] == region) & (data['province'] == province)]['locality'].unique()
locality = st.selectbox('Select the Locality', localities_options)

# Filter zip codes based on selected locality
zip_code_options = data[(data['region'] == region) & (data['province'] == province) & (data['locality'] == locality)]['zip_code'].unique()
zip_code = st.selectbox('Select the Postal Code', zip_code_options)

state_building = st.selectbox('Building State', ['New', 'Good', 'To Renovate', 'To Restore'])
epc = st.selectbox('Energy Performance Certificate', ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
heating_type = st.selectbox('Heating Type', ['Gas', 'Fuel Oil', 'Electricity', 'Wood', 'Other'])

# Validate numeric inputs
nbr_frontages = validate_numeric_input(nbr_frontages, 'Number of Frontages')
construction_year = validate_numeric_input(construction_year, 'Construction Year')
total_area_sqm = validate_numeric_input(total_area_sqm, 'Total Area (sqm)')
surface_land_sqm = validate_numeric_input(surface_land_sqm, 'Surface Land (sqm)')
nbr_bedrooms = validate_numeric_input(nbr_bedrooms, 'Number of Bedrooms')
terrace_sqm = validate_numeric_input(terrace_sqm, 'Terrace Area (sqm)')
garden_sqm = validate_numeric_input(garden_sqm, 'Garden Area (sqm)')
primary_energy_consumption_sqm = validate_numeric_input(primary_energy_consumption_sqm, 'Primary Energy Consumption (sqm)')

# Predict button
if st.button('Predict Price'):
    # Check if any numeric input validation failed
    if None in [nbr_frontages, construction_year, total_area_sqm, surface_land_sqm, nbr_bedrooms, terrace_sqm, garden_sqm, primary_energy_consumption_sqm]:
        st.warning("Please provide valid numerical values for the input fields.")
    else:
        # Prepare input data
        input_data = {
            'nbr_frontages': nbr_frontages,
            'construction_year': construction_year,
            'total_area_sqm': total_area_sqm,
            'surface_land_sqm': surface_land_sqm,
            'nbr_bedrooms': nbr_bedrooms,
            'terrace_sqm': terrace_sqm,
            'garden_sqm': garden_sqm,
            'primary_energy_consumption_sqm': primary_energy_consumption_sqm,
            'fl_terrace': 1 if fl_terrace_present == 'Yes' else 0,
            'fl_furnished': fl_furnished,
            'fl_open_fire': 1 if fl_open_fire == 'Yes' else 0,
            'fl_garden': 1 if garden_present == 'Yes' else 0,
            'fl_swimming_pool': 1 if fl_swimming_pool == 'Yes' else 0,
            'fl_floodzone': 1 if fl_floodzone == 'Yes' else 0,
            'fl_double_glazing': 1 if fl_double_glazing == 'Yes' else 0,
            'equipped_kitchen': equipped_kitchen,
            'property_type': property_type,
            'subproperty_type': subproperty_type,
            'region': region,
            'province': province,
            'locality': locality,
            'zip_code': zip_code,
            'state_building': state_building,
            'epc': epc,
            'heating_type': heating_type
        }
        input_df = pd.DataFrame([input_data])

        # Make prediction
        prediction = predict_price(input_df)

        # Display prediction
        if prediction is not None:
            st.success(f'Predicted Price: {prediction:,.2f} EUR')
