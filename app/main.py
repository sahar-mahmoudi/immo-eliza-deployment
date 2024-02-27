from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import json
import sklearn

class User_input(BaseModel):
    property_type : str
    subproperty_type : str
    region : str
    province : str
    locality : str
    zip_code : int
    latitude : float
    longitude : float
    construction_year : float
    total_area_sqm : float
    surface_land_sqm : float
    nbr_frontages : float
    nbr_bedrooms : float
    equipped_kitchen : str
    fl_furnished : int
    fl_open_fire : int
    fl_terrace : int
    terrace_sqm : float
    fl_garden : int
    garden_sqm : float
    fl_swimming_pool : int
    fl_floodzone : int
    state_building : str
    primary_energy_consumption_sqm : float
    epc : str
    heating_type : str
    fl_double_glazing : int
    cadastral_income : float

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "azerddaefazd"}

@app.post("/predict")
def predict(input: User_input):
    row_dict = {k:[v] for k, v in dict(input).items()}
    data = pd.DataFrame(row_dict)
    
    # Load the model artifacts using joblib
    artifacts = joblib.load("models/artifacts.joblib")
    
    # Unpack the artifacts
    num_features = artifacts["features"]["num_features"]
    fl_features = artifacts["features"]["fl_features"]
    cat_features = artifacts["features"]["cat_features"]
    imputer = artifacts["imputer"]
    enc = artifacts["enc"]
    model = artifacts["model"]
    scaler = artifacts["scaler"]
    
    # Extract the used data
    data = data[num_features + fl_features + cat_features]
    
    # Apply imputer and encoder on data
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
    return json.dumps(prediction)


