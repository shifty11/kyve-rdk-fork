# Use the official Python image as the base image
FROM python:3.12

ARG VERSION

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt ./

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python code and protobuf files to the container
COPY main.py settings.py ./
COPY proto ./proto
COPY server ./server

# Update the version in the settings.py file
RUN sed -i "s/RUNTIME_VERSION = '.*'/RUNTIME_VERSION = '$VERSION'/" settings.py

# Expose the gRPC port
EXPOSE 50051

# Set the command to run when the container starts
CMD ["python", "-u", "main.py"]
