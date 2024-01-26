import logging
from PySide6.QtWidgets import QApplication
from qt_window_logger import QtWindowHandler


def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    f = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    window_handler = QtWindowHandler()
    window_handler.setFormatter(f)
    logger.addHandler(window_handler)

    logger = logging.getLogger(__name__)
    logger.debug("test debug")
    logger.info("test info")
    logger.warning("test warn")
    app.exec()

if __name__ == "__main__":
    app = QApplication()
    main()