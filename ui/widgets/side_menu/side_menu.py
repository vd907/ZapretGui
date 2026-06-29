# ui/widgets/side_menu/side_menu.py
from pathlib import Path
from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import QSize, Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon
from core.config_loader import ConfigLoader
from ui.animations.side_menu import SideMenuAnimation


class SideMenu(QFrame):
    ICONS = Path(__file__).parent.parent.parent.parent / "assets" / "icons"
    expanded_changed = Signal(bool)

    def __init__(self, switch_callback=None, parent=None):
        super().__init__(parent)
        self.setObjectName("sideMenu")
        self._expanded = False
        self._switch_callback = switch_callback

        self._cfg = ConfigLoader.get("side_menu")
        self._cfg_settings = ConfigLoader.get("settings")
        self._btn_size = self._cfg.get("button_size", 40)
        self._border_radius = self._cfg.get("border_radius", 8)
        self._margin_left = self._cfg.get("margin_left", 5)
        self._label_animation = None

        self.setAttribute(Qt.WA_AlwaysStackOnTop, True)
        self._setup_ui()
        self._animation = SideMenuAnimation(self)
        self._update_icon()

    def _setup_ui(self):
        self.setStyleSheet("#sideMenu { background-color: #e0e0e0; border-right: 1px solid #bdbdbd; }")

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(self._cfg.get("spacing", 2))
        self._layout.addSpacing(8)

        self._toggle_btn = self._create_icon_button("menuToggle", self._cfg.get("icon_size", 24))
        self._toggle_btn.clicked.connect(self._toggle)
        self._add_widget(self._toggle_btn)

        self._settings_container = QWidget()
        self._settings_container.setObjectName("settingsContainer")
        self._settings_container.setFixedHeight(self._btn_size)
        self._settings_container.setFixedWidth(self._btn_size)

        settings_layout = QHBoxLayout(self._settings_container)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setSpacing(8)
        settings_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self._settings_btn = QPushButton()
        self._settings_btn.setIcon(QIcon(str(self.ICONS / "settings.svg")))
        self._settings_btn.setIconSize(
            QSize(self._cfg_settings.get("icon_size", 20), self._cfg_settings.get("icon_size", 20)))
        self._settings_btn.setFixedSize(self._btn_size, self._btn_size)
        self._settings_btn.setStyleSheet("background: transparent; border: none;")
        self._settings_btn.clicked.connect(self._open_settings)
        settings_layout.addWidget(self._settings_btn)

        self._settings_label = QLabel(ConfigLoader.get_text("settings", "page_title"))
        self._settings_label.setStyleSheet("color: #333; font-size: 14px; background: transparent;")
        self._settings_label.setVisible(False)
        self._settings_label.setMinimumWidth(0)
        self._settings_label.setMaximumWidth(120)
        settings_layout.addWidget(self._settings_label)

        self._settings_container.setStyleSheet(f"""
            #settingsContainer {{
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: {self._border_radius}px;
            }}
            #settingsContainer:hover {{
                background-color: #f5f5f5;
                border-color: #bdbdbd;
            }}
        """)

        self._add_widget(self._settings_container)
        self._layout.addStretch()
        self._settings_page = None

    def _create_icon_button(self, name, icon_size):
        btn = QPushButton()
        btn.setObjectName(name)
        btn.setIconSize(QSize(icon_size, icon_size))
        btn.setFixedSize(self._btn_size, self._btn_size)
        btn.setStyleSheet(f"""
            QPushButton#{name} {{
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-radius: {self._border_radius}px;
                padding: 8px;
            }}
            QPushButton#{name}:hover {{
                background-color: #f5f5f5;
                border-color: #bdbdbd;
            }}
        """)
        return btn

    def _add_widget(self, w):
        container = QWidget()
        container.setFixedHeight(self._btn_size)
        layout = QHBoxLayout(container)
        layout.setContentsMargins(self._margin_left, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(w)
        self._layout.addWidget(container, 0, Qt.AlignLeft)

    def _toggle(self):
        self._animation.toggle(self._expanded, self._cfg.get("width_expanded", 200),
                               self._cfg.get("width_collapsed", 50))

    def _on_animation_finished(self):
        self._expanded = not self._expanded
        self._update_icon()
        self._animate_label()
        self.expanded_changed.emit(self._expanded)

    def _animate_label(self):
        if self._label_animation and self._label_animation.state() == QPropertyAnimation.Running:
            self._label_animation.stop()

        if self._expanded:
            self._settings_label.setVisible(True)
            self._label_animation = QPropertyAnimation(self._settings_container, b"minimumWidth")
            self._label_animation.setDuration(250)
            self._label_animation.setEasingCurve(QEasingCurve.OutCubic)
            self._label_animation.setStartValue(self._btn_size)
            self._label_animation.setEndValue(160)
            self._label_animation.start()
        else:
            self._label_animation = QPropertyAnimation(self._settings_container, b"minimumWidth")
            self._label_animation.setDuration(200)
            self._label_animation.setEasingCurve(QEasingCurve.InCubic)
            self._label_animation.setStartValue(160)
            self._label_animation.setEndValue(self._btn_size)
            self._label_animation.finished.connect(lambda: self._settings_label.setVisible(False))
            self._label_animation.start()

    def _open_settings(self):
        if self._settings_page is None:
            from ui.widgets.pages.settings_page import SettingsPage
            self._settings_page = SettingsPage()
            self._settings_page.setWindowTitle(ConfigLoader.get_text("settings", "window_title"))
            self._settings_page.resize(400, 300)
            self._settings_page.setAttribute(Qt.WA_DeleteOnClose)
            self._settings_page.destroyed.connect(lambda: setattr(self, '_settings_page', None))
        self._settings_page.show()

    def _icon_path(self) -> Path:
        return self.ICONS / ("menu.svg" if self._expanded else "arrow.svg")

    def _update_icon(self):
        self._toggle_btn.setIcon(QIcon(str(self._icon_path())))