# main.py
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QSurfaceFormat
from core.app import App
from core.opengl import OpenGL
from core.config_loader import ConfigLoader


def main():
    os.environ["QT_OPENGL_NO_VSYNC"] = "1"
    os.environ["vblank_mode"] = "0"
    os.environ["__GL_SYNC_TO_VBLANK"] = "0"

    cfg = ConfigLoader.get("opengl")

    if cfg.get("enabled", True):
        format = QSurfaceFormat()
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.CompatibilityProfile)
        format.setRenderableType(QSurfaceFormat.OpenGL)
        format.setSamples(cfg.get("samples", 2) if cfg.get("use_msaa", True) else 0)
        format.setSwapInterval(0)
        format.setDepthBufferSize(24)
        format.setStencilBufferSize(8)
        format.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
        QSurfaceFormat.setDefaultFormat(format)
        QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)

    app = QApplication(sys.argv)

    if cfg.get("enabled", True):
        OpenGL.info()

    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()