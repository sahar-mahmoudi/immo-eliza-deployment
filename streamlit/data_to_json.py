import pandas as pd 
import json

data = pd.read_csv('properties.csv')
char_columns = data.select_dtypes(include='object').columns

unique_values_json = {}
for column in char_columns:
    unique_values_json[column] = data[column].unique().tolist()
with open ('uniques.json', 'w') as outfile:
    json.dump(unique_values_json, outfile)
# Format keys in the desired way and replace "MISSING" with "not available"
formatted_unique_values_json = {}
for key, values in unique_values_json.items():
    formatted_values = ['Not available' if value == 'MISSING' else value.replace('_', ' ').capitalize() for value in values]
    formatted_unique_values_json[key] = formatted_values

# Print formatted values for 'property_type'
print(formatted_unique_values_json['equipped_kitchen'])
with open ('uniques_formatted.json', 'w') as outfile:
    json.dump(formatted_unique_values_json, outfile)