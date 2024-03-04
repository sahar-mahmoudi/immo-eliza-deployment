import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import xgboost as xgb
import numpy as np


# Load the data
data = pd.read_csv("data/properties.csv")

# Define features to use
num_features = ["nbr_frontages", 'nbr_bedrooms',"latitude", "longitude", "total_area_sqm",
                    'surface_land_sqm','terrace_sqm','garden_sqm', 'primary_energy_consumption_sqm']
fl_features = ["fl_terrace", 'fl_garden', 'fl_swimming_pool', 'fl_furnished', 'fl_open_fire', 'fl_floodzone', 'fl_double_glazing']
cat_features = ["province", 'heating_type', 'state_building',
                "property_type", "epc", 'locality', 'subproperty_type','region', 'equipped_kitchen']

# Split the data into features and target
X = data[num_features + fl_features + cat_features]
y = data["price"]

# Split the data into training and testing sets with stratification
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

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

# Use the best parameters found during RandomizedSearchCV
best_params = {
    'n_estimators': 130,
    'max_depth': 10,
    'learning_rate': 0.3,
    'subsample': 0.9,
    'colsample_bytree': 1.0,
    'gamma': 5,
    'reg_alpha': 1.5,
    'reg_lambda': 1.0,
}

# Train the final model using the best parameters
final_model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42, **best_params)
final_model.fit(X_train, y_train)

# Predict on training and test data
y_train_pred = final_model.predict(X_train)
y_test_pred = final_model.predict(X_test)

# Calculate R2 score
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

# Calculate RMSE
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

# Calculate MAE
train_mae = mean_absolute_error(y_train, y_train_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)

print("Training R2 score:", train_r2)
print("Test R2 score:", test_r2)
print("Training RMSE:", train_rmse)
print("Test RMSE:", test_rmse)
print("Training MAE:", train_mae)
print("Test MAE:", test_mae)

# Extract feature importance
feature_importance = final_model.feature_importances_

    # Get the names of the features
feature_names = X_train.columns

    # Sort feature importance in descending order
sorted_indices = np.argsort(feature_importance)[::-1]

    # Print feature importance scores with corresponding names
print("Feature Importance Scores:")
for i, idx in enumerate(sorted_indices):
        print(f"{i+1}. Feature '{feature_names[idx]}': {feature_importance[idx]}")

    # Select top N features
top_n = 15  # Change this to select a different number of top features
top_features = sorted_indices[:top_n]

print("\nTop", top_n, "Features:")
for i, idx in enumerate(top_features):
        print(f"{i+1}. Feature '{feature_names[idx]}'")


# Create a dictionary mapping feature names to importances
feature_importance_dict = dict(zip(num_features, feature_importance))

# Sort features and importances
sorted_features_numeric = [x[0] for x in sorted(zip(num_features, feature_importance[:len(num_features)]), key=lambda x: x[1])]
sorted_importances_numeric = [x[1] for x in sorted(zip(num_features, feature_importance[:len(num_features)]), key=lambda x: x[1], reverse=True)]

# Plot the feature importances for numeric features
plt.figure(figsize=(10, 6))
plt.barh(range(len(num_features)), sorted_importances_numeric)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importances for Numeric Features')

# Assign custom names to the bars
custom_feature_names = ["Total area in sqm", "Latitude", 'Bedrooms Nos',  "Longitude","Frontage Nos", 'Primary energy consumption for sqm', 
                        'Surface land in sqm', 'Terrace area in sqm', 'Garden area in sqm', 
                         ]
plt.yticks(range(len(num_features)), custom_feature_names)


plt.savefig("Plot/fig1.png", dpi=600)
plt.show()

# Create a dictionary mapping feature names to importances
feature_importance_dict = dict(zip(fl_features, feature_importance))

# Sort the dictionary by importances in descending order
# sorted_features = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

# Extract feature names and importances for plotting
# features = [x[0] for x in sorted_features]
# importances = [x[1] for x in sorted_features]

# Plot the feature importances for flag features
plt.figure(figsize=(10, 6))
plt.barh(features, importances)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importances for Flag Features')

# Assign custom names to the bars
custom_feature_names = ['Open fire space', 'Swimming pool','Furnished',  'Non floodzone', 'Garden',  
                         'Double glazing',"Terrace",]
plt.yticks(range(len(fl_features)), custom_feature_names)

plt.savefig("Plot/fig2.png", dpi=600)  # Save fig2 here
plt.show()


