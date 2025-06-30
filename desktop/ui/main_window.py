# ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ToDo App - Desktop")

        # Create main widget and vertical layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header section with title
        title_label = QLabel("ToDo App")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; padding: 10px;")

        # Body section with placeholder content
        content_label = QLabel("Tutaj będzie reszta aplikacji")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to the layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(content_label)

        # Set layout in main widget
        main_widget.setLayout(main_layout)

        # Set main widget as central widget of the main window
        self.setCentralWidget(main_widget)
