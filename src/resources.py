# (c) 2021 Yannic Breiting, Martin Kistler

from datetime import datetime
import functools
import uuid

from flask import request
from flask_restful import Resource, fields, marshal

from src.db_models import Professor, APIUser, ActiveToken, db


def needs_authorization(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')

        # No authentication provided
        if auth is None:
            return 'UNAUTHORIZED', 401, {'WWW-Authenticate': 'Bearer'}

        # wrong authentication scheme provided
        if not auth.startswith('Bearer '):
            return 'Invalid authentication scheme', 401, {'WWW-Authenticate': 'Bearer'}

        raw_token = auth.removeprefix('Bearer ')
        token = ActiveToken.query.filter_by(token=raw_token).first()

        # invalid token provided
        if token is None:
            return 'Invalid token', 401, {'WWW-Authenticate': 'Bearer'}

        # expired token provided
        if token.is_expired():
            return 'Token expired', 401, {'WWW-Authenticate': 'Bearer'}

        return function(*args, **kwargs)

    return wrapper


class LoginAPI(Resource):
    def post(self):
        if not request.is_json:
            return 'request must be of Content-Type: application/json', 401

        username = request.json.get('username')
        password = request.json.get('password')

        if username is None or password is None:
            return 'No username or password provided', 401

        if not APIUser.query.filter_by(username=username, password=password).first():
            return 'Incorrect username or password', 401

        token = str(uuid.uuid4())
        db.session.add(ActiveToken(token=token, username=username, created=datetime.now()))
        db.session.commit()

        return {'token': token}, 200


class LogoutAPI(Resource):
    @needs_authorization
    def get(self):
        token = request.headers.get('Authorization').lstrip('Bearer ')
        db.session.delete(ActiveToken.query.filter_by(token=token))
        db.session.commit()

        return 'Logout successful', 200


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

    @needs_authorization
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

    @needs_authorization
    def get(self, id):
        return {'professors': marshal(Professor.query.filter_by(id=id).first(), self.fields)}