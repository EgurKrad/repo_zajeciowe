import pytest
import sys
import os
from flask import Flask

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app import db
from app.models import Animal, User


def create_test_app():
    # Test app z bazą w pamięci, aby nie wpływał na prawdziwą bazę
    # Ustawienie ścieżek do template'ów i static files
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["UPLOAD_FOLDER"] = "app/static/images"
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    return app


@pytest.fixture
def client():
    app = create_test_app()

    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()

            animal = Animal(
                name="Wilk",
                category="ssak",
                weight="10kg-30kg",
                size="50cm-100cm",
                habitats="las",
                image_filename="placeholder.png"
            )

            db.session.add(animal)
            db.session.commit()

        yield test_client
        
        # Cleanup po teście — czyszczenie i usunięcie wszystkich danych
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200

def test_register_user(client):
    response = client.post(
        "/register",
        data={
            "username": "marek",
            "password": "1234"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

def test_add_animal(client):
    response = client.post(
        "/add-animal",
        data={
            "name": "Lis",
            "category": "ssak",
            "weight": "1kg-10kg",
            "size": "20cm-50cm",
            "habitats": "las"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

def test_404_page(client):
    response = client.get("/nie-ma-takiej-strony")

    assert response.status_code == 404

def test_game_page(client):
    response = client.get("/game")

    assert response.status_code == 200

# Testy jednostkowe dla modeli

def test_animal_creation(client):
    with client.application.app_context():
        animal = Animal(
            name="Lew",
            category="ssak",
            weight="100kg-500kg",
            size="100cm-300cm",
            habitats="sawanna",
            image_filename="lion.jpg"
        )
        db.session.add(animal)
        db.session.commit()
        
        saved_animal = Animal.query.filter_by(name="Lew").first()
        assert saved_animal is not None
        assert saved_animal.category == "ssak"
        assert saved_animal.weight == "100kg-500kg"

def test_animal_unique_name(client):
    """Test unikalności nazwy zwierzęcia."""
    with client.application.app_context():
        animal1 = Animal(
            name="Tygrys",
            category="ssak",
            weight="100kg-500kg",
            size="100cm-300cm",
            habitats="las",
            image_filename="tiger.jpg"
        )
        db.session.add(animal1)
        db.session.commit()
        
        animal2 = Animal(
            name="Tygrys",  # Ta sama nazwa
            category="ssak",
            weight="50g-1kg",
            size="50cm-100cm",
            habitats="ocean",
            image_filename="tiger2.jpg"
        )
        db.session.add(animal2)
        try:
            db.session.commit()
            assert False, "Powinien wystąpić błąd unikalności"
        except Exception as e:
            assert "UNIQUE constraint failed" in str(e) or "unique" in str(e).lower()
            db.session.rollback()

def test_user_creation(client):
    with client.application.app_context():
        user = User(
            username="testuser",
            password="hashedpassword123",
            role="admin"
        )
        db.session.add(user)
        db.session.commit()
        
        saved_user = User.query.filter_by(username="testuser").first()
        assert saved_user is not None
        assert saved_user.role == "admin"
        assert saved_user.password == "hashedpassword123"

def test_user_unique_username(client):
    with client.application.app_context():
        user1 = User(
            username="uniqueuser",
            password="pass1",
            role="user"
        )
        db.session.add(user1)
        db.session.commit()
        
        user2 = User(
            username="uniqueuser",  # Ta sama nazwa
            password="pass2",
            role="user"
        )
        db.session.add(user2)
        try:
            db.session.commit()
            assert False, "Powinien wystąpić błąd unikalności"
        except Exception as e:
            assert "UNIQUE constraint failed" in str(e) or "unique" in str(e).lower()
            db.session.rollback()

def test_animal_default_image_filename(client):
    """Test domyślnej wartości image_filename dla Animal."""
    with client.application.app_context():
        animal = Animal(
            name="Panda",
            category="ssak",
            weight="50g-1kg",
            size="50cm-100cm",
            habitats="las"
            # image_filename nie podane — powinno użyć default
        )
        db.session.add(animal)
        db.session.commit()
        
        saved_animal = Animal.query.filter_by(name="Panda").first()
        assert saved_animal.image_filename == "placeholder.png"  # Domyślna wartość

def test_user_default_role(client):
    with client.application.app_context():
        user = User(
            username="defaultroleuser",
            password="pass"
            # role nie podane — powinno użyć default
        )
        db.session.add(user)
        db.session.commit()
        
        saved_user = User.query.filter_by(username="defaultroleuser").first()
        assert saved_user.role == "user"  # Domyślna wartość