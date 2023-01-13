#!/bin/sh

echo "Waiting for ElasticSearch..."

while ! nc -z $ELS_HOST $ELS_PORT; do
  sleep 0.1
done

echo "ElasticSearch started"

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

while true
do
    echo "Starting load_data_els"
    python main.py
    sleep 3600
done
