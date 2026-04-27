# 🧠 API Users Management (FastAPI)

## 📌 Opis projektu

Aplikacja backendowa napisana w Pythonie z użyciem FastAPI.
Pozwala zarządzać użytkownikami (CRUD) oraz posiada system logowania z autoryzacją JWT.

---

## 🚀 Funkcjonalności

* 📥 Rejestracja użytkownika
* 🔐 Logowanie (JWT)
* 📄 Pobieranie listy użytkowników
* ➕ Dodawanie użytkownika
* ✏️ Edycja użytkownika
* ❌ Usuwanie użytkownika

---

## 🛠️ Technologie

* Python
* FastAPI
* SQLite
* JWT (python-jose)
* bcrypt

---

## 🌐 Demo (LIVE API)

👉 https://api-projekt-ugfm.onrender.com/docs

---

## 📊 Data Pipeline (ETL)

Projekt zawiera pipeline danych:

* Extract: dane z pliku CSV
* Transform: filtrowanie i tworzenie kategorii (pandas)
* Load: zapis do PostgreSQL
* Automatyzacja: pipeline może być uruchamiany cyklicznie (scheduler)

Endpoint:

* `/analytics` – agregacja danych (FastAPI + PostgreSQL)

---

## ⚙️ Uruchomienie lokalne

```bash
git clone https://github.com/nataliakloc96-ui/api-projekt.git
cd api-project
py -3.11 -m pip install -r requirements.txt
py -3.11 -m uvicorn main:app --reload
```

---

## 🔐 Autoryzacja

Aby korzystać z endpointów:

1. Zarejestruj użytkownika `/register`
2. Zaloguj się `/login`
3. Skopiuj token
4. Kliknij "Authorize" w `/docs`
5. Wklej:

```
Bearer TWÓJ_TOKEN
```

---

## 📊 Przykładowe endpointy

* GET /users
* POST /users
* DELETE /users/{id}
* PUT /users/{id}

---

## 💡 Autor

Natalia Kurek
