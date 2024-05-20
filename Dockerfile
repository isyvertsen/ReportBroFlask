# Use an official Python runtime as a parent image
FROM python:3.11.5

RUN apt-get update && apt-get install -y curl wget
# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY ./templates /app/templates
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Make port 80 available to the world outside this container
EXPOSE 5012

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]