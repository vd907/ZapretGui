# ============================================================
# __init__.py (корень)
# ============================================================
from .core.app import App
from .core.config_loader import ConfigLoader
from .core.opengl import OpenGL
from .ui.mainwindow.main_window import MainWindow
from .ui.widgets.side_menu import SideMenu
from .ui.pages.main_page import MainPage
from .ui.pages.settings_page import SettingsPage
from .ui.widgets.power_button import PowerButton
from .ui.animations.animation_side_menu import SideMenuAnimation
from .ui.animations.animation_manager import AnimationManager

__all__ = [
    "App",
    "ConfigLoader",
    "OpenGL",
    "MainWindow",
    "SideMenu",
    "MainPage",
    "SettingsPage",
    "PowerButton",
    "SideMenuAnimation",
    "AnimationManager",
]