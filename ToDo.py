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
            print("Podaj treść zadania:")
            task_content = input()
            add_task(task_content)
        case '2':
            dispaly_tasks()
        case '3':
            print("Podaj numer zadania do oznaczenia jako wykonane:")
            task_number = input()
            mark_task_as_done(task_number)
        case '4':
            print("Podaj numer zadania do usunięcia:")
            task_number = input()
            delete_task(task_number)
        case '5':
            is_running = False
            print("Dziękujemy za korzystanie z menedżera zadań!")


def add_task(task_content):
    # Function to add a new task to the file
    with open(file_name, 'r+') as tasks:
        json.dump(task_content, tasks)
    print(f"Zadanie '{task_content}' zostało dodane.")


def dispaly_tasks():
    # Function to dispaly all the tasks that have been added
    with open(file_name, 'r') as tasks:
        for task in tasks:
            print(task.strip())


def mark_task_as_done(task_number):
    with open(file_name, 'w') as tasks:
        for id, task in tasks:
            if id == task_number:
                tasks.write(f"{task.strip()} - Wykonane\n")
                print(
                    f"Zadanie {task_number} zostało oznaczone jako wykonane.")
                return


def delete_task(task_number):
    with open(file_name, 'r') as tasks:
        for id, task in tasks:
            if id == task_number:
                tasks.remove(task)
                print(f"Zadanie {task_number} zostało usunięte.")
                return


# Main loop to keep the program running until the user decides to exit
while is_running:
    dispaly_menu()
    if not is_running:
        break
    print()  # Print a new line for better readability
