from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

database_path = "postgresql://postgres@localhost:5432/trivia"

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
