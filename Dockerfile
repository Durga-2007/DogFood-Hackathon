FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application source
COPY src/ /app/src/

# Copy fixtures
COPY data/fixtures.json /app/data/fixtures.json

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Data volume for SQLite database
VOLUME ["/app/data"]

EXPOSE 8080

ENV DATABASE_URL=sqlite:////app/data/dogfood.db
ENV FIXTURES_PATH=/app/data/fixtures.json

ENTRYPOINT ["/entrypoint.sh"]
