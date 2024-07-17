# First stage: Python environment setup
FROM python:3.9-slim as python-build

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for Python environment
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy your application files
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Second stage: PostgreSQL environment setup
FROM postgres:latest as postgres-build

# Install system dependencies for PostgreSQL and pgvector
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-all \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN git clone --branch v0.7.2 https://github.com/pgvector/pgvector.git

WORKDIR /pgvector
RUN make && make install

# Clean up installation artifacts
RUN apt-get remove --purge -y \
    git \
    postgresql-server-dev-all \
    build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/pgvector

# Final stage: combining Python and PostgreSQL setups
FROM python:3.9-slim

# Copy Python environment from python-build
COPY --from=python-build /app /app
WORKDIR /app

# Copy PostgreSQL binaries from postgres-build (if necessary, adjust as per your needs)
# This is a placeholder as you might need to manually configure paths or shared libraries

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
