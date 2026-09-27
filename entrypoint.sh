#!/bin/sh
set -e

# Run seed if database is fresh or forced
python /app/src/seed.py

# Start the web server
exec uvicorn main:app --host 0.0.0.0 --port 8080 --app-dir /app/src
