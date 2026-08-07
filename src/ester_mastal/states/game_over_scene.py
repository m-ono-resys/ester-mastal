import pyxel

from .base_scene import BaseScene


class GameOverScene(BaseScene):
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z):
            from .title_scene import TitleScene

            self.app.change_state(TitleScene(self.app))

    def draw(self):
        pyxel.cls(0)
        pyxel.text(60, 50, "GAME OVER", 8)
        pyxel.text(40, 80, "PRESS SPACE TO TITLE", 7)
