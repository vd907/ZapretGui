# ui/widgets/power_button.py
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon


class PowerButton(QPushButton):

    def __init__(self, start_icon=None, stop_icon=None, parent=None):
        super().__init__(parent)
        self._is_running = False
        self._icon_start = start_icon
        self._icon_stop = stop_icon

        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
        """)

        if self._icon_start and not self._icon_start.isNull():
            self.setIcon(self._icon_start)

    def _update_state(self):
        if self._is_running:
            if self._icon_stop and not self._icon_stop.isNull():
                self.setIcon(self._icon_stop)
        else:
            if self._icon_start and not self._icon_start.isNull():
                self.setIcon(self._icon_start)

    def toggle(self):
        self._is_running = not self._is_running
        self._update_state()
        return self._is_running

    def is_running(self):
        return self._is_running