import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from model.db import db


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {"id": self.id, "type": self.type}


def get_categories():
    categories_raw = Category.query.all()
    categories = [category.format() for category in categories_raw]
    return categories
