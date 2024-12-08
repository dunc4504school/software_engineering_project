#### EXPLANATION::

#### RUNNING THE PROJECT


### Setup
# Clone This Repo To The Folder Of Your Choice
# Enter Command Line
# Run: "psql -U postgres"
# Enter your (postgres) password
# Run: "CREATE DATABASE cp317_final"
# Run: "\c cp317_final"
# Paste: db.sql
# Run: "SET CLIENT_ENCODING TO 'UTF8';"

### Import Data
# Within frontend.py and full_setup.py replace the default database credentials with the one you just created
# Run: python full_setup.py
# Note: the database should be filled with the extracted data at this point

### Run Program
# Run: streamlit run frontend.py


