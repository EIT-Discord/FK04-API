# (c) 2021 Yannic Breiting, Martin Kistler

from src.app import db
from src.db_models import APIUser


def new_api_user(username: str, password: str):
    new_user = APIUser(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()


if __name__ == '__main__':
    new_api_user('eitbot', '1234')
