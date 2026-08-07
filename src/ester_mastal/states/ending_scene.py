import pyxel

from ..audio import play_se
from ..ui.window import draw_window
from .base_scene import BaseScene


class EndingScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        play_se(3)  # ★ 勝利ファンファーレ再生！
        self.frame_timer = 0

    def update(self):
        self.frame_timer += 1
        # 2秒経過したらSPACE/Zキーでタイトルへ戻る
        if self.frame_timer > 60 and (
            pyxel.btnp(pyxel.KEY_Z)
            or pyxel.btnp(pyxel.KEY_SPACE)
            or pyxel.btnp(pyxel.KEY_RETURN)
        ):
            from .title_scene import TitleScene

            self.app.change_state(TitleScene(self.app))

    def draw(self):
        pyxel.cls(0)
        draw_window(10, 20, 172, 152)

        pyxel.text(48, 35, "～ せかい の へいわ ～", 10, self.app.font)

        pyxel.text(24, 60, "りゅうおう は たおれた！", 7, self.app.font)
        pyxel.text(24, 76, "せかい に へいわ が もどった！", 7, self.app.font)
        pyxel.text(24, 92, "ありがとう たびの ゆうしゃよ！", 7, self.app.font)

        pyxel.text(52, 125, "CONGRATULATIONS!", 11, self.app.font)

        if (self.frame_timer // 15) % 2 == 0:
            pyxel.text(28, 150, "PRESS SPACE TO TITLE", 7, self.app.font)
