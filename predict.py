import click
import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import zipfile
import os

@click.command()
@click.option("-i", "--input-dataset", help="Path to input .csv dataset", required=True)
@click.option("-o", "--output-dataset", default="output/predictions.csv", help="Full path where to store predictions", required=True)
@click.option("-a", "--artifacts-zip", default="models/artifacts.zip", help="Path to compressed model artifacts", required=True)
def predict(input_dataset, output_dataset, artifacts_zip):
    """Predicts house prices from 'input_dataset', stores it to 'output_dataset'."""
    # Load the data
    data = pd.read_csv(input_dataset)

    # Extract compressed artifacts
    with zipfile.ZipFile(artifacts_zip, 'r') as zip_ref:
        zip_ref.extractall('models')

    # Load the model artifacts using joblib
    artifacts = joblib.load("models/artifacts.joblib")

    # Unpack the artifacts
    num_features = artifacts["features"]["num_features"]
    fl_features = artifacts["features"]["fl_features"]
    cat_features = artifacts["features"]["cat_features"]
    imputer = artifacts["imputer"]
    enc = artifacts["enc"]
    ensemble_model = artifacts["ensemble_model"]

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

    # Make predictions using the ensemble model
    predictions = ensemble_model.predict(data)

    # Save predictions to a CSV file
    pd.DataFrame({"predictions": predictions}).to_csv(output_dataset, index=False)

    # Print success messages
    click.echo(click.style("Predictions generated successfully!", fg="green"))
    click.echo(f"Saved to {output_dataset}")
    click.echo(
        f"Nbr. observations: {data.shape[0]} | Nbr. predictions: {predictions.shape[0]}"
    )

if __name__ == "__main__":
    predict()
