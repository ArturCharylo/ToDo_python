from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

app = QApplication([])

window = QMainWindow()
window.setWindowTitle("ToDo App - Desktop")
label = QLabel("Hello, PySide6!")
window.setCentralWidget(label)

window.resize(400, 300)
window.show()

app.exec()
