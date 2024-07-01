# !/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies from requirements.txt
pip install -r requirements.txt
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

