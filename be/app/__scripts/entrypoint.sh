#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."
until nc -z -v -w30 db 5432; do
    echo "Waiting for db:5432..."
    sleep 5
done
    echo "PostgreSQL is up - Running migrations..."
    ./__scripts/migrations.sh up

# App run
if [ "$PYTHON_ENV" = "development" ]; then
    echo "Starting the app in development mode..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --log-level trace --use-colors --reload
elif [ "$PYTHON_ENV" = "worker" ]; then
    echo "Starting worker..."
    celery -A worker.celery_app worker -l info
elif [ "$PYTHON_ENV" = "beat" ]; then
    echo "Starting beat..."
    rm -f celerybeat.pid
    celery -A worker.celery_app beat -l info
else
    echo "Invalid PYTHON_ENV."
fi

exec "$@"
