
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog
from PySide6.QtGui import QPdfWriter, QAction
from PySide6.QtPrintSupport import QPrinter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        save_as_pdf_action = QAction("Save as PDF", self)
        save_as_pdf_action.triggered.connect(self.save_as_pdf)
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(save_as_pdf_action)

    def save_as_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as PDF", "", "PDF Files (*.pdf)")
        if file_path:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            writer = QPdfWriter(file_path)
            self.text_edit.document().print_(printer)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())