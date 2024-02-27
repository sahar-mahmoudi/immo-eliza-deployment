import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, IsolationForest, VotingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
import numpy as np
import matplotlib.pyplot as plt

def train():
    # Load the data
    data = pd.read_csv("data/properties.csv")

    # Define features to use
    num_features = ["nbr_frontages", "construction_year", "total_area_sqm", "surface_land_sqm", "nbr_bedrooms", "terrace_sqm", "garden_sqm", "primary_energy_consumption_sqm"]
    fl_features = ["fl_terrace", "fl_furnished", "fl_open_fire", "fl_garden", "fl_swimming_pool", "fl_floodzone", "fl_double_glazing"]
    cat_features = ["equipped_kitchen", "property_type", "subproperty_type", "region", "province", "locality", "state_building", "epc", "heating_type"]

    # Impute missing values using SimpleImputer
    imputer = SimpleImputer(strategy="mean")
    data[num_features] = imputer.fit_transform(data[num_features])

    # One-hot encoding for categorical features
    enc = OneHotEncoder(handle_unknown='ignore')
    encoded_data = enc.fit_transform(data[cat_features]).toarray()
    cat_feature_names = enc.get_feature_names_out()
    encoded_df = pd.DataFrame(encoded_data, columns=cat_feature_names)

    # Combine encoded categorical features with numerical and flag features
    X = pd.concat([data[num_features + fl_features].reset_index(drop=True), encoded_df], axis=1)
    y = data["price"]


    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=505)

    # Train the random forest regressor model
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Train XGboost
    XG_model = XGBRegressor()
    XG_model.fit(X_train, y_train)

    # Create an ensemble of models
    ensemble_model = VotingRegressor([('random_forest', rf_model), ('xgboost', XG_model)])
    ensemble_model.fit(X_train, y_train)

    # Evaluate the ensemble model
    train_ensemble_score = r2_score(y_train, ensemble_model.predict(X_train))
    test_ensemble_score = r2_score(y_test, ensemble_model.predict(X_test))
    train_rmse = mean_squared_error(y_train, ensemble_model.predict(X_train), squared=False)
    test_rmse = mean_squared_error(y_test, ensemble_model.predict(X_test), squared=False)
    train_mae = mean_absolute_error(y_train, ensemble_model.predict(X_train))
    test_mae = mean_absolute_error(y_test, ensemble_model.predict(X_test))

    print("\nEnsemble Model (Random Forest + XGBoost):")
    print(f"Train R² score: {train_ensemble_score}")
    print(f"Test R² score: {test_ensemble_score}")
    print("Train RMSE:", train_rmse)
    print("Test RMSE:", test_rmse)
    print("Train MAE:", train_mae)
    print("Test MAE:", test_mae)

    # Save the ensemble model
    artifacts = {"ensemble_model": ensemble_model, "features": {"num_features": num_features, "fl_features": fl_features, "cat_features": cat_features}, "imputer": imputer, "enc": enc}
    joblib.dump(artifacts, "models/artifacts.joblib")

    # Predict on the test set for the ensemble model
    #y_pred_ensemble = ensemble_model.predict(X_test)

    # Plot the predictions for the ensemble model
    #plt.scatter(y_test, y_pred_ensemble, color='blue')
    #plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    #plt.title("Ensemble Model: Actual vs Predicted Prices")
    #plt.xlabel('Actual Prices')
    #plt.ylabel('Predicted Prices')
    #plt.show()

if __name__ == "__main__":
    train()
