Developed in python using flask and postgresql. 

# Setup Info
export FLASK\_APP = "run.py" 

Enter Database Info in instance/config.py

setup, migrate, upgrade db commands:

python manage.py db init

python manage.py db migrate 

python manage.py db upgrade 

# API Supports
New user registration, login, logout. 

Per user Note creation, editing, retrieval.

# File Description
app/models.py - Database structure
app/__init__.py - REST methods

instance/config.py - Configuration info

manage.py - create, update, migrate database. 

run.py - configure and run server. 







