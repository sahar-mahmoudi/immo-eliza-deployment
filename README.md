# Real Estate Price Predictor

This is a Streamlit web application designed to predict the price range of real estate properties based on various features provided by the user. The application employs a machine learning model deployed as an API to make predictions. Users are guided through a series of steps to input property details, and the application then uses these inputs to predict the price range.

## Usage

Access the App: Navigate to https://immoelizapredict.streamlit.app/ to access the application.

Using the App: Follow the instructions provided by the application to input property details at each step. Once all details are provided, click on the "Predict!" button to initiate the prediction process and view the predicted price range.

## Technical Details

### Core Technologies

Streamlit: The application's user interface is built using Streamlit, a Python library that simplifies the creation of interactive web applications.

Session State Management: Streamlit's built-in session state management feature is utilized to persist data across different pages of the application.

Custom Zipcodes Library: A custom-made library is used to fetch location details such as latitude, longitude, region, and province based on the provided zip code.

## Application Structure

### Location Input (location.py)

Collects location details such as zip code and locality from the user.
Loads unique property data from JSON files to populate dropdown menus and sliders.
Coordinates can optionally be set using the provided map.

### Exterior Features Input (exterior.py)

Gathers exterior features including living space area, terrace, garden, etc., from the user.
Handles boolean features such as terrace, garden, and swimming pool by calculating integer values.

### Interior Features Input (interior.py)

Captures interior features like the number of bedrooms, kitchen equipment, building condition, etc., from the user.

### Energy Features Input (energy.py)

Acquires energy-related features such as EPC class and heating type from the user.

### Prediction (predict.py)

Collects all input features from previous steps and prepares them for prediction.
Utilizes the custom zipcodes library to fetch location details.
Sends input data to the prediction API endpoint via HTTP POST request and displays the predicted price range upon receiving the response.

### Author

[Maarten Knaepen](https://github.com/MaartenKnaepen)