from app import db, APIUser


def new_api_user(username: str, password: str):
    new_user = APIUser(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
