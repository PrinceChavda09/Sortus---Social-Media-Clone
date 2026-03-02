# Install dependencies
pip install -r requirements.txt

# This command moves your 'static/style.css' into the 'staticfiles_build' folder
python3.12 manage.py collectstatic --noinput --clear