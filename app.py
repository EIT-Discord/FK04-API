import uuid

from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PROJECT_ROOT}/data.sqlite'
db = SQLAlchemy(app)


def need_authorization(function):
    def authorization(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if auth is None:
            return {'message': 'UNAUTHORIZED'}, 401

        if not auth.startswith('Bearer '):
            return {'message': 'Invalid authentication scheme'}, 401

        token = auth.lstrip('Bearer ')

        if not ActiveToken.query.filter_by(token=token).first():
            return {'message': 'Invalid token provided'}, 401

        return function(*args, **kwargs)

    return authorization


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
    userame = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))


class ActiveToken(db.Model):
    token = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100))


class LoginAPI(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if username is None or password is None:
            return {'message': 'No username or password provided with request.'}, 401

        if not APIUser.query.filter_by(username=username, password=password).first():
            return {'message': 'Incorrect username or password.'}, 401

        token = str(uuid.uuid4())
        db.session.add(ActiveToken(token=token, username=username))
        db.session.commit()

        return {'token': token}


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

    @need_authorization
    def get(self):
        name = request.args.get('name')

        if name is not None:
            return {'professors': marshal(Professor.query.filter(Professor.name.contains(name)).all(), self.fields)}

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

    @need_authorization
    def get(self, id):
        return {'professors': marshal(Professor.query.filter_by(id=id).first(), self.fields)}


# Endpoint configuration
api.add_resource(ProfessorsAPI, '/api/professors', endpoint='professors')
api.add_resource(ProfessorAPI, '/api/professors/<int:id>', endpoint='professor')
api.add_resource(ProfessorAPI, '/api/login', endpoint='login')


if __name__ == '__main__':
    db.create_all()
