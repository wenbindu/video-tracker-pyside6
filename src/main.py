from sqlite3 import Time
import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox
)
from analyse import frame_generator
from core import logger
from analyse import get_video_info
from PySide6.QtCore import QTimer



root_path = os.path.dirname(os.path.realpath(__file__))



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗体标题
        self.setWindowTitle("视频分析系统V1.0")
        # set width/height
        self.setFixedSize(800, 470)
        # 创建视频
        self.video_list = QListWidget(self)
        # self.upload_video_label = ClickableLabel()
        self.video_list.setFixedSize(500, 400)  # 设置视频框的大小
        self.video_list.setStyleSheet(
            "QListWidget { background: grey; border: 1px;}"
            "QListWidget::item {"
            "border-style: solid;"
            "border-width:1px;"
            "border-color:  black;"
            "margin-right: 10px;"
            "}"
            "QListWidget::item:hover {"
            "border-color: green;"
            "}"
        )

        # 创建文本框
        self.analysis_result_text = QTextEdit()
        self.analysis_result_text.setReadOnly(True)  # 设置文本框为只读
        self.analysis_result_text.show()

        # 创建按钮
        self.upload_button = QPushButton("上传视频", self)
        self.upload_button.clicked.connect(self.upload_videos)

        self.analyze_button = QPushButton("分析视频", self)
        self.analyze_button.clicked.connect(self.analyze_videos)

        self.export_button = QPushButton("导出结果", self)
        self.export_button.clicked.connect(self.export_result)

        self.clear_button = QPushButton("清空列表", self)
        self.clear_button.clicked.connect(self.clear_text)

        # 创建布局
        video_text_layout = QHBoxLayout()
        video_text_layout.addWidget(self.video_list)
        video_text_layout.addWidget(self.analysis_result_text)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.upload_button)
        buttons_layout.addWidget(self.analyze_button)
        buttons_layout.addWidget(self.export_button)
        buttons_layout.addWidget(self.clear_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(video_text_layout)
        main_layout.addLayout(buttons_layout)
        # 创建容器控件并设置布局
        container = QWidget()
        container.setLayout(main_layout)
        # 将容器控件设置为窗体的中心控件
        self.setCentralWidget(container)
        # timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.analyze_videos)
    
    def show_error_message(self):
        # Create a QMessageBox with an error type
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("错误")
        error_box.setText("An error occurred!")
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()

    # 槽函数：上传视频文件
    def upload_videos(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "上传视频", "", "视频文件 (*.mp4 *.avi)"
        )

        # Add items to the QListWidget
        item = QListWidgetItem()
        item_widget = QWidget()
        line_text = QLabel(filename)
        rm_btn = QPushButton("移除")
        rm_btn.setObjectName(str(self.video_list.count()))
        rm_btn.setFixedWidth(90)
        rm_btn.clicked.connect(self.rm_clicked)
        item_layout = QHBoxLayout()
        item_layout.addWidget(rm_btn)
        item_layout.addWidget(line_text)
        item_widget.setLayout(item_layout)
        item.setSizeHint(item_widget.sizeHint())
        self.video_list.addItem(item)
        self.video_list.setItemWidget(item, item_widget)

        if filename:
            # 这里添加上传视频文件的逻辑
            self.analysis_result_text.append(f"已选择视频文件：{filename}\n")

    # 槽函数：清除文本框内容
    def clear_text(self):
        self.analysis_result_text.clear()
        self.video_list.clear()

    # 槽函数：分析视频
    def analyze_videos(self):
        # 这里添加分析视频的逻辑
        self.analysis_result_text.append("开始分析视频...\n")
        items = []
        for x in range(self.video_list.count()):
            item_at_index = self.video_list.item(x)
            widget_in_item = self.video_list.itemWidget(item_at_index)
            label_in_widget = widget_in_item.findChild(QLabel)
            if label_in_widget is not None:
                label_text = label_in_widget.text()
                items.append(label_text)
            else:
                logger.error(f"there is no label: {item_at_index}")
        
        logger.info(f"all the videos: {items}")
        # begin the timer
        self.timer.start(1000)
        # justify the exist for every row in items.
        for _item in items:
            self.analysis_result_text.append(f"开始分析:{_item}")
            if not os.path.exists(_item):
                logger.error(f"文件[{_item}]不存在")
                self.analysis_result_text.append(f"异常:{_item} 文件不存在")
            # get video info
            vinfo = get_video_info(_item)
            self.analysis_result_text.append(f"width: {vinfo.width}, \nheight: {vinfo.height}, \nfps: {vinfo.fps}, \ntotalFrames:{vinfo.total_frames}")
            # analyse video with model.
            for idx_frame, ret_frame in frame_generator(_item, stripe=5):
                logger.info(idx_frame)
                self.analysis_result_text.append(f"{idx_frame}: {ret_frame}")
            
        self.timer.stop()
        

    def export_result(self):
        self.analysis_result_text.append("开始导出分析结果...\n")

    def rm_clicked(self):
        sender_button = self.sender()
        # Find the item associated with the button
        widget = sender_button.parentWidget()
        item = self.video_list.itemAt(widget.pos())
        widget_in_item = self.video_list.itemWidget(item)
        label_in_widget = widget_in_item.findChild(QLabel)
        if label_in_widget is not None:
            label_text = label_in_widget.text()
            logger.info(f"Label text for removed item: {label_text}")
        else:
            label_text = None
            logger.error(f"the label not exist in item: {item}")

        # Remove the item from the QListWidget
        if item is not None:
            row = self.video_list.row(item)
            self.video_list.takeItem(row)
            self.analysis_result_text.append(f"移除:{label_text}\n")

    def play(self):
        """测试"""
        # Add items to the QListWidget
        filename = "/Users/dean/Downloads/2023.12.02修改版.mp4"
        item = QListWidgetItem()
        item_widget = QWidget()
        line_text = QLabel(filename)
        rm_btn = QPushButton("移除")
        rm_btn.setObjectName(str(self.video_list.count()))
        rm_btn.setFixedWidth(90)
        rm_btn.clicked.connect(self.rm_clicked)
        item_layout = QHBoxLayout()
        item_layout.addWidget(rm_btn)
        item_layout.addWidget(line_text)
        item_widget.setLayout(item_layout)
        item.setSizeHint(item_widget.sizeHint())
        self.video_list.addItem(item)
        self.video_list.setItemWidget(item, item_widget)
        # self.show_error_message()




# 创建应用程序实例
app = QApplication(sys.argv)

# 实例化窗体并显示
window = MainWindow()
window.show()
# window.play()

# 运行应用程序的事件循环
sys.exit(app.exec())
