# Install all packages from your requirements.txt
pip install -r requirements.txt

# Create the static folder and move your CSS there
python3.12 manage.py collectstatic --noinput --clear