import pyxel

from .base_state import BaseState


class GameOverState(BaseState):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z):
            from .title_state import TitleState

            self.app.change_state(TitleState(self.app))

    def draw(self):
        pyxel.cls(0)
        pyxel.text(60, 50, "GAME OVER", 8)
        pyxel.text(40, 80, "PRESS SPACE TO TITLE", 7)
