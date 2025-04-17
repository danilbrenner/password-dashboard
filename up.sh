#!/bin/bash

echo "1. Start postgres"

docker compose up postgres -d

sleep 3

echo "2. Create Password Dashboard DB"

docker compose exec postgres psql -U postgres -d postgres -c "CREATE DATABASE password_dashboard;"
docker compose exec postgres psql -U postgres -d postgres -c "CREATE DATABASE metabase;"

echo "3. Up!"

docker compose up --build  # -d
