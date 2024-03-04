import click
import joblib
import pandas as pd


# python predict.py -i data/properties.csv -o output/predictions.csv
# or python predict.py -i C:\Users\admin\Desktop\Model-deployment\data\properties.csv -o C:\Users\admin\Desktop\Model-deployment\output\predictions.csv
@click.command()
@click.option("-i", "--input-dataset", help="path to input .csv dataset", required=True)
@click.option(
    "-o",
    "--output-dataset",
    default="output/predictions.csv",
    help="full path where to store predictions",
    required=True,
)
def predict(input_dataset, output_dataset):
    """Predicts house prices from 'input_dataset', stores it to 'output_dataset'."""
    ### -------- DO NOT TOUCH THE FOLLOWING LINES -------- ###
    # Load the data
    data = pd.read_csv(input_dataset)
    ### -------------------------------------------------- ###

    # Load the model artifacts using joblib
    artifacts = joblib.load("models/artifacts.joblib")

    # Unpack the artifacts
    num_features = artifacts["features"]["num_features"]
    fl_features = artifacts["features"]["fl_features"]
    cat_features = artifacts["features"]["cat_features"]
    imputer = artifacts["imputer"]
    enc = artifacts["enc"]
    models = artifacts["models"]

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

    # Make predictions with each model
    predictions = {}
    for name, model in models.items():
        predictions[name] = model.predict(data)
        predictions[name] = predictions[name][:10]  # just picking 10 to display sample output :-)

    ### -------- DO NOT TOUCH THE FOLLOWING LINES -------- ###
    # Save the predictions to a CSV file (in order of data input!)
    for name, pred in predictions.items():
        pd.DataFrame({f"{name}_predictions": pred}).to_csv(f"output/{name}_predictions.csv", index=False)

    # Print success messages
    click.echo(click.style("Predictions generated successfully!", fg="green"))
    for name, pred in predictions.items():
        click.echo(f"{name} predictions saved to output/{name}_predictions.csv")
    click.echo(
        f"Nbr. observations: {data.shape[0]} | Nbr. predictions: {predictions[name].shape[0]}"
    )
    ### -------------------------------------------------- ###


if __name__ == "__main__":
    # how to run on command line:
    # python .\predict.py -i "data\input.csv" -o "output\predictions.csv"
    predict()