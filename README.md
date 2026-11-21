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

### Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

### Frontend

W drugim terminalu:

```bash
cd frontend
npm install
npm run dev
```