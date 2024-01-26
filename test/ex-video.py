import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super(ClickableLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText("点击此处上传视频")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #00f;
                background-color: #ddd;
            }
            QLabel:hover {
                background-color: #ddf;
            }
        """)

    def mousePressEvent(self, event):
        filename, _ = QFileDialog.getOpenFileName(self, "上传视频文件", "", "视频文件 (*.mp4 *.avi)")
        if filename:
            # 这里添加上传视频文件的逻辑
            # 例如，你可以在这里设置视频预览或者存储文件路径等
            print(f"已选择视频文件：{filename}")
            # 如果你想显示视频的缩略图，可以使用 QPixmap 设置 QLabel 的图片
            # pixmap = QPixmap(filename)
            # self.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))