# (c) 2021 Yannic Breiting, Martin Kistler
from datetime import datetime, timedelta

from src.app import db

DB_STRING_SIZE = 100
TOKEN_LIFETIME = timedelta(seconds=20)


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(DB_STRING_SIZE))
    email = db.Column(db.String(DB_STRING_SIZE))
    phone = db.Column(db.String(DB_STRING_SIZE))
    fax = db.Column(db.String(DB_STRING_SIZE))
    address = db.Column(db.String(DB_STRING_SIZE))
    room = db.Column(db.String(DB_STRING_SIZE))
    description = db.Column(db.String(10*DB_STRING_SIZE))
    moodleCourses = db.Column(db.String(DB_STRING_SIZE))
    imageUrl = db.Column(db.String(2*DB_STRING_SIZE))

    def __repr__(self):
        return self.name


class APIUser(db.Model):
    username = db.Column(db.String(DB_STRING_SIZE), primary_key=True)
    password = db.Column(db.String(DB_STRING_SIZE))


class ActiveToken(db.Model):
    token = db.Column(db.String(DB_STRING_SIZE), primary_key=True)
    username = db.Column(db.String(DB_STRING_SIZE))
    created = db.Column(db.DateTime)

    def is_expired(self) -> bool:
        return datetime.now()-self.created > TOKEN_LIFETIME
