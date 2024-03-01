import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('Dataanalysis/properties.csv')

# Function to analyze price distribution by a specific feature
def analyze_price_by_feature(df, feature):
    st.subheader(f'Price Distribution by {feature.capitalize()}')
    
    # Filter out rows where the feature values are "MISSING"
    df = df[df[feature.lower()] != "MISSING"]
    
    # Group by the selected feature and calculate median price
    median_price = df.groupby(feature)['price'].median().reset_index()
    
    # Plot the distribution
    fig = px.bar(median_price, x=feature, y='price', color='price', title=f'Price Distribution by {feature.capitalize()}')
    
    # Capitalize axis labels and legends
    fig.update_layout(xaxis_title=feature.capitalize(), yaxis_title="Price", legend_title="Price")
    
    st.plotly_chart(fig)
    
    # Explain the plot interactively
    explanation = f"The bar plot above shows the median price distribution across different {feature}s.\n\n"
    explanation += "Here are some insights:\n"
    explanation += f"- The {feature.lower()} with the highest median price is {median_price.loc[median_price['price'].idxmax(), feature]}.\n"
    explanation += f"- The {feature.lower()} with the lowest median price is {median_price.loc[median_price['price'].idxmin(), feature]}.\n"
    explanation += f"- The price difference between the highest and lowest median prices is {median_price['price'].max() - median_price['price'].min()}.\n"
    
    st.write(explanation)

# Function to analyze price distribution
def analyze_price_distribution(df, features):
    st.title("Price Distribution Analysis")
    
    # Sidebar options
    selected_features = st.sidebar.multiselect("Select Features", features)
    
    # Filter data based on selected options
    df_filtered = df.copy()
    for feature in selected_features:
        if feature == "Number of Bedrooms":
            selected_bedrooms = st.sidebar.slider('Number of Bedrooms', min_value=1, max_value=5)
            df_filtered = df_filtered[df_filtered['nbr_bedrooms'] == selected_bedrooms]
        else:
            selected_items = st.sidebar.multiselect(f"Select {feature}", df[feature].unique())
            df_filtered = df_filtered[df_filtered[feature].isin(selected_items)]
    
    # Display data count after applying filters
    st.write(f"Data Count after Filtering: {len(df_filtered)}")
    
    # Display map with filtered points
    display_map(df_filtered)
    
    # Analyze price distribution based on selected options
    if selected_features:
        for feature in selected_features:
            analyze_price_by_feature(df_filtered, feature)

# Function to display the map
def display_map(df):
    st.header("Map")
    view_state = pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=8
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=['longitude', 'latitude'],
        get_radius=100,
        get_fill_color=[255, 165, 0],
        pickable=True,
        tooltip={"text": "Price: {price}, Bedrooms: {nbr_bedrooms}, Region: {region}, Locality: {locality}, Province: {province}"},
    )

    map = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state
    )

    st.pydeck_chart(map)

# Main function
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ('Introduction', 'Price Distribution Analysis'))

    if page == 'Introduction':
        st.title('Welcome to Data Analysis')
        st.write('This is an interactive data analysis tool where you can explore the price distribution of properties.')
        
        # Load the data
        df = load_data()
        
        # Display map with all points
        display_map(df)

    elif page == 'Price Distribution Analysis':
        st.title("Price Distribution Analysis")
        
        # Load the data
        df = load_data()
        
        # Get list of available features
        features = ["region", "province", "locality", "nbr_bedrooms"]
        
        # Analyze price distribution
        analyze_price_distribution(df, features)

if __name__ == "__main__":
    main()
