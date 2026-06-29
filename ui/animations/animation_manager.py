# ui/animations/animation_manager.py
from PySide6.QtCore import QTimer


class AnimationManager:

    FPS = 90
    INTERVAL = 1000 // FPS

    def __init__(self):
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_frame)
        self._start_value = 0
        self._end_value = 0
        self._current_step = 0
        self._total_steps = 0
        self._callback = None
        self._duration = 400

    def start(self, start_value, end_value, duration=400, callback=None):
        if self._timer.isActive():
            self._timer.stop()

        self._start_value = start_value
        self._end_value = end_value
        self._current_step = 0
        self._duration = duration
        self._total_steps = max(1, duration // self.INTERVAL)
        self._callback = callback

        self._timer.start(self.INTERVAL)

    def stop(self):
        self._timer.stop()

    def is_running(self):
        return self._timer.isActive()

    def _update_frame(self):
        self._current_step += 1

        if self._current_step >= self._total_steps:
            self._on_update(self._end_value)
            self._timer.stop()
            if self._callback:
                self._callback()
        else:
            progress = self._current_step / self._total_steps
            eased_progress = self._ease_out_expo(progress)
            current_value = self._start_value + (self._end_value - self._start_value) * eased_progress
            self._on_update(current_value)

    def _on_update(self, value):
        pass

    @staticmethod
    def _ease_out_expo(t):
        if t >= 1.0:
            return 1.0
        return 1.0 - pow(2.0, -10.0 * t)

    @staticmethod
    def _ease_in_out_cubic(t):
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2