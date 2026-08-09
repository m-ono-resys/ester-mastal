from .base_mode import BaseMode
from .signals import ModeSignal


class MainMenuMode(BaseMode):
    def update(self):
        return ModeSignal()

    def draw(self):
        pass