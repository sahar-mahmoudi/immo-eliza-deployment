from fastapi import FastAPI
from pydantic import BaseModel

from app.predict import predict

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
    return {"message": "Welcome to this API"}

@app.post("/user")
def user(input: User_input):
    return predict(input)

@app.post("/dev")
def dev(input: User_input):
    return predict(input)

