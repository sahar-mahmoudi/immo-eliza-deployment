# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run your FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
