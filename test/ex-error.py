from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create a button that triggers an error
        error_button = QPushButton("Trigger Error", self)
        error_button.clicked.connect(self.show_error_message)

        self.setCentralWidget(error_button)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Error Alert Example")
        self.show()

    def show_error_message(self):
        # Create a QMessageBox with an error type
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText("An error occurred!")
        error_box.setStandardButtons(QMessageBox.Ok)

        # Show the error message box
        error_box.exec_()

if __name__ == '__main__':
    app = QApplication([])
    window = MyMainWindow()
    app.exec_()
