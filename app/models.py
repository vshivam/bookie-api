import datetime

from app import db


class Note(db.Model):
    """ This class represents the Notes table"""
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    content = db.Column(db.String)
    is_fav = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_modified = db.Column(
        db.DateTime, default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    def __init__(self, user_id, book_id, content, is_fav):
        self.user_id = user_id
        self.book_id = book_id
        self.content = content
        self.is_fav = is_fav

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Notes {}>".format(self.id)
