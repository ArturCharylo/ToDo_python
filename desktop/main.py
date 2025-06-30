# main.py

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
# This is the main entry point for the desktop application.
# The application initializes the main window and starts the event loop here.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec())
