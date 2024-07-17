#!/bin/bash

# Fetch credentials from environment variables
DB_USERNAME=${DB_USERNAME}
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=${DB_NAME}
DB_HOST=${DB_HOST:-localhost}  # Default to localhost if DB_HOST is not set

# Check if variables are set
if [ -z "$DB_USERNAME" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_NAME" ]; then
    echo "Environment variables DB_USERNAME, DB_PASSWORD, or DB_NAME are not set!"
    exit 1
fi

# Export the PGPASSWORD variable so that psql does not prompt for password
export PGPASSWORD=$DB_PASSWORD
export POSTGRES_PASSWORD=$DB_PASSWORD

# Add the pgvector extension
psql -h $DB_HOST -U $DB_USERNAME -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Unset the PGPASSWORD variable
unset PGPASSWORD