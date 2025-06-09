import sys
import os
import json
# This is the line that will be executed when the script starts and will be dispalyed only once
print("Witaj w menedżerze zadań!")
# is_running is a flag to control the main loop
is_running = True


def dispaly_menu():
    # Function to dispaly the menu
    print("Wybierz opcję:")
    print("1. Dodaj zadanie")
    print("2. Wyświetl zadania")
    print("3. Oznacz zadanie jako wykonane")
    print("4. Usuń zadanie")
    print("5. Wyjdź")

    anwser = input("Wprowadź numer opcji: ")

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


def dispaly_tasks():
    # Function to dispaly all the tasks that have been added
    with open("data.json", 'r') as tasks:
        for task in tasks:
            print(task.strip())


def add_task(task_content):
    with open("data.json", 'w') as tasks:
        tasks.write(task_content + "\n")
    print(f"Zadanie '{task_content}' zostało dodane.")
