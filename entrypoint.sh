#!/bin/bash
set -e

# Execute database upgrades
python manage.py db upgrade

# Exec the container's main process (what's set as CMD in the Dockerfile).
exec "$@"
