from enum import Enum

from ester_mastal.ui.menu import EnumMenu

from ..main import App


class MenuCommand(Enum):
    Item = "アイテム"
    Spell = "じゅもん"
    Status = "つよさ"


class MenuMode:
    def __init__(self, app: App):
        self.player = app.player
        self._default_window = EnumMenu(10, 20, 60, list(MenuCommand), app.font)

    def update(self):
        command = self._default_window.update()

    def draw(self):
        self._default_window.draw()