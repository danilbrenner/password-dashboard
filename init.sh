#!/bin/bash

echo "0. Start postgres"

docker compose up postgres -d
sleep 5

echo "1. Create Databases"

docker compose exec postgres psql -U postgres -d postgres -c "CREATE DATABASE airflow;"

echo "2. Airflow db init"

docker compose run webserver airflow db init

echo "3. Create Airflow user"

docker compose run webserver airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
