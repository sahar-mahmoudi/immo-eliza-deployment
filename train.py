import joblib
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import Lasso
from sklearn.ensemble import VotingRegressor
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
import seaborn as sns
import matplotlib.pyplot as plt


def train():
    """Trains a linear regression model on the full dataset and stores output."""
    # Load the data
    data = pd.read_csv("data/properties.csv")

    # Define features to use
    num_features = ["construction_year", "nbr_frontages", 'nbr_bedrooms',"latitude", "longitude", "total_area_sqm",
                        "surface_land_sqm", "terrace_sqm", "garden_sqm", "primary_energy_consumption_sqm"]
    fl_features = ['fl_terrace', 'fl_garden', 'fl_swimming_pool', 'fl_furnished', 'fl_open_fire', 'fl_floodzone', 'fl_double_glazing']
    cat_features = ['province', 'heating_type', 'state_building',
                    "property_type", "epc", 'locality', 'subproperty_type','region', 'equipped_kitchen']

    # Split the data into features and target
    X = data[num_features + fl_features + cat_features]
    y = data["price"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=505
    )

    # Impute missing values using SimpleImputer
    imputer = SimpleImputer(strategy="mean")
    imputer.fit(X_train[num_features])
    X_train[num_features] = imputer.transform(X_train[num_features])
    X_test[num_features] = imputer.transform(X_test[num_features])

    # Convert categorical columns with one-hot encoding using OneHotEncoder
    enc = OneHotEncoder()
    enc.fit(X_train[cat_features])
    X_train_cat = enc.transform(X_train[cat_features]).toarray()
    X_test_cat = enc.transform(X_test[cat_features]).toarray()

    # Combine the numerical and one-hot encoded categorical columns
    X_train = pd.concat(
        [
            X_train[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(X_train_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    X_test = pd.concat(
        [
            X_test[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(X_test_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    # Train the models
    linear_model = LinearRegression()
    lasso_model = Lasso(alpha=0.1, max_iter=10000)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    xgb_model = XGBRegressor(objective='reg:squarederror',
                                n_estimators=130,
                                max_depth=10,
                                learning_rate=0.3,
                                subsample=0.9,
                                colsample_bytree=1.0,
                                gamma=5,
                                reg_alpha=1.5,
                                reg_lambda=1.0,
                                random_state=42)

    models = {
        "Linear Regression": linear_model,
        "Lasso Regression": lasso_model,
        "Random Forest Regression": rf_model,
        "XGBoost Regression": xgb_model
    }

    # Train and evaluate models
    results_train = {}
    results_test = {}
    for name, model in models.items():
    # Fit the model
        model.fit(X_train, y_train)
    
    # Predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
    
    # Evaluate metrics
        r2_train = r2_score(y_train, y_train_pred)
        rmse_train = mean_squared_error(y_train, y_train_pred, squared=False)
        mae_train = mean_absolute_error(y_train, y_train_pred)
        
        r2_test = r2_score(y_test, y_test_pred)
        rmse_test = mean_squared_error(y_test, y_test_pred, squared=False)
        mae_test = mean_absolute_error(y_test, y_test_pred)
        
        results_train[name] = {"R2": r2_train, "RMSE": rmse_train, "MAE": mae_train}
        results_test[name] = {"R2": r2_test, "RMSE": rmse_test, "MAE": mae_test}

    # Print results for training data
        print("Results for Training Data:")
        for name, result in results_train.items():
            print(f"{name}:")
            print(f"R2: {result['R2']}")
            print(f"RMSE: {result['RMSE']}")
            print(f"MAE: {result['MAE']}")
            print()

        # Print results for test data
        print("Results for Test Data:")
        for name, result in results_test.items():
            print(f"{name}:")
            print(f"R2: {result['R2']}")
            print(f"RMSE: {result['RMSE']}")
            print(f"MAE: {result['MAE']}")
            print()

        if __name__ == "__main__":
            train()