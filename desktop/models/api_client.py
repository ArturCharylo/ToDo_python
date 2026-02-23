# desktop/models/task_service.py

import aiohttp
import datetime

API_URL = "http://localhost:8000/api/"


async def load_tasks_from_api(task_filter):
    tasks_to_display = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}tasks/") as response:
            response.raise_for_status()
            tasks = await response.json()

            for task in tasks:
                status = "✅" if task['completed'] == "Done" else "❌"
                pretty_date = task['timestamp']
                try:
                    pretty_date = datetime.datetime.fromisoformat(
                        task['timestamp']).strftime("%d.%m.%Y %H:%M")
                except Exception:
                    pass

                if task_filter == "wszystkie":
                    tasks_to_display.append((task, status, pretty_date))
                elif task_filter == "wykonane" and task['completed'] == "Done":
                    tasks_to_display.append((task, status, pretty_date))
                elif task_filter == "niewykonane" and task['completed'] != "Done":
                    tasks_to_display.append((task, status, pretty_date))
    return tasks_to_display


async def add_task_to_api(title, description, deadline):
    new_task = {
        "title": title,
        "description": description,
        "deadline": deadline,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}tasks/", json=new_task) as response:
            return response


async def toggle_task_done_in_api(task_number):
    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f"{API_URL}tasks/{task_number}/", json={"completed": "Done"}
        ) as response:
            return response


async def delete_task_in_api(task_number):
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}tasks/{task_number}/") as response:
            return response
