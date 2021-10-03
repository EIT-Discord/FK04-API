# (c) 2021 Yannic Breiting, Martin Kistler

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PROJECT_ROOT}/data.sqlite'
db = SQLAlchemy(app)


# Resources must be importet AFTER creation of the db object, to avoid a circular import
# see https://stackoverflow.com/a/31016384
from src.resources import ProfessorsAPI, ProfessorAPI, LoginAPI

# Endpoint configuration
api.add_resource(ProfessorsAPI, '/api/professors', endpoint='professors')
api.add_resource(ProfessorAPI, '/api/professors/<int:id>', endpoint='professor')
api.add_resource(LoginAPI, '/api/login', endpoint='login')
