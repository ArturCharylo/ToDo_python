# ToDo_python

A simple ToDo application created to practice Python skills and expand my programming portfolio.

## 🚀 How to Start

### Requirements

- [Poetry](https://python-poetry.org/docs/) must be installed
- Python 3.10+ recommended

### Running the app

1. Go to the `api` directory and run:

   ```bash
   poetry run python manage.py runserver
   ```

2. Once the server is running, go back to the root directory and run:
   ```bash
   poetry run python ToDo.py
   ```

> ⚠️ Make sure you have installed all required packages beforehand.

---

## 🗃️ API Setup

When running the project for the first time, you need to set up the database:

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

This will generate the database and create the required tables.

All the backend endpoints are located in `api/src/api/views.py`. The app provides the following API routes:

- `GET` – Returns all tasks from the database
- `POST` – Adds a new task
- `PATCH` – Updates the completion status of a task
- `DELETE` – Deletes a task

---

## 🧠 About `ToDo.py`

The `ToDo.py` file contains the main logic of the app. It includes:

- `display_menu()` – Displays the menu and handles user input
- `load_data()` – Utility function for fetching data from the backend.
- `add_task()`, `display_tasks()`, `mark_task_as_done()`, `delete_task()` – Main task-handling functions that interact with the backend

---

## 📦 Structure

```
.
├── ToDo.py                        # Main CLI interface
├── README.md                      # Project documentation
├── pyproject.toml / poetry.lock   # Poetry dependency files
└── api/
    ├── src/
    │   ├── api/                   # Django app for API
    │   │   ├── __init__.py
    │   │   ├── admin.py           # Django admin config (optional)
    │   │   ├── apps.py            # App configuration
    │   │   ├── models.py          # Database models
    │   │   ├── serializers.py     # DRF serializers
    │   │   ├── tests.py           # Unit tests for the app
    │   │   ├── urls.py            # App-specific URL routes
    │   │   └── views.py           # API views/endpoints
    │   ├── myapi/                 # Django project configuration
    │   │   ├── __init__.py
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py            # Project URL routing
    │   │   └── wsgi.py
    │   ├── db.sqlite3             # SQLite database
    │   └── manage.py              # Django management script
    └── tests/
        └── __init__.py            # Placeholder for tests
```

---

## ✅ Example Features

- Task title, description, deadline
- Marking tasks as completed
- Deleting tasks
- All data stored in a database via Django backend
- CLI Interface

---

## 💡 Future Improvements

- Categories/tags
- Search and filter options

---

## 📜 License

Licensed under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
