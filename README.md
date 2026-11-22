# Song Recommendation System

## Nazwa kursu

Testowanie i Jakość Oprogramowania

## Autor

Katarzyna Mierzyńska

## Temat projektu

System rekomendacji utworów muzycznych

## Opis projektu

Projekt jest systemem rekomendacji utworów muzycznych wykorzystującym algorytmy uczenia maszynowego. Analizuje cechy utworów, takie jak gatunek, tempo i nastrój, aby proponować użytkownikom spersonalizowane rekomendacje. Aplikacja składa się z backendu w Pythonie oraz interfejsu użytkownika we Vue.js.

## Uruchomienie projektu

Wymagane są Python 3.11+ oraz Node.js z npm.

### Backend (FastAPI)

Z katalogu głównego projektu:

```bash
python -m uvicorn backend.main:app --reload
```

### Frontend

W drugim terminalu:

```bash
cd frontend
npm install
npm run dev
```

Backend jest dostępny pod adresem `http://localhost:8000`, a frontend pod adresem wyświetlonym przez Vite (domyślnie `http://localhost:5173`).

## Testy

Testy jednostkowe i integracyjne nie zostały jeszcze dodane. Sekcja zostanie uzupełniona po ich przygotowaniu.

## Dokumentacja API

API jest udostępniane przez FastAPI. Po uruchomieniu backendu dokumentacja interaktywna jest dostępna pod adresami:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

| Metoda | Endpoint | Opis |
|---|---|---|
| `GET` | `/` | Sprawdzenie dostępności API |
| `POST` | `/auth/register` | Rejestracja użytkownika |
| `POST` | `/auth/verify-email` | Potwierdzenie adresu e-mail |
| `POST` | `/auth/login` | Logowanie użytkownika |
| `POST` | `/auth/logout` | Wylogowanie użytkownika |
| `GET` | `/auth/me` | Dane zalogowanego użytkownika |
| `GET` | `/auth/favorites` | Lista ulubionych utworów |
| `POST` | `/auth/favorites` | Dodanie utworu do ulubionych |
| `DELETE` | `/auth/favorites/{track_id}` | Usunięcie utworu z ulubionych |
| `GET` | `/songs/search/{name}` | Wyszukiwanie utworów po nazwie |
| `GET` | `/songs/{track_id}` | Szczegóły utworu |
| `POST` | `/songs/recommend` | Rekomendacje utworów |

## Przypadki testowe dla testera manualnego (TestCase)

Każdy przypadek testowy powinien zawierać: unikalny identyfikator, tytuł opisujący cel testu, warunki wymagane przed jego rozpoczęciem, ponumerowane kroki testowe oraz jednoznacznie określony oczekiwany rezultat.

### TC-01 — Rejestracja poprawnymi danymi

| ID | TC-01 |
|---|---|
| **Tytuł** | Rejestracja użytkownika poprawnymi danymi |
| **Warunki początkowe** | Aplikacja jest uruchomiona, użytkownik znajduje się na stronie rejestracji i nie ma jeszcze konta z podanym adresem e-mail |
| **Kroki testowe** | 1. Wprowadź poprawny adres e-mail.<br>2. Wprowadź hasło spełniające wymagania walidacyjne.<br>3. Powtórz hasło w polu potwierdzającym.<br>4. Zaakceptuj regulamin.<br>5. Kliknij przycisk rejestracji |
| **Oczekiwany rezultat** | Konto zostaje utworzone, a użytkownik otrzymuje komunikat o potrzebie potwierdzenia adresu e-mail |

### TC-02 — Walidacja hasła

| ID | TC-02 |
|---|---|
| **Tytuł** | Odrzucenie hasła niespełniającego wymagań |
| **Warunki początkowe** | Aplikacja jest uruchomiona i użytkownik znajduje się na stronie rejestracji |
| **Kroki testowe** | 1. Wprowadź poprawny adres e-mail.<br>2. Wprowadź hasło krótsze niż 8 znaków lub nie zawierające wielkiej litery i cyfry.<br>3. Kliknij przycisk rejestracji |
| **Oczekiwany rezultat** | Konto nie zostaje utworzone, a formularz wyświetla komunikat walidacyjny dotyczący hasła |

### TC-03 — Logowanie

| ID | TC-03 |
|---|---|
| **Tytuł** | Poprawne logowanie użytkownika |
| **Warunki początkowe** | Konto użytkownika zostało utworzone i potwierdzono jego adres e-mail |
| **Kroki testowe** | 1. Otwórz stronę logowania.<br>2. Wprowadź poprawny adres e-mail.<br>3. Wprowadź poprawne hasło.<br>4. Kliknij przycisk logowania |
| **Oczekiwany rezultat** | Użytkownik zostaje zalogowany i uzyskuje dostęp do panelu aplikacji |

### TC-04 — Wyszukiwanie utworu

| ID | TC-04 |
|---|---|
| **Tytuł** | Wyszukiwanie utworów po nazwie |
| **Warunki początkowe** | Aplikacja działa, użytkownik jest zalogowany lub ma dostęp do wyszukiwarki, a baza zawiera utwory |
| **Kroki testowe** | 1. Otwórz moduł wyszukiwania utworów.<br>2. Wprowadź nazwę istniejącego utworu.<br>3. Uruchom wyszukiwanie |
| **Oczekiwany rezultat** | Zostaje wyświetlona lista utworów pasujących do wpisanej nazwy |

### TC-05 — Rekomendacje

| ID | TC-05 |
|---|---|
| **Tytuł** | Generowanie rekomendacji na podstawie utworu |
| **Warunki początkowe** | Użytkownik widzi szczegóły utworu znajdującego się w bazie |
| **Kroki testowe** | 1. Wybierz istniejący utwór.<br>2. Uruchom generowanie rekomendacji.<br>3. Poczekaj na odpowiedź systemu |
| **Oczekiwany rezultat** | Aplikacja wyświetla listę rekomendowanych utworów, najlepiej podobnych do wyboru użytkownika |

### TC-06 — Dodanie utworu do ulubionych

| ID | TC-06 |
|---|---|
| **Tytuł** | Dodanie utworu do listy ulubionych |
| **Warunki początkowe** | Użytkownik jest zalogowany i wyświetla szczegóły lub wynik wyszukiwania zawierający istniejący utwór |
| **Kroki testowe** | 1. Otwórz szczegóły utworu.<br>2. Kliknij przycisk dodania do ulubionych |
| **Oczekiwany rezultat** | Utwór pojawia się na liście ulubionych zalogowanego użytkownika |

### TC-07 — Wylogowanie

| ID | TC-07 |
|---|---|
| **Tytuł** | Poprawne wylogowanie użytkownika |
| **Warunki początkowe** | Użytkownik jest zalogowany i znajduje się w panelu aplikacji |
| **Kroki testowe** | 1. Kliknij menu użytkownika.<br>2. Wybierz opcję wylogowania |
| **Oczekiwany rezultat** | Sesja użytkownika zostaje zakończona, a aplikacja przenosi go do strony logowania lub strony głównej |

### TC-08 — Niepoprawne dane logowania

| ID | TC-08 |
|---|---|
| **Tytuł** | Odrzucenie niepoprawnych danych logowania |
| **Warunki początkowe** | Aplikacja działa i użytkownik znajduje się na stronie logowania |
| **Kroki testowe** | 1. Wprowadź nieistniejący adres e-mail lub błędne hasło.<br>2. Kliknij przycisk logowania |
| **Oczekiwany rezultat** | Logowanie zostaje odrzucone i wyświetla się komunikat o niepoprawnych danych |

### TC-09 — Wyszukiwanie nieistniejącego utworu

| ID | TC-09 |
|---|---|
| **Tytuł** | Wyszukiwanie utworu nieobecnego w bazie |
| **Warunki początkowe** | Aplikacja działa i użytkownik ma dostęp do wyszukiwarki |
| **Kroki testowe** | 1. Otwórz wyszukiwarkę utworów.<br>2. Wprowadź nazwę, której brak w bazie danych.<br>3. Uruchom wyszukiwanie |
| **Oczekiwany rezultat** | Aplikacja wyświetla komunikat informujący, że nie znaleziono pasujących utworów |

### TC-10 — Usunięcie ulubionego utworu

| ID | TC-10 |
|---|---|
| **Tytuł** | Usunięcie utworu z listy ulubionych |
| **Warunki początkowe** | Użytkownik jest zalogowany, a co najmniej jeden utwór znajduje się na jego liście ulubionych |
| **Kroki testowe** | 1. Otwórz listę ulubionych utworów.<br>2. Wybierz zapisany utwór.<br>3. Kliknij przycisk usunięcia |
| **Oczekiwany rezultat** | Wybrany utwór zostaje usunięty i nie jest już widoczny na liście ulubionych |

## Technologie użyte w projekcie

- **Python** i **FastAPI** – backend oraz REST API.
- **SQLAlchemy** i **SQLite** – obsługa bazy danych.
- **scikit-learn** – modele uczenia maszynowego wykorzystywane do rekomendacji.
- **Pandas** i **NumPy** – przetwarzanie danych.
- **Vue.js** – frontend aplikacji.
- **TypeScript** – typowanie kodu frontendowego.
- **Vite** – uruchamianie i budowanie frontendu.