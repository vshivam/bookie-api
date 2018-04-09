from app import db

class Notes(db.model):
  """ This class represents the Notes table"""
  __tablename__="notes"

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer)
  book_id = db.Column(db.Integer)
  content = db.Column(db.String)
  date_created = db.Column(db.DateTime, db.func.currenr_timestamp())
  date_modified = db.Column(
    dbDateTime, default=db.func.current_timestamp(), 
    onupdate=db.func.current_timestamp()) 
