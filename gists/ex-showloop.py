import sys
import time
from PySide6 import QtWidgets, QtCore, QtGui


class ProcessingWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Processing...")
        self.setFixedSize(200, 100)
        layout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel("Processing...", self)
        self.label.setFont(QtGui.QFont("Arial", 16))
        layout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setWindowFlags(QtCore.Qt.WindowType.SplashScreen)

    def center(self):
        # Calculate the center position of the main window
        parent_rect = self.parent().geometry()
        parent_center = parent_rect.center()

        # Calculate the position of the dialog
        dialog_rect = self.geometry()
        dialog_rect.moveCenter(parent_center)
        self.setGeometry(dialog_rect)


class LongProcessThread(QtCore.QThread):
    finished = QtCore.Signal()

    def __init__(self, parent=None, duration=None):
        super().__init__(parent)
        self.parent = parent
        self.duration = duration

    def run(self):
        self.parent.simulate_long_process(self.duration)
        self.finished.emit()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Long Process Example")
        self.setFixedSize(500, 300)
        layout = QtWidgets.QVBoxLayout(self)
        self.button = QtWidgets.QPushButton("Run Long Process", self)
        layout.addWidget(self.button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button.clicked.connect(self.run_long_process)
        self.processing_window = None

    def run_long_process(self):
        self.button.setEnabled(False)
        long_process_duration = 10  # seconds
        delay_popup = 3000  # milliseconds
        long_process_thread = LongProcessThread(self, long_process_duration)
        long_process_thread.finished.connect(self.enable_button)
        long_process_thread.start()
        QtCore.QTimer.singleShot(delay_popup, lambda: self.show_processing_window(long_process_thread))

    @staticmethod
    def simulate_long_process(duration=None):
        print("before")
        if duration:
            time.sleep(duration)  # Simulating a long process
        print(f"after {duration} seconds")

    def show_processing_window(self, long_process_thread):
        if not long_process_thread.isFinished():
            self.processing_window = ProcessingWindow(self)
            self.processing_window.center()
            self.processing_window.show()

    def enable_button(self):
        if self.processing_window is not None:
            self.processing_window.close()
        self.button.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())