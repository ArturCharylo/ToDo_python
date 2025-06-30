# ui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QMenuBar, QMenu
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ToDo App - Desktop")

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

        # ---------------- BODY ----------------

        # Layout for adding tasks
        add_task_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Wpisz nowe zadanie")
        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.add_task)

        add_task_layout.addWidget(self.task_input)
        add_task_layout.addWidget(add_button)

        # Task list
        self.task_list = QListWidget()

        # ---------------- FOOTER ----------------
        footer_label = QLabel("Footer - Placeholder")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet(
            "font-size: 12px; background-color: #f0f0f0; border-top: 1px solid #ccc;"
        )

        # ---------------- FINAL LAYOUT ----------------
        main_layout.addWidget(title_label)
        main_layout.addLayout(add_task_layout)
        main_layout.addWidget(self.task_list)
        main_layout.addWidget(footer_label)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ---------------- FUNKCJE ----------------
    def add_task(self):
        task_text = self.task_input.text().strip()
        if task_text:
            self.task_list.addItem(task_text)
            self.task_input.clear()
