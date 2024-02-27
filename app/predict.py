import joblib
import pandas as pd
import sklearn

def predict(input):
    row_dict = {k:[v] for k, v in dict(input).items()}
    data = pd.DataFrame(row_dict)
    
    # Load and unpack the model
    artifacts = joblib.load("app/models/artifacts.joblib")
    
    num_features = artifacts["features"]["num_features"]
    fl_features = artifacts["features"]["fl_features"]
    cat_features = artifacts["features"]["cat_features"]
    imputer = artifacts["imputer"]
    enc = artifacts["enc"]
    model = artifacts["model"]
    scaler = artifacts["scaler"]
    
    # Extract the used data
    data = data[num_features + fl_features + cat_features]
    
    # Apply imputer, scaler and encoder on data
    data[num_features] = imputer.transform(data[num_features])
    data[num_features] = scaler.transform(data[num_features])
    data_cat = enc.transform(data[cat_features]).toarray()
    
    # Combine the numerical and one-hot encoded categorical columns
    data = pd.concat(
        [
            data[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(data_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )
    
    prediction = {"price": model.predict(data)[0]}
    return prediction