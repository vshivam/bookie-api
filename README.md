## Project Description

Bookie API is the backend service for the [Bookie](https://github.com/adaszyn/bookie-app/) web app. 

## Done  

We have completed the following things thus far: 

- Project setup
    - [Flask](http://flask.pocoo.org/)
    - [SQLAlchemy](https://www.sqlalchemy.org/)
    - [Postgresql](https://www.postgresql.org/)
- API
    - New User Signup
    - User Login
    - User Logout 
    - Notes Creation
    - Notes Editing
    - Notes Update

## Your project file structure:

```
app/
└── models.py (database structure)
└── __init__.py (REST API definitions)

instance/
└── config.py (server configuration info)

migrations/
├── versions (migration info for database model changes)

manage.py (helper methods for database migration)

run.py (run flask server)
```

## To do
- Delete Notes
- Add tags support for Notes
- API will evolve as required by the frontend. 








