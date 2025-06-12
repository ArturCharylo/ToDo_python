import os
import json
import datetime
import requests
# This is the line that will be executed when the script starts and will be dispalyed only once
print("Witaj w menedżerze zadań!")
# is_running is a flag to control the main loop
is_running = True
file_name = "data.json"

# Sprawdzanie czy plik istnieje, jeśli nie to tworzenie go
if not os.path.exists(file_name):
    with open(file_name, 'w') as file:
        json.dump([], file)


def load_tasks():
    # Function to load tasks from the file
    response = requests.get("http://127.0.0.1:8000/api/")
    if response.status_code == 200:
        return response.json()
    else:
        print("An error occurred while loading tasks.")
        print(f"Status code: {response.status_code}")
        return []


def dispaly_menu():
    # Function to dispaly the menu
    global is_running
    print("Wybierz opcję:")
    print("1. Dodaj zadanie")
    print("2. Wyświetl zadania")
    print("3. Oznacz zadanie jako wykonane")
    print("4. Usuń zadanie")
    print("5. Wyjdź")

    anwser = input("Wprowadź numer opcji: ")

    # Match case to handle the user's choice
    match anwser:
        case '1':
            print("Podaj tytuł zadania:")
            task_title = input()
            print("Podaj opis zadania:")
            task_description = input()
            print("Podaj deadline zadania:")
            task_deadline = input()
            add_task(task_title, task_description, task_deadline)
        case '2':
            dispaly_tasks()
        case '3':
            print("Podaj numer zadania do oznaczenia jako wykonane:")
            task_id = input()
            mark_task_as_done(task_id)
        case '4':
            print("Podaj numer zadania do usunięcia:")
            task_id = input()
            delete_task(task_id)
        case '5':
            is_running = False
            print("Dziękujemy za korzystanie z menedżera zadań!")


def add_task(task_title, task_description, task_deadline):
    # Function to add a new task to the file
    new_task = {
        "title": task_title,
        "description": task_description,
        "deadline": task_deadline
    }
    response = requests.post("http://127.0.0.1:8000/api/add/", json=new_task)
    if response.status_code == 201:
        print(f"Zadanie '{task_title}' zostało dodane.")
    else:
        print("Błąd podczas dodawania zadania.")
        print(response.status_code, response.text)


def dispaly_tasks():
    # Function to dispaly all the tasks that have been added
    tasks = load_tasks()
    if not tasks:
        print("Brak zadań.")
        return
    print("Lista zadań:")
    for task in tasks:
        status = "Wykonane" if task['completed'] == "Done" else "Niewykonane"
        pretty_date = task['timestamp']
        try:
            pretty_date = datetime.datetime.fromisoformat(
                task['timestamp']).strftime("%d.%m.%Y %H:%M")
        except Exception:
            pass
        print(
            f"id: {task['id']}, tytuł: {task['title']}, opis: {task['description']}, termin: {task['deadline']}, dodano: {pretty_date}, status: {status}")


def mark_task_as_done(task_id):
    # Function to change the status of a task to done
    task_id = int(task_id)
    response = requests.patch(
        f"http://localhost:8000/api/update/{task_id}/", json={"completed": "Done"})
    if response.status_code in [200, 202]:
        print(f"Zadanie o id {task_id} zostało oznaczone jako wykonane.")
    else:
        print("Nie udało się zaktualizować zadania.")
        print(response.status_code, response.text)


def delete_task(task_id):
    # Function to delete a task by its id form the data file
    task_id = int(task_id)
    response = requests.delete(f"http://localhost:8000/api/delete/{task_id}/")
    if response.status_code == 204:
        print(f"Zadanie o id {task_id} zostało usunięte.")
    else:
        print("Nie udało się usunąć zadania.")
        print(response.status_code, response.text)


# Main loop to keep the program running until the user decides to exit
while is_running:
    dispaly_menu()
    if not is_running:
        break
    print()  # Print a new line for better readability
