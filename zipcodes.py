import pandas as pd


zipcodes = pd.read_csv('zipcodes.csv')
zip = zipcodes.drop(zipcodes.columns[0], axis=1).reindex()

def get_lat(zipcode):
    lat = zipcodes[zipcodes['zip_code'] == zipcode]['latitude']
    return lat.values[0]

def get_long(zipcode):
    long = zipcodes[zipcodes['zip_code'] == zipcode]['longitude']
    return long.values[0]

def get_province(zipcode):
    province = zipcodes[zipcodes['zip_code'] == zipcode]['province']
    return province.values[0]

def get_region(zipcode):
    region = zipcodes[zipcodes['zip_code'] == zipcode]['region']
    return region.values[0]
