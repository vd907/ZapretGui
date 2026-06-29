# ============================================================
# ui/pages/main_page.py
# ============================================================
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from core.config_loader import ConfigLoader
from ui.widgets.power_button import PowerButton


class MainPage(QWidget):
    ICONS = Path(__file__).parent.parent.parent / "assets" / "icons"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("mainPage")
        self._setup_ui()

    def _setup_ui(self):
        cfg = ConfigLoader.get("power_button")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._text_stopped = ConfigLoader.get_text("status", "stopped")
        self._text_running = ConfigLoader.get_text("status", "running")

        layout.addStretch()

        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(20)
        center_layout.setAlignment(Qt.AlignCenter)

        start_icon = QIcon(str(self.ICONS / "power.svg"))
        stop_icon = QIcon(str(self.ICONS / "stop.svg"))

        self._power_btn = PowerButton(start_icon, stop_icon)
        self._power_btn.setIconSize(QSize(cfg.get("icon_size", 64), cfg.get("icon_size", 64)))
        self._power_btn.setFixedSize(cfg.get("button_size", 80), cfg.get("button_size", 80))

        center_layout.addWidget(self._power_btn, 0, Qt.AlignCenter)

        self._status_label = QLabel(self._text_stopped)
        self._status_label.setObjectName("statusLabel")
        self._status_label.setAlignment(Qt.AlignCenter)

        center_layout.addWidget(self._status_label, 0, Qt.AlignCenter)
        layout.addWidget(center, 0, Qt.AlignCenter)
        layout.addStretch()

    def set_power_callback(self, callback):
        if callback:
            self._power_btn.clicked.connect(callback)

    def update_status(self, is_running):
        self._status_label.setText(self._text_running if is_running else self._text_stopped)
        self._status_label.setStyleSheet(f"""
            QLabel#statusLabel {{
                font-size: 14px;
                color: {'#4caf50' if is_running else '#f44336'};
                padding: 10px;
            }}
        """)

    def toggle_power(self):
        return self._power_btn.toggle()