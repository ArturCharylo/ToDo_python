import os
import json
import datetime
import requests
# This is the line that will be executed when the script starts and will be displayed only once
print("Witaj w menedżerze zadań!")
# is_running is a flag to control the main loop
is_running = True
API_URL = "http://localhost:8000/api/"
task_filter = "wszystkie"  # Default filter for displaying tasks


def load_tasks():
    # Function to load tasks from the file
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("An error occurred while loading tasks.")
        print(f"Status code: {response.status_code}")
        return []


def display_menu():
    # Function to display the menu
    global is_running
    global task_filter
    print("Wybierz opcję:")
    print("1. Dodaj zadanie")
    print("2. Wyświetl zadania")
    print("3. Zmień filtry wyświetlania zadań")
    print("4. Oznacz zadanie jako wykonane")
    print("5. Usuń zadanie")
    print("6. Wyjdź")

    try:
        anwser = int(input("Wprowadź numer opcji: "))
    except ValueError:
        print("Nieprawidłowy numer opcji.")
        return

    # Match case to handle the user's choice
    match anwser:
        case 1:
            print("Podaj tytuł zadania:")
            task_title = input()
            print("Podaj opis zadania:")
            task_description = input()
            print("Podaj deadline zadania:")
            task_deadline = input()
            add_task(task_title, task_description, task_deadline)
        case 2:
            display_tasks()
        case 3:
            print(
                f"Obecnie opcja filtrowania to: {task_filter}, jeśli chcesz zmienić, wpisz nową opcję (wszystkie, wykonane, niewykonane):")
            # Validate new filter input
            new_filter = input()
            if new_filter in ["wszystkie", "wykonane", "niewykonane"]:
                task_filter = new_filter
                print(f"Zmieniono filtr na: {task_filter}")
            else:
                print(
                    "Nieprawidłowa opcja filtrowania. Ustawiono domyślnie na 'wszystkie'.")
                task_filter = "wszystkie"
        case 4:
            print("Podaj numer zadania do oznaczenia jako wykonane:")
            try:
                task_id = int(input())
            except ValueError:
                print("Nieprawidłowy numer zadania.")
                return
            mark_task_as_done(task_id)
        case 5:
            print("Podaj numer zadania do usunięcia:")
            try:
                task_id = int(input())
            except ValueError:
                print("Nieprawidłowy numer zadania.")
                return
            delete_task(task_id)
        case 6:
            is_running = False
            print("Dziękujemy za korzystanie z menedżera zadań!")
        case _:
            print("Nieprawidłowa opcja.")


def add_task(task_title, task_description, task_deadline):
    # Function to add a new task to the file
    new_task = {
        "title": task_title,
        "description": task_description,
        "deadline": task_deadline
    }
    response = requests.post(f"{API_URL}add/", json=new_task)
    if response.status_code == 201:
        print(f"Zadanie '{task_title}' zostało dodane.")
    else:
        print("Błąd podczas dodawania zadania.")
        print(response.status_code, response.text)


def display_tasks():
    # Function to display all the tasks that have been added
    tasks = load_tasks()
    if not tasks:
        print("Brak zadań.")
        return
    print("="*150)
    print("Lista zadań:")
    for task in tasks:
        status = "Wykonane" if task['completed'] == "Done" else "Niewykonane"
        pretty_date = task['timestamp']
        try:
            pretty_date = datetime.datetime.fromisoformat(
                task['timestamp']).strftime("%d.%m.%Y %H:%M")
        except Exception:
            pass
        if task_filter == "wszystkie":
            print(
                f"id: {task['id']}, tytuł: {task['title']}, opis: {task['description']}, termin: {task['deadline']}, dodano: {pretty_date}, status: {status}")
        elif task_filter == "wykonane" and task['completed'] == "Done":
            print(
                f"id: {task['id']}, tytuł: {task['title']}, opis: {task['description']}, termin: {task['deadline']}, dodano: {pretty_date}, status: {status}")
        elif task_filter == "niewykonane" and task['completed'] != "Done":
            print(
                f"id: {task['id']}, tytuł: {task['title']}, opis: {task['description']}, termin: {task['deadline']}, dodano: {pretty_date}, status: {status}")
    print("="*150)


def mark_task_as_done(task_id):
    # Function to change the status of a task to done
    response = requests.patch(
        f"{API_URL}update/{task_id}/", json={"completed": "Done"})
    if response.status_code in [200, 202]:
        print(f"Zadanie o id {task_id} zostało oznaczone jako wykonane.")
    else:
        print("Nie udało się zaktualizować zadania.")
        print(response.status_code, response.text)


def delete_task(task_id):
    # Function to delete a task by its id from the API
    response = requests.delete(f"{API_URL}delete/{task_id}/")
    if response.status_code == 204:
        print(f"Zadanie o id {task_id} zostało usunięte.")
    else:
        print("Nie udało się usunąć zadania.")
        print(response.status_code, response.text)


# Main loop to keep the program running until the user decides to exit
if __name__ == "__main__":
    while is_running:
        display_menu()
        if not is_running:
            break
        print()  # Print a new line for better readability
