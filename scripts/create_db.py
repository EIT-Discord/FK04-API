# (c) 2021 Yannic Breiting, Martin Kistler

from src.app import db


if __name__ == '__main__':
    db.create_all()
