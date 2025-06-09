import sys
import os
import json
# This is the line that will be executed when the script starts and will be dispalyed only once
print("Witaj w menedżerze zadań!")
# is_running is a flag to control the main loop
is_running = True


def dispaly_tasks():
    # Function to dispaly all the tasks that have been added
    with open("data.json", 'r') as tasks:
        for task in tasks:
            print(task.strip())
