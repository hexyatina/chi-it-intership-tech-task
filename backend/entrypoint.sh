#!/bin/bash
while ! nc -z db 5432; do
  sleep 1
done
echo "db is ready"

python creating_users.py

uvicorn main:app --host 0.0.0.0 --port 8000