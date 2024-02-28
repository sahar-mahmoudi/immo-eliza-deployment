# immo-eliza-deployment
![python version](https://img.shields.io/badge/python-v3.12.1-green?logo=python) ![build version](https://img.shields.io/badge/build-v0.42-blue)

# Mission
This repository contains the codebase for a real estate prediction system developed for real estate company Immo Eliza. The system includes a regression model for predicting property prices, an API for accessing predictions programmatically, and a web application for easy user access.

# Project Structure

- ``app/models/artifacts.joblib``: Contains the model artifacts.
- ``app/predict.py``: Contains the code to run the prediction.
- ``app/main.py``: Includes the FastAPI code for building the API endpoints.
- ``app/frontend.py``: Holds the Streamlit code for the web application interface.
- ``Dockerfile``: The Dockerfile for containerizing the API.
- ``LICENSE``: License information for the repository.

# Setup Instructions:

Clone the repository to your local machine:
```bash
git clone https://github.com/sahar-mahmoudi/real-estate-prediction.git
```

Navigate to the project directory:
```bash
cd real-estate-prediction
```

Setup the environment:
```bash
pip install -r requirements.txt
```

Build Docker image:
```bash
docker build -t image_name .
```

Run the Docker container:
```bash
docker run -d --name container_name -p 8000:8000 image_name
```

# Deploy the web application:
Deploy the Streamlit web application on Streamlit Community Cloud.

# Usage:
Access the API endpoints to make predictions programmatically.
Access the web application interface to interactively explore property predictions.

# License:
This project is licensed under the MIT License. See the LICENSE file for details.