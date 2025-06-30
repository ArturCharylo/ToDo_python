import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDo App - Desktop")

        # General layout for the main window
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

        # Apply widget styles
        main_layout.addWidget(title_label)
        main_layout.addWidget(content_label)

        # Apply the layout to the main widget
        main_widget.setLayout(main_layout)

        # Making the main widget the central widget of the main window
        self.setCentralWidget(main_widget)


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec())
