#!/bin/bash

DB_USER="gatimu"
DB_PASS="gatimu"
DB_NAME="url_db1"

# Create the database
psql -U postgres -c "CREATE DATABASE $DB_NAME;"

# Create the user and grant privileges
psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;"