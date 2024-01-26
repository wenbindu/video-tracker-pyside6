import sys
import os

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
    QPlainTextEdit
)
from PySide6.QtGui import QCloseEvent
from videotrackersystem.analyse import frame_generator
from videotrackersystem.core import logger
from videotrackersystem.analyse import get_video_info


root_path = os.path.dirname(os.path.realpath(__file__))



class VideoTrackerSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
    
    def init_ui(self):
        # set window title
        self.setWindowTitle("视频分析系统V1.0")
        # set width/height
        self.setFixedSize(800, 470)
        # video list
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
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)  # 设置文本框为只读

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
        video_text_layout.addWidget(self.text)

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
        
    def message(self, s):
        self.text.appendPlainText(s)
    
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
            self.message(f"已选择视频文件：{filename}")

    # 槽函数：清除文本框内容
    def clear_text(self):
        self.text.clear()
        self.video_list.clear()

    # 槽函数：分析视频
    def analyze_videos(self):
        # 这里添加分析视频的逻辑
        self.message("开始分析视频...")
        self.analyze_button.setEnabled(False)
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
        # justify the exist for every row in items.
        # for _item in items:
        #     self.message(f"开始分析:{_item}")
        #     if not os.path.exists(_item):
        #         logger.error(f"文件[{_item}]不存在")
        #         self.message(f"异常:{_item} 文件不存在")
        #     # get video info
        #     vinfo = get_video_info(_item)
        #     self.message(f"width: {vinfo.width}, \nheight: {vinfo.height}, \nfps: {vinfo.fps}, \ntotalFrames:{vinfo.total_frames}")
        #     # analyse video with model.
        #     for idx_frame, ret_frame in frame_generator(_item, stripe=5):
        #         logger.info(idx_frame)
        #         self.message(f"{idx_frame}: {ret_frame}")
        self.analyze_button.setEnabled(True)
            
        

    def export_result(self):
        self.message("开始导出分析结果...\n")

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
            self.text(f"移除:{label_text}")
    
    def closeEvent(self, event: QCloseEvent):
        # reply = QMessageBox.question(self, '信息', '你确定要退出吗?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('提示')
        box.setText('确定要退出吗?')
        box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('是')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('否')
        box.exec_()

        if box.clickedButton() == buttonY:
            event.accept()
        else:
            event.ignore()

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


# # 创建应用程序实例
# app = QApplication(sys.argv)

# # 实例化窗体并显示
# window = MainWindow()
# window.show()
# # window.play()

# # 运行应用程序的事件循环
# sys.exit(app.exec())


def main():
    # Linux desktop environments use app's .desktop file to integrate the app
    # to their application menus. The .desktop file of this app will include
    # StartupWMClass key, set to app's formal name, which helps associate
    # app's windows to its menu item.
    #
    # For association to work any windows of the app must have WMCLASS
    # property set to match the value set in app's desktop file. For PySide2
    # this is set with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules['__main__'].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    QApplication.setApplicationName(metadata['Formal-Name'])

    app = QApplication(sys.argv)
    main_window = VideoTrackerSystem()
    main_window.show()
    sys.exit(app.exec())