# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

FROM postgres:latest

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-all \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git

WORKDIR /tmp/pgvector
RUN make
RUN make install

# Clean up
RUN apt-get remove --purge -y \
    git \
    postgresql-server-dev-all \
    build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /pgvector

# Upgrade pip
RUN pip install --upgrade pip

# Copy your application's requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

