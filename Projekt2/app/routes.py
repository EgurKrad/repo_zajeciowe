from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from app.models import Animal
from app import db
import random
from werkzeug.utils import secure_filename
import os
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from app.models import User
from functools import wraps
from flask import abort
import unicodedata
from rapidfuzz import process, fuzz

main = Blueprint("main", __name__)

WEIGHT_ORDER = [
    "<1g",
    "1g-15g",
    "15g-50g",
    "50g-1kg",
    "1kg-10kg",
    "10kg-30kg",
    "30kg-100kg",
    "100kg-500kg",
    ">500kg"
]

SIZE_ORDER = [
    "<5cm",
    "5cm-20cm",
    "20cm-50cm",
    "50cm-100cm",
    "100cm-300cm",
    ">300cm"
]

HABITAT_ENUM = [
    "ocean",
    "morze",
    "rzeka",
    "jezioro",
    "las",
    "góry",
    "pustynia",
    "sawanna",
    "dżungla",
    "bagna",
    "tundra",
    "łąka"
]

CATEGORIES = [
    "ryba",
    "pajęczak",
    "owad",
    "gad",
    "płaz",
    "ssak",
    "ptak",
    "mięczak"
]

WEIGHT_ENUM = [
    "<1g",
    "1g-15g",
    "15g-50g",
    "50g-1kg",
    "1kg-10kg",
    "10kg-30kg",
    "30kg-100kg",
    "100kg-500kg",
    ">500kg"
]

SIZE_ENUM = [
    "<5cm",
    "5cm-20cm",
    "20cm-50cm",
    "50cm-100cm",
    "100cm-300cm",
    ">300cm"
]

def compare_enum(guess, target, order):
    guess_index = order.index(guess)
    target_index = order.index(target)

    if guess_index < target_index:
        return "↑ za małe"
    elif guess_index > target_index:
        return "↓ za duże"

    return "✓ idealnie"


def compare_habitats(guess, target):
    guess_set = set(guess.split(","))
    target_set = set(target.split(","))

    if guess_set == target_set:
        return "Zgadza się"
    elif guess_set & target_set:
        return "Częściowo"
    return "Nie zgadza się"


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

def normalize_text(text: str) -> str:
    return text.strip().lower()

# Autoryzacja
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Do kolorowania
def get_status_class(value):
    if value in ["Zgadza się", "✓ idealnie"]:
        return "status-correct"

    if value == "Częściowo":
        return "status-partial"

    return "status-wrong"

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/game", methods=["GET", "POST"])
def game():
    animals = Animal.query.all()

    if not animals:
        return "Brak zwierząt w bazie"

    # losowanie zwierzęcia na sesję
    if "animal_id" not in session:
        random_animal = random.choice(animals)
        session["animal_id"] = random_animal.id

    target = Animal.query.get(session["animal_id"])

    # historia prób
    if "attempts" not in session:
        session["attempts"] = []

    hint = None

    if request.method == "POST":
        guess_raw = request.form["guess"]
        guess_name = normalize_text(guess_raw)

        # FUZZY SEARCH
        best_match = process.extractOne(
            guess_name,
            [normalize_text(a.name) for a in animals],
            scorer=fuzz.WRatio
        )

        guessed = None
        score = 0
        matched_name = None

        if best_match:
            matched_name, score, _ = best_match

            guessed = next(
                (a for a in animals if normalize_text(a.name) == matched_name),
                None
            )

        if not guessed:
            hint = {
                "error": f"{guess_raw} - nie ma takiego zwierzęcia"
            }

        else:
            # jeśli fuzzy match jest słaby
            if score < 80:
                hint = {
                    "error": f"{guess_raw} - nie ma takiego zwierzęcia"
                }

            # wygrana
            elif normalize_text(guessed.name) == normalize_text(target.name):
                session.pop("attempts", None)
                return redirect(url_for("main.win"))

            else:
                hint = {
                    "category": guessed.category == target.category,
                    "habitat": compare_habitats(
                        guessed.habitats,
                        target.habitats
                    ),
                    "weight": compare_enum(
                        guessed.weight,
                        target.weight,
                        WEIGHT_ORDER
                    ),
                    "size": compare_enum(
                        guessed.size,
                        target.size,
                        SIZE_ORDER
                    )
                }

                # zapis próby
                attempt = {
                    "name": guessed.name,

                    "category": (
                        "✓" if hint["category"] else "✗"
                    ),
                    "category_class": (
                        "status-correct"
                        if hint["category"]
                        else "status-wrong"
                    ),

                    "habitat": hint["habitat"],
                    "habitat_class": get_status_class(hint["habitat"]),

                    "weight": hint["weight"],
                    "weight_class": get_status_class(hint["weight"]),

                    "size": hint["size"],
                    "size_class": get_status_class(hint["size"])
                }

                session["attempts"].append(attempt)
                session.modified = True

    return render_template(
        "game.html",
        hint=hint,
        attempts=session["attempts"]
    )

@main.route("/win")
def win():
    animal = Animal.query.get(session["animal_id"])
    # Czyszczenie sesji po wygranej
    session.pop("animal_id", None)
    session.pop("attempts", None)

    return render_template("win.html", animal=animal)

@main.route("/add-animal", methods=["GET", "POST"])
@login_required
def add_animal():
    if request.method == "POST":
        name = normalize_text(request.form["name"])

        existing_animal = Animal.query.filter(
            Animal.name.ilike(name)
        ).first()

        if existing_animal:
            return render_template(
                "add_animal.html",
                error=f"Zwierzę '{name}' już istnieje w bazie"
            )

        category = request.form["category"]
        weight = request.form["weight"]
        size = request.form["size"]

        habitats = request.form.getlist("habitats")
        habitats_str = ",".join(habitats)

        image = request.files.get("image")

        filename = "placeholder.png"

        if image and image.filename != "":
            if allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(
                    os.path.join(
                        current_app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )



        animal = Animal(
            name=name,
            category=category,
            weight=weight,
            size=size,
            habitats=habitats_str,
            image_filename=filename
        )

        db.session.add(animal)
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template(
        "add_animal.html",
        categories=CATEGORIES,
        weights=WEIGHT_ENUM,
        sizes=SIZE_ENUM,
        habitats=HABITAT_ENUM
    )

@main.route("/animals")
def animals():
    animals_list = Animal.query.all()
    return render_template(
        "animals.html",
        animals=animals_list
    )

@main.route("/delete-animal/<int:animal_id>")
def delete_animal(animal_id):
    if session.get("role") != "admin":
        return "Brak uprawnień"

    animal = Animal.query.get_or_404(animal_id)

    db.session.delete(animal)
    db.session.commit()

    return redirect(url_for("main.animals"))

@main.route(
    "/edit-animal/<int:animal_id>",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)

    if request.method == "POST":
        animal.name = normalize_text(request.form["name"])
        animal.category = request.form["category"]
        animal.weight = request.form["weight"]
        animal.size = request.form["size"]

        habitats = request.form.getlist("habitats")
        animal.habitats = ",".join(habitats)

        image = request.files.get("image")

        if image and image.filename:
            filename = secure_filename(image.filename)
            image_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
            image.save(image_path)
            animal.image_filename = filename

        db.session.commit()

        return redirect(url_for("main.animals"))

    return render_template(
        "edit_animal.html",
        animal=animal,
        categories=CATEGORIES,
        weights=WEIGHT_ENUM,
        sizes=SIZE_ENUM,
        habitats=HABITAT_ENUM
    )

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return "Taki użytkownik już istnieje"

        hashed_password = generate_password_hash(password)

        role = "admin" if username == "admin" else "user"

        user = User(
            username=username,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("main.login"))

    return render_template("register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:
            return "Nie ma takiego użytkownika"

        if not check_password_hash(
            user.password,
            password
        ):
            return "Błędne hasło"

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        return redirect(url_for("main.index"))

    return render_template("login.html")

@main.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))








# Własne errory
@main.app_errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@main.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500