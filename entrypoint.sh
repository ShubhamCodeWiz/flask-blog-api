#!/bin/sh

# This script is the entrypoint for the Docker container.
# It runs database migrations and then starts the Gunicorn server.

echo "Running database migrations..."
# Run the database upgrade command.
flask db upgrade

echo "Starting Gunicorn server..."
# Start the Gunicorn server.
# The 'exec' command is important because it replaces the shell process with the gunicorn process,
# which allows signals to be passed correctly.
exec gunicorn --workers 3 --bind 0.0.0.0:8000 wsgi:app