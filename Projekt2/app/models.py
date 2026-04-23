from app import db
from enum import Enum

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)

    weight = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)

    habitats = db.Column(db.String(255), nullable=False)

    image_filename = db.Column(
        db.String(255),
        nullable=True,
        default="placeholder.png"
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="user"
    )
