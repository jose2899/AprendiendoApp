#!/usr/bin/env bash
# exit on error*-
set -o errexit

#poetry install
pip install --upgrade pip
pip install --force-reinstall -U setuptools
pip install --upgrade pippip install --force-reinstall -U setuptools
pip install -r requirements.txt
python manage.py migrate
