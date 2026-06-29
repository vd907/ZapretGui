# ui/animations/side_menu.py
from PySide6.QtCore import QPropertyAnimation, QEasingCurve


class SideMenuAnimation:

    DURATION = 300

    def __init__(self, target):
        self._target = target
        self._anim = None

    def toggle(self, expanded: bool, width_expanded: int, width_collapsed: int):
        if self._anim and self._anim.state() == QPropertyAnimation.Running:
            return

        self._anim = QPropertyAnimation(self._target, b"minimumWidth")
        self._anim.setDuration(self.DURATION)
        self._anim.setEasingCurve(QEasingCurve.InOutCubic)

        if expanded:
            self._anim.setStartValue(width_expanded)
            self._anim.setEndValue(width_collapsed)
        else:
            self._anim.setStartValue(width_collapsed)
            self._anim.setEndValue(width_expanded)

        self._anim.finished.connect(self._on_finished)
        self._anim.start()

    def _on_finished(self):
        if hasattr(self._target, '_on_animation_finished'):
            self._target._on_animation_finished()