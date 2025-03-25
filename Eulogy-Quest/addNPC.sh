#!/bin/bash

# check for filename provided
# $1 is the first argument on the command line
# $0 is the command used to run this script
if [ -z "$1" ]; then
  echo "Usage: $0 <file_name.sql>"
  exit 1
fi

# append to file path, for altering if we change our structure
# and so usage only requires filename
SQL_FILE="./npc/$1"

# Safety check if file was found
if [ ! -f "$SQL_FILE" ]; then
  echo "Error: File '$SQL_FILE' not found in npc directory."
  exit 1
fi

# Taken from /akk-stack/Makefile
# I tracked down where the passwords are stored so they can be grabbed without having to enter them
MARIADB_ROOT_PASSWORD=$(grep 'MARIADB_ROOT_PASSWORD' ../.env | cut -d '=' -f2)
MARIADB_DATABASE=$(grep 'MARIADB_DATABASE' ../.env | cut -d '=' -f2)

# Safety check if passwords were grabbed
if [[ -z "$MARIADB_ROOT_PASSWORD" || -z "$MARIADB_DATABASE" ]]; then
  echo "Error: Could not find database credentials in .env file."
  exit 1
fi

# Taken from /akk-stack/Makefile
# Used to enter the mariaDB database console
# The script enters this console and runs the SQL file there
cat "$SQL_FILE" | docker-compose exec -T mariadb bash -c "mysql -uroot -p${MARIADB_ROOT_PASSWORD} -h localhost ${MARIADB_DATABASE}"

# $? holds exit status of above command nonzero is an error
if [ $? -ne 0 ]; then
    echo "Failed to add into database"
    exit 1
fi

echo "$1 successfully added to database."
