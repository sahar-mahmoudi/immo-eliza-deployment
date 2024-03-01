from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator, Field
import joblib
import pandas as pd

app = FastAPI(
    title="Real Estate Price Prediction API",
    description="API for predicting real estate prices based on input features.",
    version="1.0.0",
)

# Load the model artifacts using joblib
artifacts = joblib.load("api/models/artifacts_xg.joblib")

# Unpack the artifacts
num_features = artifacts["features"]["num_features"]
fl_features = artifacts["features"]["fl_features"]
cat_features = artifacts["features"]["cat_features"]

imputer = artifacts["imputer"]
enc = artifacts["enc"]
model = artifacts["model"]

class Item(BaseModel):
    nbr_frontages: float = Field(..., example=2.0)
    nbr_bedrooms: float = Field(..., example=3.0)
    latitude: float = Field(..., example=50.8503)
    longitude: float = Field(..., example=4.3517)
    total_area_sqm: float = Field(..., example=150.0)
    surface_land_sqm: float = Field(..., example=200.0)
    terrace_sqm: float = Field(..., example=20.0)
    garden_sqm: float = Field(..., example=50.0)
    fl_terrace: int = Field(..., example=1)
    fl_garden: int = Field(..., example=0)
    fl_swimming_pool: int = Field(..., example=1)
    province: str = Field(..., example="Brussels")
    heating_type: str = Field(..., example="GAS")
    state_building: str = Field(..., example="GOOD")
    property_type: str = Field(..., example="APARTMENT")
    epc: str = Field(..., example="C")
    locality: str = Field(..., example="Brussels")
    subproperty_type: str = Field(..., example="APARTMENT")
    region: str = Field(..., example="Brussels-Capital")

    # @validator("province")
    # def validate_province(cls, value):
    #     # List of valid provinces
    #     valid_provinces = ["Brussels", "Flemish", "Walloon"]

    #     # Check if the provided province is in the list of valid provinces
    #     if value not in valid_provinces:
    #         raise ValueError("Invalid province. Please provide a valid province.")
    #     return value

# Define API tags
tags_metadata = [
    {"name": "predict", "description": "Operations related to real estate price prediction."},
]

# Assign tags to the entire app
app.openapi_tags = tags_metadata

# New route at the root path
@app.get("/")
async def read_root():
    return {"message": "alive"}

@app.post("/predict", tags=["predict"], response_description="Predicted real estate price range")
async def predict(item: Item):
    """
    Predicts real estate prices based on input features.

    **How to use:**
    - Provide input features in the request body.
    - Ensure that the input features are valid.

    **Example Usage:**
    ```json
    {
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
      "region": "Brussels-Capital"
    }
    ```

    **Responses:**
    - 200 OK: Returns the predicted real estate price range.
    - 500 Internal Server Error: If an error occurs during prediction.
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

        # Make predictions
        prediction = model.predict(input_data)

        # Define price range
        
        # Calculate lower and upper bounds based on the percentage
        lower_bound = prediction - (prediction * (5 / 100))
        upper_bound = prediction + (prediction * (5 / 100))

        # Return the price range
        return {"price_range": {"lower_bound": "{:,.0f}".format(int(lower_bound[0])), "upper_bound":  "{:,.0f}".format(int(upper_bound[0]))}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
