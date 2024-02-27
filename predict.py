import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import zipfile
import os

def preprocess(data):
    # Load the model artifacts using joblib
    artifacts = joblib.load("models/artifacts.joblib")

    # Unpack the artifacts
    num_features = artifacts["features"]["num_features"]
    fl_features = artifacts["features"]["fl_features"]
    cat_features = artifacts["features"]["cat_features"]
    imputer = artifacts["imputer"]
    enc = artifacts["enc"]

    # Extract the used data
    data = data[num_features + fl_features + cat_features]

    # Apply imputer and encoder on data
    data[num_features] = imputer.transform(data[num_features])
    data_cat = enc.transform(data[cat_features]).toarray()

    # Combine the numerical and one-hot encoded categorical columns
    data = pd.concat(
        [
            data[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(data_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    return data

def predict(data):
    # Load the model artifacts using joblib
    artifacts = joblib.load("models/artifacts.joblib")
    ensemble_model = artifacts["ensemble_model"]

    # Preprocess the data
    processed_data = preprocess(data)

    # Make predictions using the ensemble model
    predictions = ensemble_model.predict(processed_data)

    return predictions
