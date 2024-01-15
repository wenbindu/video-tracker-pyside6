import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QSlider)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗体标题
        self.setWindowTitle("V1.0")

        # 创建视频播放组件
        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(320, 240)  # 设置视频播放组件的大小

        # 创建媒体播放器
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)

        # 创建进度条
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.slider)

        # 创建容器控件并设置布局
        container = QWidget()
        container.setLayout(layout)

        # 将容器控件设置为窗体的中心控件
        self.setCentralWidget(container)

        # 连接视频播放组件的点击事件
        self.video_widget.mousePressEvent = self.video_widget_clicked

        # 连接媒体播放器的信号
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)

    # 视频播放组件的点击事件处理函数
    def video_widget_clicked(self, event):
        filename, _ = QFileDialog.getOpenFileName(self, "上传视频文件", "", "视频文件 (*.mp4 *.avi)")
        if filename:
            # 设置媒体播放器的媒体源为选中的视频文件
            self.media_player.setSource(QUrl.fromLocalFile(filename))
            # 开始播放视频
            self.media_player.play()

    # 更新进度条的最大值
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    # 更新进度条的当前值
    def position_changed(self, position):
        self.slider.setValue(position)

    # 设置媒体播放器的播放位置
    def set_position(self, position):
        self.media_player.setPosition(position)

# 创建应用程序实例
app = QApplication(sys.argv)

# 实例化窗体并显示
window = MainWindow()
window.show()

# 运行应用程序的事件循环
sys.exit(app.exec())