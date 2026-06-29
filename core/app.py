# core/app.py
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from core.config_loader import ConfigLoader
from ui.mainwindow.main_window import MainWindow


class App:

    ICONS = Path(__file__).parent.parent / "assets" / "icons"

    def __init__(self):
        self._apply_qss()
        self._apply_icon()
        self._window = MainWindow()

    def _apply_qss(self):
        qss = ConfigLoader.qss()
        if qss:
            QApplication.instance().setStyleSheet(qss)

    def _apply_icon(self):
        QApplication.instance().setWindowIcon(QIcon(str(self.ICONS / "app.ico")))

    def show(self):
        self._window.show()