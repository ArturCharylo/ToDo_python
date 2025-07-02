# ToDo_python

A simple ToDo application created to practice Python skills and expand my programming portfolio.

This is a desktop version of the app

> Api Uses [Django REST Framework](https://www.django-rest-framework.org/) for the API layer.

## 🚀 How to Start

### Requirements

- [Poetry](https://python-poetry.org/docs/) must be installed
- Python 3.10+ recommended

### Running the app

1. Go to the `api/src` directory and run:

   ```bash
   poetry run python manage.py runserver
   ```

2. Once the server is running, go back to the `desktop` directory and run:
   ```bash
   poetry run python main.py
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

## 🧠 About `main_window.py`

The `main_window.py` file contains the main layout and logic of the app. It includes:

- all the visual elements of the app that you are able to see and interact with once the app starts
- `display_menu()` – Displays the menu and handles user input
- `load_data()` – Utility function for fetching data from the backend.
- `add_task()`, `display_tasks()`, `mark_task_as_done()`, `delete_task()` – Main task-handling functions that interact with the backend

---

## 📦 Structure

```
.
├── README.md                      # Project documentation
├── LICENSE                        # Project license
├── pyproject.toml                 # Poetry project configuration
├── poetry.lock                    # Exact versions of installed dependencies
├── .gitignore                     # Files and folders to ignore in version control
├── main.py                        # Main entry point for the desktop application
├── api/
│   ├── src/
│   │   ├── api/                   # Django app for API
│   │   │   ├── __init__.py
│   │   │   ├── admin.py           # Django admin config (optional)
│   │   │   ├── apps.py            # App configuration
│   │   │   ├── models.py          # Database models
│   │   │   ├── serializers.py     # DRF serializers
│   │   │   ├── tests.py           # Unit tests for the app
│   │   │   ├── urls.py            # App-specific URL routes
│   │   │   └── views.py           # API views/endpoints
│   │   ├── myapi/                 # Django project configuration
│   │   │   ├── __init__.py
│   │   │   ├── asgi.py
│   │   │   ├── settings.py        # Main project settings
│   │   │   ├── urls.py            # Project URL routing
│   │   │   └── wsgi.py
│   │   ├── db.sqlite3             # SQLite database
│   │   └── manage.py              # Django management script
│   └── tests/
│       └── __init__.py            # Placeholder for tests
└── desktop/
    ├── assets/                    # Static assets like icons, images or styles
    ├── models/                    # Business logic and data layer for the desktop app
    │   ├── __init__.py
    │   ├── api_client.py          # Handles API communication
    │   └── state.py               # Application state management
    └── ui/                        # User interface components
        ├── __init__.py
        └── main_window.py         # Main application window UI


```

---

## ✅ Example Features

- Task title, description, deadline
- Marking tasks as completed
- Deleting tasks
- Filtering task by status
- All data stored in a database via Django backend
- CLI Interface

---

## 💡 Future Improvements

- Categories/tags
- Search options
- Moving functions from `ui/main_window` to `models/api_client`

---

## 📜 License

Licensed under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
