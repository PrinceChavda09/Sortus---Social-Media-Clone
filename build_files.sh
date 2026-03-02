#!/bin/bash
# Install dependencies
python3.12 -m pip install -r requirements.txt

# Gather all CSS/JS files into the STATIC_ROOT folder
python3.12 manage.py collectstatic --noinput --clear