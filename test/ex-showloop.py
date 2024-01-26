from PySide6.QtWidgets import QApplication, QTextEdit
from PySide6.QtCore import QTimer
import time

def text_generator():
    # A sample generator that yields lines of text.
    for i in range(10):
        yield f'Line {i+1}\n'

generator = text_generator()

app = QApplication([])

text_edit = QTextEdit()
text_edit.show()

def append_text():
    try:
        next_line = next(generator)
        text_edit.append(next_line)
        text_edit.append(next_line)
        text_edit.append(next_line)
        print("tet")
    except StopIteration:
        timer.stop()  # stop the timer when the generator is exhausted

timer = QTimer()
timer.timeout.connect(append_text)
timer.start(1000)  # generate a new line every 1 second

app.exec()