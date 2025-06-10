import sys
import os
import json
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
    with open(file_name, 'r') as tasks:
        try:
            return json.load(tasks)
        except json.JSONDecodeError:
            return []  # Return an empty list if the file is empty or corrupted


def save_tasks(tasks):
    # Function to save tasks to the file
    with open(file_name, 'w') as tasks_file:
        # Save with indentation for readability
        json.dump(tasks, tasks_file, indent=4)


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
    tasks = load_tasks()
    tasks.append(
        {"title": task_title, "description": task_description,
         "deadline": task_deadline, "done": False}
    )
    save_tasks(tasks)
    print(f"Zadanie '{task_title}' zostało dodane.")


def dispaly_tasks():
    # Function to dispaly all the tasks that have been added
    tasks = load_tasks()
    if not tasks:
        print("Brak zadań, najpierw dodaj zadania.")
        return
    print("Lista zadań:")
    for id, task in enumerate(tasks, start=1):
        status = "Wykonane" if task['done'] else "Niewykonane"
        print(
            f"id: {id}.  tytuł: {task['title']}, opis: {task['description']}, termin wykonania: {task['deadline']}, status: {status}")


def mark_task_as_done(task_id):
    # Function to change the status of a task to done
    tasks = load_tasks()
    task_id = int(task_id) - 1  # Convert to zero-based index
    if 0 <= task_id < len(tasks):
        tasks[task_id]['done'] = True
        save_tasks(tasks)
        print(f"Zadanie o id {task_id + 1} zostało oznaczone jako wykonane.")
    else:
        print(f"Zadanie o id {task_id + 1} nie istnieje.")


def delete_task(task_id):
    # Function to delete a task by its id form the data file
    tasks = load_tasks()
    task_id = int(task_id) - 1  # Convert to zero-based index
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
        print(f"Zadanie o id {task_id + 1} zostało usunięte.")
    else:
        print(f"Zadanie o id {task_id + 1} nie istnieje.")


# Main loop to keep the program running until the user decides to exit
while is_running:
    dispaly_menu()
    if not is_running:
        break
    print()  # Print a new line for better readability
