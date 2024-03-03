import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load the dataset
@st.cache
def load_data():
    df = pd.read_csv('Dataanalysis/properties.csv')
    # Drop the "ID" column
    df.drop(columns=['id'], inplace=True)
    # Capitalize column names
    df.columns = df.columns.str.capitalize()
    return df

# Function to clean the data
def clean_data(df):
    # Drop duplicate rows
    df = df.drop_duplicates()
    # Fill missing values with "None"
    df = df.fillna("None")
    # Filter out rows where the 'Price' and 'Total_area_sqm' columns don't contain 'None'
    df = df[(df['Price'] != 'None') & (df['Total_area_sqm'] != 'None')]
    return df

# Function to display introduction section
def display_introduction(df):
    st.title('Welcome to Data Analysis')
    st.write('This is an interactive data analysis tool where you can explore the price distribution of properties in Belgium.')
    st.image('Dataanalysis/Belgium_properties.png', caption='Properties in Belgium', use_column_width=True)

    # Additional text
    st.write("""
    This tool allows you to analyze the price distribution of properties in Belgium based on different features such as region, province, locality, and number of bedrooms.
    
    You can use the navigation panel on the left to explore various sections of the app, including:
    
    - **Price Distribution Analysis:** Analyze the price distribution based on selected features.
    - **Dataset Dashboard:** Explore the dataset and select features for analysis.
    - **KPIs:** View key performance indicators.
    - **KDE Plot:** View Kernel Density Estimate plot for price distribution.
    - **Summary & Price Prediction:** Get a summary of analysis and predict property prices using machine learning models.
    """)

    # Display total number of properties
    total_properties = len(df)
    st.write(f"Total number of properties in Belgium: {total_properties}")

    # Display types of properties
    property_types = df['Property_type'].unique()
    st.write("Types of properties:")
    for prop_type in property_types:
        st.write(f"- {prop_type}")

    # Display sub-properties for each property type
    for prop_type in property_types:
        sub_properties = df[df['Property_type'] == prop_type]['Subproperty_type'].unique()
        st.write(f"Sub-properties for {prop_type}:")
        for sub_prop in sub_properties:
            st.write(f"  - {sub_prop}")

# Function to analyze price distribution by a specific feature
def analyze_price_by_feature(df, feature):
    st.subheader(f'Price Distribution by {feature.capitalize()}')
    
    # Filter out rows where the feature values are "MISSING"
    df = df[df[feature] != "MISSING"]
    
    # Group by the selected feature and calculate median price
    median_price = df.groupby(feature)['Price'].median().reset_index()
    
    # Plot the distribution
    fig, ax = plt.subplots()
    sns.barplot(x=feature, y='Price', data=median_price, ax=ax)
    plt.xlabel(feature.capitalize())
    plt.ylabel("Price")
    plt.title(f'Price Distribution by {feature.capitalize()}')
    st.pyplot(fig)
    
    # Explain the plot interactively
    explanation = f"The bar plot above shows the median price distribution across different {feature.lower()}s.\n\n"
    explanation += "Here are some insights:\n"
    explanation += f"- The {feature.lower()} with the highest median price is {median_price.loc[median_price['Price'].idxmax(), feature]}.\n"
    explanation += f"- The {feature.lower()} with the lowest median price is {median_price.loc[median_price['Price'].idxmin(), feature]}.\n"
    explanation += f"- The price difference between the highest and lowest median prices is {median_price['Price'].max() - median_price['Price'].min()}.\n"
    
    st.write(explanation)

# Function to analyze price distribution
def analyze_price_distribution(df, features):
    st.title("Price Distribution Analysis")
    
    # Sidebar options
    selected_features = st.sidebar.multiselect("Select Features", features)
    
    # Check if no features are selected
    if not selected_features:
        st.warning("Please select at least one feature for analysis.")
        return
    
    # Filter data based on selected options and remove rows with explicitly mentioned missing values
    df_filtered = df.copy()
    for feature in selected_features:
        df_filtered = df_filtered[df_filtered[feature] != "MISSING"]
        if feature == "Number of bedrooms":
            selected_bedrooms = st.sidebar.slider('Number of Bedrooms', min_value=1, max_value=5)
            df_filtered = df_filtered[df_filtered['Nbr_bedrooms'] == selected_bedrooms]
        else:
            selected_items = st.sidebar.multiselect(f"Select {feature}", df[feature].unique())
            df_filtered = df_filtered[df_filtered[feature].isin(selected_items)]
    
    # Display data count after applying filters
    st.write(f"Data Count after Filtering: {len(df_filtered)}")

    # Check if any valid data remains after filtering
    if df_filtered.empty:
        st.warning("No data available after filtering. Please adjust your selection.")
        return

    # Analyze price distribution based on selected options
    for feature in selected_features:
        analyze_price_by_feature(df_filtered, feature)


# Function to divide features into numerical and categorical
def divide_features(df):
    numerical_features = ["Nbr_frontages", "Construction_year", "Total_area_sqm", "Surface_land_sqm", "Nbr_bedrooms", "Terrace_sqm", "Garden_sqm", "Primary_energy_consumption_sqm"]
    fl_features = ["Fl_terrace", "Fl_furnished", "Fl_open_fire", "Fl_garden", "Fl_swimming_pool", "Fl_floodzone", "Fl_double_glazing"]
    cat_features = ["Equipped_kitchen", "Property_type", "Subproperty_type", "Region", "Province", "Locality", "State_building", "Epc", "Heating_type"]
    return numerical_features, fl_features, cat_features

# Function to display analysis for selected features with box plots
def display_feature_analysis(df, selected_features):
    if selected_features:
        for feature in selected_features:
            st.subheader(f"Analysis for {feature.capitalize()}")

            # Display box plot with hue
            st.write(f"### Box Plot for {feature.capitalize()}")
            hue_feature = st.selectbox(f"Select Hue Feature for {feature.capitalize()} Box Plot", ['Price', 'Region', 'Province', 'Locality'])
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x=feature, y='Price', hue=hue_feature, data=df, ax=ax)
            plt.xlabel(feature.capitalize())
            plt.ylabel("Price")
            plt.title(f"Box Plot for {feature.capitalize()} with Hue {hue_feature}")
            st.pyplot(fig)

            # Explain the plot interactively
            explanation = f"The box plot above shows the distribution of prices across different {feature.lower()} categories.\n\n"
            explanation += f"- Each box represents the interquartile range (IQR) of prices for a specific {feature.lower()} category.\n"
            explanation += f"- The whiskers extend to the minimum and maximum prices, excluding outliers.\n"
            explanation += f"- The hue feature ({hue_feature.lower()}) provides additional insights by categorizing the data.\n"
            
            st.write(explanation)

# Function to calculate KPIs by region, province, and locality
def calculate_kpis(df, feature):
    # Filter out rows where the feature values are "MISSING"
    df = df[df[feature] != "MISSING"]
    
    # Group data by the selected feature and calculate KPIs for each group
    kpis = df.groupby(feature)['Price'].agg(['count', 'mean', 'median', 'max', 'min']).reset_index()
    return kpis

# Function to display KPIs
def display_kpis(kpis):
    st.subheader("Key Performance Indicators")
    st.write(kpis)

# Function to display KDE plot for price distribution
def display_kde_plot(df):
    st.title("Kernel Density Estimate (KDE) Plot")

    # Allow user to select the numerical feature for analysis
    numerical_feature = st.selectbox("Select Numerical Feature", df.select_dtypes(include=['float64', 'int64']).columns.tolist())

    # Allow user to select the feature to use as hue (price levels)
    hue_feature = st.selectbox("Select Feature for Hue", ['Price', 'Region', 'Province', 'Locality'])

    # Create KDE plot
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(data=df, x=numerical_feature, hue=hue_feature, shade=True, ax=ax)
    plt.xlabel(numerical_feature.capitalize())
    plt.ylabel("Density")
    plt.title(f"KDE Plot for {numerical_feature.capitalize()} with Hue {hue_feature}")
    st.pyplot(fig)
    
    # Explain the plot interactively
    explanation = f"The KDE plot above shows the distribution of {numerical_feature.lower()} with respect to {hue_feature.lower()}.\n\n"
    explanation += f"- The plot illustrates how the distribution of {numerical_feature.lower()} changes across different levels of {hue_feature.lower()}.\n"
    explanation += f"- The shaded areas represent the density of {numerical_feature.lower()} values.\n"
    
    st.write(explanation)

# Function for Summary & Price Prediction
def predict_prices(df):
    st.title("Recap & Predictive Modeling")

      # Summary
    st.header("Summary of Analysis")
    st.write("Here is a summary of the analysis performed:")

    st.write("- Explored the distribution of property prices based on various features such as region, province, locality, and number of bedrooms.")
    st.write("- Identified key factors influencing property prices, including total area, number of bedrooms, and presence of amenities such as terrace and garden.")
    st.write("- Investigated the relationship between price and categorical features like property type, subproperty type, and state of the building.")
    st.write("- Calculated key performance indicators (KPIs) such as count, mean, median, max, and min prices by region, province, and locality.")

    # List of machine learning models for price prediction
    st.header("Machine Learning Models for Price Prediction")
    st.write("Below are some of the commonly used machine learning models for predicting property prices:")

    st.subheader("1. Linear Regression")
    st.write("Linear Regression is a simple and commonly used algorithm for predicting numeric values. It works by fitting a linear relationship between the independent variables and the target variable.")

    st.subheader("2. Random Forest Regression")
    st.write("Random Forest is an ensemble learning method that operates by constructing a multitude of decision trees at training time and outputs the mean prediction of the individual trees as the final prediction.")

    st.subheader("3. Support Vector Regression (SVR)")
    st.write("Support Vector Regression is an extension of Support Vector Machines (SVM) for regression tasks. It works by mapping the input features into a higher-dimensional space where a linear relationship is sought.")

    st.subheader("4. XGBoost")
    st.write("XGBoost is an efficient and scalable implementation of gradient boosting algorithms. It is highly flexible and provides state-of-the-art results on a wide range of problems.")

    st.subheader("5. Lasso Regression")
    st.write("Lasso Regression, or Least Absolute Shrinkage and Selection Operator, is a linear regression technique that performs both variable selection and regularization to improve the prediction accuracy and interpretability of the model.")

    # Additional information
    st.header("Additional Information")
    st.write("While these are some of the commonly used models, there are many other algorithms such as Gradient Boosting, Neural Networks, and LSTMs that can also be used for price prediction tasks.")

    st.write("It's essential to preprocess the data, handle missing values, encode categorical variables, and perform feature scaling before training the models to achieve better performance.")

    st.write("Furthermore, model performance can be evaluated using metrics such as Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R-squared.")

# Main function
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ('Introduction', 'Price Distribution Analysis', 'Dataset Dashboard', 'KPIs', 'KDE Plot', 'Summary & Price Prediction'))

    # Load the data
    df = load_data()
    df = clean_data(df)

    if page == 'Introduction':
        display_introduction(df)

    elif page == 'Price Distribution Analysis':
        # Get list of available features
        features = ["Region", "Province", "Locality", "Nbr_bedrooms"]
        
        # Analyze price distribution
        analyze_price_distribution(df, features)

    elif page == 'Dataset Dashboard':
        st.title("Dataset Dashboard")

        # Display options to select features for analysis
        st.write("### Select Features for Analysis")
        numerical_features, fl_features, cat_features = divide_features(df)
        selected_numerical_features = st.multiselect("Select Numerical Features", numerical_features)
        selected_fl_features = st.multiselect("Select Boolean Features", fl_features)
        selected_categorical_features = st.multiselect("Select Categorical Features", cat_features)

        # Display analysis for selected features
        if selected_numerical_features or selected_fl_features or selected_categorical_features:
            if selected_numerical_features:
                st.subheader("Numerical Features Analysis")
                display_feature_analysis(df, selected_numerical_features)
            if selected_fl_features:
                st.subheader("Boolean Features Analysis")
                display_feature_analysis(df, selected_fl_features)
            if selected_categorical_features:
                st.subheader("Categorical Features Analysis")
                display_feature_analysis(df, selected_categorical_features)

    elif page == 'KPIs':
        st.title("Key Performance Indicators")

        # Calculate and display KPIs by selected feature
        selected_feature = st.selectbox("Select Feature", ["Region", "Province", "Locality"])
        kpis = calculate_kpis(df, selected_feature)
        display_kpis(kpis)

    elif page == 'KDE Plot':
        # Display KDE plot for price distribution
         display_kde_plot(df)

    elif page == 'Recap & Predictive Modeling':
        # Summary and Price Prediction
        predict_prices(df)

if __name__ == "__main__":
    main()
