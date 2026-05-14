# PromptVault

A modern AI Prompt Manager built using FastAPI, JWT Authentication, SQLAlchemy, and Vanilla JavaScript.

---

## Features

- User Registration & Login
- JWT Authentication
- Secure Password Hashing
- User-specific Prompt Management
- Create, Edit, Delete Prompts
- Favorite Prompts
- Search & Filter Prompts
- Copy Prompt to Clipboard
- Beautiful Modern UI
- Fully Responsive Frontend
- Protected Routes using JWT

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Pydantic

### Frontend
- HTML
- CSS
- Vanilla JavaScript

---

## Screenshots

(Add screenshots here later)

---

## Project Structure

```text
PromptVault/
│
├── routers/
│   ├── prompts.py
│   └── auth.py
│
├── static/
│   ├── style.css
│   └── app.js
│
├── templates/
│   └── home.html
│
├── database.py
├── models.py
├── schemas.py
├── security.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/promptvault-fastapi.git
```

Move into folder:

```bash
cd promptvault-fastapi
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn main:app --reload
```

Open browser:

```text
http://127.0.0.1:8000
```

---

## Authentication Flow

- User registers account
- Password hashed using Argon2
- User logs in
- JWT token generated
- Token stored in browser localStorage
- Protected APIs accessed using Bearer token

---

## Future Improvements

- Docker Deployment
- React Frontend
- PostgreSQL Database
- AI Prompt Suggestions
- Dark/Light Theme Toggle

---

## Author

Made by Mithun Venkatesan