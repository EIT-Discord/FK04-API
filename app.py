from flask import Flask
from flask_restful import Api, Resource, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
print(PROJECT_ROOT)

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PROJECT_ROOT}/data.sqlite'
db = SQLAlchemy(app)


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


class ProfessorsAPI(Resource):
    fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'address': fields.String,
        'room': fields.String,
        'description': fields.String,
        'imageUrl': fields.String,
        'moodleCourses': fields.String,
        'uri': fields.Url('professor', absolute=True),

    }

    def get(self):
        return {'professors': marshal(Professor.query.all(), self.fields)}


class ProfessorAPI(Resource):
    fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'phone': fields.String,
        'address': fields.String,
        'room': fields.String,
        'description': fields.String,
        'moodleCourses': fields.String,
        'imageUrl': fields.String,
        'uri': fields.Url('professor', absolute=True)
    }

    def get(self, id):
        return {'professors': marshal(Professor.query.filter_by(id=id).first(), self.fields)}


# Endpoint configuration
api.add_resource(ProfessorsAPI, '/api/professors', endpoint='professors')
api.add_resource(ProfessorAPI, '/api/professors/<int:id>', endpoint='professor')

if __name__ == '__main__':
    db.create_all()
