import datetime

from app import db
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import uuid
import json


@login_manager.user_loader
def load_user(session_token):
    user = User.query.filter(User.session_token == str(session_token)).first()
    if user is not None:
        return user
    else:
        return None


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    session_token = db.Column(db.String(128))

    def __init__(self, email):
        self.email = email
        self.session_token = str(uuid.uuid4())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.session_token

    # We don't need inactive users
    def is_active(self):
        return True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Note(db.Model):
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Text)
    content = db.Column(db.String)
    is_fav = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_modified = db.Column(
        db.DateTime, default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    def __init__(self, user_id, book_id, content, is_fav, tags):
        self.user_id = user_id
        self.book_id = book_id
        self.content = content
        self.is_fav = is_fav
        self.tags = tags

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_response_object(self):
        return {
            'id': self.id,
            'bookId': self.book_id,
            'content': self.content,
            'isFav': self.is_fav,
            'tags': json.loads(self.tags) if self.tags is not None else [],
            'dateCreated': self.date_created,
            'dateModified': self.date_modified
        }

    def __repr__(self):
        return "<Notes {}>".format(self.content)
