from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import joblib
import pandas as pd

app = FastAPI(
    title="Real Estate Price Prediction API",
    description="API for predicting real estate prices based on input features.",
    version="1.0.0",
)

# Load the model artifacts using joblib
artifacts = joblib.load("models/artifacts_xg.joblib")

# Unpack the artifacts
num_features = artifacts["features"]["num_features"]
fl_features = artifacts["features"]["fl_features"]
cat_features = artifacts["features"]["cat_features"]

imputer = artifacts["imputer"]
enc = artifacts["enc"]
model = artifacts["model"]

class Item(BaseModel):
    nbr_frontages: float
    nbr_bedrooms: float
    latitude: float
    longitude: float
    total_area_sqm: float
    surface_land_sqm: float
    terrace_sqm: float
    garden_sqm: float
    fl_terrace: int
    fl_garden: int
    fl_swimming_pool: int
    province: str
    heating_type: str
    state_building: str
    property_type: str
    epc: str
    locality: str
    subproperty_type: str
    region: str
    
    class Config:
        schema_extra = {
            "example": {
                "nbr_frontages": 2.0,
                "nbr_bedrooms": 3.0,
                "latitude": 50.8503,
                "longitude": 4.3517,
                "total_area_sqm": 150.0,
                "surface_land_sqm": 200.0,
                "terrace_sqm": 20.0,
                "garden_sqm": 50.0,
                "fl_terrace": 1,
                "fl_garden": 0,
                "fl_swimming_pool": 1,
                "province": "Brussels",
                "heating_type": "GAS",
                "state_building": "GOOD",
                "property_type": "APARTMENT",
                "epc": "C",
                "locality": "Brussels",
                "subproperty_type": "APARTMENT",
                "region": "Brussels-Capital",
            }
        }

    @validator("province")
    def validate_province(cls, value):
        # List of valid provinces
        valid_provinces = ["Brussels", "Flemish", "Walloon"]

        # Check if the provided province is in the list of valid provinces
        if value not in valid_provinces:
            raise ValueError("Invalid province. Please provide a valid province.")
        return value

# Define API tags
tags_metadata = [
    {"name": "predict", "description": "Operations related to real estate price prediction."},
]

# Assign tags to the entire app
app.openapi_tags = tags_metadata

@app.post("/predict", tags=["predict"], response_description="Predicted real estate price for users")
async def predict(item: Item):
    """
    Predicts real estate prices based on input features for regular users.
    """
    try:
        # Create a DataFrame from the input data
        input_data = pd.DataFrame([item.dict()])

        # Apply preprocessing transformations
        input_data[num_features] = imputer.transform(input_data[num_features])
        input_data_cat = enc.transform(input_data[cat_features]).toarray()

        # Combine the numerical and one-hot encoded categorical columns
        input_data = pd.concat(
            [
                input_data[num_features + fl_features].reset_index(drop=True),
                pd.DataFrame(input_data_cat, columns=enc.get_feature_names_out()),
            ],
            axis=1,
        )

        prediction = model.predict(input_data)

        # Return the prediction for regular users
        return {"prediction": float(prediction[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Additional endpoint for developers
@app.post("/dev/predict", tags=["predict"], response_description="Predicted real estate price for developers")
async def predict_for_dev(item: Item):
    """
    Predicts real estate prices based on input features for developers.
    This endpoint may return additional information useful for development purposes.
    """
    try:
        # Create a DataFrame from the input data
        input_data = pd.DataFrame([item.dict()])

        # Apply preprocessing transformations
        input_data[num_features] = imputer.transform(input_data[num_features])
        input_data_cat = enc.transform(input_data[cat_features]).toarray()

        # Combine the numerical and one-hot encoded categorical columns
        input_data = pd.concat(
            [
                input_data[num_features + fl_features].reset_index(drop=True),
                pd.DataFrame(input_data_cat, columns=enc.get_feature_names_out()),
            ],
            axis=1,
        )

        prediction = model.predict(input_data)

        # Return the prediction with additional information for developers
        return {"prediction": float(prediction[0]),
                "dev_info": "Additional information for developers"
                }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
