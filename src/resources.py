import uuid

from flask import request
from flask_restful import Resource, fields, marshal

from src.db_models import Professor, APIUser, ActiveToken, db


def need_authorization(function):
    def authorization(*args, **kwargs):
        auth = request.headers.get('Authorization')

        if auth is None:
            return {'message': 'UNAUTHORIZED'}, 401

        if not auth.startswith('Bearer '):
            return {'message': 'Invalid authentication scheme'}, 401

        token = auth.lstrip('Bearer ')

        if not ActiveToken.query.filter_by(token=token).first():
            return {'message': 'Invalid token'}, 401

        return function(*args, **kwargs)

    return authorization


class LoginAPI(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if username is None or password is None:
            return {'message': 'No username or password provided'}, 401

        if not APIUser.query.filter_by(username=username, password=password).first():
            return {'message': 'Incorrect username or password'}, 401

        token = str(uuid.uuid4())
        db.session.add(ActiveToken(token=token, username=username))
        db.session.commit()

        return {'token': token}


class LogoutAPI(Resource):
    @need_authorization
    def get(self):
        token = request.headers.get('Authorization').lstrip('Bearer ')
        db.session.delete(ActiveToken.query.filter_by(token=token))
        db.session.commit()

        return {'message': 'Logout successful'}


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