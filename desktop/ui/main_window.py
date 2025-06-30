# ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QMenuBar, QMenu, QMessageBox, QComboBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
import requests
import datetime

API_URL = "http://localhost:8000/api/"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDo App - Desktop")
        self.task_filter = "wszystkie"  # domyślny filtr

        # ---------------- MENU ----------------
        menu_bar = QMenuBar(self)
        file_menu = QMenu("Plik", self)
        exit_action = QAction("Zamknij", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

        # ---------------- MAIN LAYOUT ----------------
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header
        title_label = QLabel("ToDo App")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; padding: 10px; background-color: #f0f0f0; border-bottom: 1px solid #ccc;"
        )

        # ---------------- ADD TASK ----------------
        add_task_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Wpisz tytuł nowego zadania")
        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.add_task)

        add_task_layout.addWidget(self.task_input)
        add_task_layout.addWidget(add_button)

        # ---------------- FILTER ----------------
        filter_layout = QHBoxLayout()
        self.filter_box = QComboBox()
        self.filter_box.addItems(["wszystkie", "wykonane", "niewykonane"])
        self.filter_box.currentTextChanged.connect(self.change_filter)
        filter_layout.addWidget(QLabel("Filtr:"))
        filter_layout.addWidget(self.filter_box)

        # ---------------- TASK LIST ----------------
        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.toggle_task_done)

        # ---------------- DELETE BUTTON ----------------
        delete_button = QPushButton("Usuń zaznaczone zadanie")
        delete_button.clicked.connect(self.delete_selected_task)

        # ---------------- FOOTER ----------------
        footer_label = QLabel("ToDo App - PySide6 Example")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet(
            "font-size: 12px; background-color: #f0f0f0; border-top: 1px solid #ccc;"
        )

        # ---------------- FINAL LAYOUT ----------------
        main_layout.addWidget(title_label)
        main_layout.addLayout(add_task_layout)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.task_list)
        main_layout.addWidget(delete_button)
        main_layout.addWidget(footer_label)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # load tasks on startup
        self.load_tasks()

    # ---------------- FUNCTIONS ----------------
    def load_tasks(self):
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            tasks = response.json()
            self.task_list.clear()

            for task in tasks:
                status = "✅" if task['completed'] == "Done" else "❌"
                pretty_date = task['timestamp']
                try:
                    pretty_date = datetime.datetime.fromisoformat(
                        task['timestamp']).strftime("%d.%m.%Y %H:%M")
                except Exception:
                    pass

                # Task filters
                if self.task_filter == "wszystkie":
                    self.add_task_to_listwidget(task, status, pretty_date)
                elif self.task_filter == "wykonane" and task['completed'] == "Done":
                    self.add_task_to_listwidget(task, status, pretty_date)
                elif self.task_filter == "niewykonane" and task['completed'] != "Done":
                    self.add_task_to_listwidget(task, status, pretty_date)

        except Exception as e:
            QMessageBox.warning(
                self, "Błąd", f"Nie udało się pobrać zadań:\n{e}")

    def add_task_to_listwidget(self, task, status, pretty_date):
        item_text = f"{status} [{task['task_number']}] {task['title']} (do: {task['deadline']}) dodano: {pretty_date}"
        self.task_list.addItem(item_text)

    def add_task(self):
        title = self.task_input.text().strip()
        if title:
            new_task = {
                "title": title,
                "description": "",
                "deadline": ""
            }
            try:
                response = requests.post(f"{API_URL}add/", json=new_task)
                if response.status_code == 201:
                    QMessageBox.information(
                        self, "Sukces", f"Zadanie '{title}' dodane.")
                    self.task_input.clear()
                    self.load_tasks()
                else:
                    QMessageBox.warning(
                        self, "Błąd", f"Nie udało się dodać zadania:\n{response.text}")
            except Exception as e:
                QMessageBox.warning(self, "Błąd", f"Wystąpił problem:\n{e}")

    def toggle_task_done(self, item):
        # Get task number from text
        text = item.text()
        try:
            task_number = int(text.split('[')[1].split(']')[0])
            response = requests.patch(
                f"{API_URL}update/{task_number}/", json={"completed": "Done"})
            if response.status_code in [200, 202]:
                QMessageBox.information(
                    self, "OK", f"Oznaczono zadanie {task_number} jako wykonane.")
                self.load_tasks()
            else:
                QMessageBox.warning(
                    self, "Błąd", f"Nie udało się zaktualizować:\n{response.text}")
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Błąd:\n{e}")

    def delete_selected_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.information(
                self, "Uwaga", "Wybierz zadanie do usunięcia.")
            return
        for item in selected_items:
            try:
                task_number = int(item.text().split('[')[1].split(']')[0])
                response = requests.delete(f"{API_URL}delete/{task_number}/")
                if response.status_code == 204:
                    QMessageBox.information(
                        self, "OK", f"Usunięto zadanie {task_number}.")
                    self.load_tasks()
                else:
                    QMessageBox.warning(
                        self, "Błąd", f"Nie udało się usunąć:\n{response.text}")
            except Exception as e:
                QMessageBox.warning(self, "Błąd", f"Błąd:\n{e}")

    def change_filter(self, new_filter):
        self.task_filter = new_filter
        self.load_tasks()
