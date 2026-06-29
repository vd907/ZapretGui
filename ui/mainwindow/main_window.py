# ui/mainwindow/main_window.py
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QApplication
from PySide6.QtGui import QFont
from core.config_loader import ConfigLoader
from ui.widgets.side_menu.side_menu import SideMenu
from ui.widgets.pages.main_page import MainPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_fonts()
        self._setup_ui()

    def _setup_window(self):
        w = ConfigLoader.get("window")
        self.setWindowTitle(w.get("title"))
        self.setGeometry(w.get("x"), w.get("y"), w.get("width"), w.get("height"))

    def _setup_fonts(self):
        f = ConfigLoader.get("fonts")
        QApplication.instance().setFont(QFont(f.get("family"), f.get("size")))

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._stack = QStackedWidget()
        self._stack.setObjectName("contentArea")

        self._main_page = MainPage()
        self._main_page.set_power_callback(self._on_power_toggle)
        self._stack.addWidget(self._main_page)
        layout.addWidget(self._stack)

        self._menu = SideMenu(switch_callback=self._switch_page)
        self._menu.setParent(central)
        self._menu.setGeometry(0, 0, ConfigLoader.get("side_menu", "width_collapsed"), self.height())
        self._menu.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, '_menu') and self._menu:
            self._menu.setGeometry(0, 0, self._menu.width(), self.height())

    def _on_power_toggle(self):
        self._main_page.update_status(self._main_page.toggle_power())

    def _switch_page(self, index: int):
        while self._stack.count() <= index:
            self._stack.addWidget(QWidget())
        self._stack.setCurrentIndex(index)