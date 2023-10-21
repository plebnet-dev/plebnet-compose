# Use an official Python runtime as a base image
FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y gcc python3-dev

# Set the working directory
WORKDIR /usr/src/app

COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Make port 8050 available to the world outside this container
EXPOSE 8050


# Run app.py when the container launches
CMD ["python", "app.py"]

