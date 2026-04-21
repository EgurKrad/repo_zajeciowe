from app import db
from enum import Enum

class WeightCategory(Enum):
    BELOW_1G = "<1g"
    FROM_1_TO_15G = "1g-15g"
    FROM_15_TO_50G = "15g-50g"
    FROM_50G_TO_1KG = "50g-1kg"
    FROM_1_TO_10KG = "1kg-10kg"
    FROM_10_TO_30KG = "10kg-30kg"
    FROM_30_TO_100KG = "30kg-100kg"
    FROM_100_TO_500KG = "100kg-500kg"
    ABOVE_500KG = ">500kg"

class SizeCategory(Enum):
    BELOW_5CM = "<5cm"
    FROM_5_TO_20CM = "5cm-20cm"
    FROM_20_TO_50CM = "20cm-50cm"
    FROM_50_TO_100CM = "50cm-100cm"
    FROM_100_TO_300CM = "100cm-300cm"
    ABOVE_300CM = ">300cm"

class Habitat(Enum):
    FOREST = "las"
    OCEAN = "ocean"
    MOUNTAINS = "góry"
    DESERT = "pustynia"
    SAVANNA = "sawanna"

class AnimalCategory(Enum):
    FISH = "ryba"
    ARACHNID = "pajęczak"
    INSECT = "owad"
    REPTILE = "gad"
    AMPHIBIAN = "płaz"
    MAMMAL = "ssak"
    BIRD = "ptak"

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