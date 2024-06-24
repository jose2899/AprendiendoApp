<<<<<<< HEAD
=======

>>>>>>> 4c68cd389380f1a6b534ba9774d968c0752d8a81
# !/usr/bin/env bash
# Exit on error
set -o errexit

# Upgrade pip and setuptools
pip install --upgrade pip setuptools

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Apply database migrations
<<<<<<< HEAD
python manage.py migrate
=======
python manage.py migrate
>>>>>>> 4c68cd389380f1a6b534ba9774d968c0752d8a81
