# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy all contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Define environment variable to run FastAPI
ENV MODULE_NAME="api" \
    VARIABLE_NAME="app" \
    HOST="0.0.0.0" \
    PORT=8000

# Command to run your application using uvicorn
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--reload", "${MODULE_NAME}:${VARIABLE_NAME}"]
