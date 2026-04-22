Prosta gra inspirowana Wordlem, gdzie zgadujemy nazwy zwierząt.

Po każdej próbie dostajemy historię naszych prób, wraz z informacjami co (kategoria, habitat, waga, rozmiar) było dobrze, częściowo dobrze lub źle.

Uruchomiamy komendą:
python run.py

Elementy niezbędne:

● Przynajmniej 5 podstron; -> win, game, add_animal, edit_animal, login, animals itd. (patrz routes.py)
● Komunikacja z bazą danych: przesył danych w dwie strony (np. CRUD – Create, Read, Update,
Delete); -> Dodawanie, oglądanie, usuwanie i modyfikacja zwierząt w bazie danych.
● Przynajmniej 5 widoków; -> win, game, add_animal, edit_animal, login, register itd. (patrz app/templates)
● Wykorzystanie blueprintów; -> blueprint main w routes.py, podpięty do aplikacji w app factory w __init__.py.
● Przynajmniej 1 formularz na stronie (np. rejestracyjny, kontaktowy, dodawania danych do bazy); -> rejestracja użytkownika, dodawanie i edytowanie zwierząt.
● Obsługa błędów 404 i 500 (np. własne szablony dla tych błędów); -> app/templates 404.html i 500.html
● Testy najważniejszych funkcjonalności. -> app/tests/

Elementy dodatkowe:
● Stylizacja z wykorzystaniem CSS lub frameworka (np. Bootstrap, Tailwind); -> app/static/style.css
● Wykorzystanie Jinja2; -> We wszystkich widokach do ładowania zawartości przez {% block content %}, dodatkowo w add_animal.html i edit_animal.html do
ładowania habitatów, kategorii itd.
● Formularz na stronie obejmujący możliwość załączenia pliku z uwzględnieniem różnych
rozszerzeń; -> Gdy dodaję/edytuję zwierzę mogę załączyć plik .jpg, .png, .jpeg.
● Możliwość tworzenia kont przez użytkowników: przynajmniej konta zwykłego i administratora,
oraz logowania; -> Jest
● Możliwość tworzenia/dodawania postów/artykułów/ankiet; -> możliwość dodawania zwierząt do gry
● Dodanie systemu uwierzytelniającego, np. zabezpieczenie kont adminów; -> w routes.py funkcje login_required i admin_required upewniają się
że niezalogowane osoby nie mogą dodawać zwierząt, a tylko admini mogą je edytować/usuwać.
● Inne zaawansowane opcje. -> dzięki fuzzy search nie muszę dać dokładnie nazwy zwierzęcia: przykładowo "czarn wdowy" zostanie zaakceptowany
jako "czarna wdowa".
