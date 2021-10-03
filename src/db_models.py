from app import db


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    fax = db.Column(db.String(100))
    address = db.Column(db.String(100))
    room = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    moodleCourses = db.Column(db.String(100))
    imageUrl = db.Column(db.String(200))

    def __repr__(self):
        return self.name


class APIUser(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))


class ActiveToken(db.Model):
    token = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100))
