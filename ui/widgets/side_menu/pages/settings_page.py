# ui/widgets/pages/settings_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from core.config_loader import ConfigLoader


class SettingsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setObjectName("settingsPage")
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        title = QLabel(ConfigLoader.get_text("settings", "page_title"))
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        layout.addStretch()

        back_btn = QPushButton(ConfigLoader.get_text("settings", "back_button"))
        back_btn.setObjectName("backButton")
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)