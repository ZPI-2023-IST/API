# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Repos urls
ARG GAME="git+https://github.com/ZPI-2023-IST/FreeCell.git"
ARG TRANSLATOR="git+https://github.com/ZPI-2023-IST/Translator.git"

# Install git
RUN apt-get update && \
    apt-get install -y git

# Downloand game and translator from git

RUN pip3 install --upgrade pip

RUN pip3 install $GAME
RUN pip3 install $TRANSLATOR

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5002 available to the world outside this container
EXPOSE 5002

# Run app.py when the container launches
CMD ["python3", "main.py"]
