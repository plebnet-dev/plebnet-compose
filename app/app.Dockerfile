# Use an official Python runtime as a base image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir dash plotly psycopg2-binary flask pandas SQLAlchemy


# Make port 8050 available to the world outside this container
EXPOSE 8050

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
