# Use an official Python runtime as a parent image
FROM python:3.11-slim

#Create the working directory
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY . /app


# Make port 8080 available to the world outside this container
EXPOSE 8080


# Run app.py when the container launches
CMD ["python", "app.py"]
