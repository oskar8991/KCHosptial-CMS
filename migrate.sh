#!/usr/bin/env bash
# Author Edouard Azoulai
# This script allows you to add data to a heroku postgresql database.
# The data needs to be in csv files in a separate data folder.
# For each csv file starting with "add-", the script will try to add to a table
# with the same name as the csv file (excluding the add- prefix and extension).
# It will use the csv header to describe the rows affected for each table.
# There needs to be one row per line per file.

APP_NAME=williwaller

for table in data/add-*.csv; do
    t=${table#data/add-}
    t=${t%.csv}
    echo "Adding $t to the database."
    header=$(head -n 1 $table)
    echo $header
    cat $table | psql `heroku config:get DATABASE_URL --app $APP_NAME` -c "COPY $t($header) FROM STDIN DELIMITER ',' CSV HEADER;" &&
    mv $table data/$t.csv # Removes prefix if the data was added to the db.
done