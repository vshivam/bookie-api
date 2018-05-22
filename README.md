## Project Description

Bookie API is the backend service for the [Bookie](https://github.com/adaszyn/bookie-app/) web app. 

## Done  

- Project setup
    - [Flask](http://flask.pocoo.org/)
    - [SQLAlchemy](https://www.sqlalchemy.org/)
    - [Postgresql](https://www.postgresql.org/)
- API
    - New User Signup
    - User Login
    - User Logout 
    - Note Creation
    - Note Editing
    - Note Update
    - Note Delete
    - Manage Note Tags
    - Upload Images
    - Book Delete
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
