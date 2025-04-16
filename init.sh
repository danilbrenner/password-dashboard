#!/bin/bash

echo "1. Airflow db init"

docker compose run webserver airflow db init

echo "2. Create Password Dashboard DB"

docker compose exec postgres psql -U postgres -d postgres -c "CREATE DATABASE password_dashboard;"
docker compose exec postgres psql -U postgres -d postgres -c "CREATE DATABASE metabase;"

echo "3. Create Airflow user"

docker compose run webserver airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com