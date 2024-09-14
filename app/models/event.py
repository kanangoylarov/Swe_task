# app/models/event.py

from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)  # Store image path

    def __repr__(self):
        return f'<Event {self.title}>'
