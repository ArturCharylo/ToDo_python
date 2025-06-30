# desktop/models/api.py
import datetime
import requests

API_URL = "http://localhost:8000/api/"


def load_tasks():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Błąd ładowania zadań: {e}")
        return []


def add_task(title, description, deadline):
    new_task = {"title": title,
                "description": description, "deadline": deadline}
    try:
        response = requests.post(f"{API_URL}add/", json=new_task)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Błąd dodawania zadania: {e}")
        return False


def mark_task_as_done(task_number):
    try:
        response = requests.patch(
            f"{API_URL}update/{task_number}/", json={"completed": "Done"})
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Błąd oznaczania zadania: {e}")
        return False


def delete_task(task_number):
    try:
        response = requests.delete(f"{API_URL}delete/{task_number}/")
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Błąd usuwania zadania: {e}")
        return False
