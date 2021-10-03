from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PROJECT_ROOT}/data.sqlite'
db = SQLAlchemy(app)


# Endpoint configuration
from src.resources import ProfessorsAPI, ProfessorAPI, LoginAPI

api.add_resource(ProfessorsAPI, '/api/professors', endpoint='professors')
api.add_resource(ProfessorAPI, '/api/professors/<int:id>', endpoint='professor')
api.add_resource(LoginAPI, '/api/login', endpoint='login')
