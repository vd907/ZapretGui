# core/opengl.py
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QSurfaceFormat, QOpenGLContext
from core.config_loader import ConfigLoader


class OpenGL:

    @staticmethod
    def setup():
        cfg = ConfigLoader.get("opengl")
        if not cfg.get("enabled", True):
            return

        format = QSurfaceFormat()
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.CompatibilityProfile)
        format.setRenderableType(QSurfaceFormat.OpenGL)
        format.setSamples(cfg.get("samples", 2) if cfg.get("use_msaa", True) else 0)
        format.setSwapInterval(0)
        format.setDepthBufferSize(cfg.get("depth_buffer_size", 24))
        format.setStencilBufferSize(cfg.get("stencil_buffer_size", 8))
        format.setSwapBehavior(QSurfaceFormat.DoubleBuffer)

        QSurfaceFormat.setDefaultFormat(format)

    @staticmethod
    def info():
        ctx = QOpenGLContext()
        if ctx.create():
            f = ctx.format()
            swap = f.swapInterval()
            print(
                f"OpenGL {f.majorVersion()}.{f.minorVersion()} | MSAA x{f.samples()} | V-Sync {'On' if swap > 0 else 'Off'}")