#!/bin/bash

sleep 10

echo "Running initial execution..."
python3 /app/flow/password_etl.py

echo "Starting cron..."
cron -f
