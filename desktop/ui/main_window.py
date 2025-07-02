# ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QMenuBar, QMenu, QMessageBox, QComboBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QTimer
from models.api_client import (
    load_tasks_from_api,
    add_task_to_api,
    toggle_task_done_in_api,
    delete_task_in_api,
)
import asyncio


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDo App - Desktop")
        self.task_filter = "wszystkie"  # default filter

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
        self.task_title = QLineEdit()
        self.task_description = QLineEdit()
        self.task_deadline = QLineEdit()
        self.task_title.setPlaceholderText("Wpisz tytuł nowego zadania")
        self.task_description.setPlaceholderText("Opis zadania")
        self.task_deadline.setPlaceholderText("Termin wykonania")
        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.add_task)

        add_task_layout.addWidget(self.task_title)
        add_task_layout.addWidget(self.task_description)
        add_task_layout.addWidget(self.task_deadline)
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

        # Run the event loop
        self.loop = asyncio.get_event_loop()
        QTimer.singleShot(0, self.process_events)

        # load tasks on startup
        asyncio.ensure_future(self.load_tasks())

    def process_events(self):
        try:
            self.loop.stop()
            self.loop.run_forever()
        except Exception:
            pass
        QTimer.singleShot(50, self.process_events)

    async def load_tasks(self):
        try:
            tasks = await load_tasks_from_api(self.task_filter)
            self.task_list.clear()
            for task, status, pretty_date in tasks:
                self.add_task_to_listwidget(task, status, pretty_date)
        except Exception as e:
            QMessageBox.warning(
                self, "Błąd", f"Nie udało się pobrać zadań:\n{e}")

    def add_task_to_listwidget(self, task, status, pretty_date):
        item_text = (
            f"{status} [{task['task_number']}] {task['title']} (do: {task['deadline']})\n"
            f"Opis: {task.get('description', '')} | dodano: {pretty_date}"
        )
        self.task_list.addItem(item_text)

    def add_task(self):
        title = self.task_title.text().strip()
        description = self.task_description.text().strip()
        deadline = self.task_deadline.text().strip()
        if title:
            asyncio.ensure_future(self._add_task_async(
                title, description, deadline))

    async def _add_task_async(self, title, description, deadline):
        try:
            response = await add_task_to_api(title, description, deadline)
            if response.status == 201:
                QMessageBox.information(
                    self, "Sukces", f"Zadanie '{title}' dodane.")
                self.task_title.clear()
                self.task_description.clear()
                self.task_deadline.clear()
                await self.load_tasks()
            else:
                text = await response.text()
                QMessageBox.warning(
                    self, "Błąd", f"Nie udało się dodać zadania:\n{text}")
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Wystąpił problem:\n{e}")

    def toggle_task_done(self, item):
        text = item.text()
        try:
            task_number = int(text.split('[')[1].split(']')[0])
            asyncio.ensure_future(self._toggle_task_done_async(task_number))
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Błąd:\n{e}")

    async def _toggle_task_done_async(self, task_number):
        try:
            response = await toggle_task_done_in_api(task_number)
            if response.status in [200, 202]:
                QMessageBox.information(
                    self, "OK", f"Oznaczono zadanie {task_number} jako wykonane.")
                await self.load_tasks()
            else:
                text = await response.text()
                QMessageBox.warning(
                    self, "Błąd", f"Nie udało się zaktualizować:\n{text}")
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
                asyncio.ensure_future(self._delete_task_async(task_number))
            except Exception as e:
                QMessageBox.warning(self, "Błąd", f"Błąd:\n{e}")

    async def _delete_task_async(self, task_number):
        try:
            response = await delete_task_in_api(task_number)
            if response.status == 204:
                QMessageBox.information(
                    self, "OK", f"Usunięto zadanie {task_number}.")
                await self.load_tasks()
            else:
                text = await response.text()
                QMessageBox.warning(
                    self, "Błąd", f"Nie udało się usunąć:\n{text}")
        except Exception as e:
            QMessageBox.warning(self, "Błąd", f"Błąd:\n{e}")

    def change_filter(self, new_filter):
        self.task_filter = new_filter
        asyncio.ensure_future(self.load_tasks())
