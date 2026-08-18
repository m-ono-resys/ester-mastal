import pyxel

from audio import play_se
from ui.input import is_confirm
from ui.window import draw_window

from .base_scene import BaseScene


class EndingScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        # play_se(3)  # ★ 勝利ファンファーレ再生！
        self.frame_timer = 0

    def update(self):
        self.frame_timer += 1
        # 2秒経過したらSPACE/Zキーでタイトルへ戻る
        if self.frame_timer > 60 and is_confirm():
            from .title_scene import TitleScene

            self.app.change_state(TitleScene(self.app))

    def draw(self):
        pyxel.cls(0)
        draw_window(10, 20, 172, 152)

        pyxel.text(40, 35, "～ せかい の へいわ ～", 10, self.app.font)

        pyxel.text(24, 60, "まおうデラミール は たおれた！", 7, self.app.font)
        pyxel.text(24, 76, "せかい に へいわ が もどった！", 7, self.app.font)
        pyxel.text(24, 92, "ありがとう ゆうしゃ トイロよ！", 7, self.app.font)

        pyxel.text(32, 125, "あそんでくれてありがとう！", 11, self.app.font)

        if (self.frame_timer // 15) % 2 == 0:
            pyxel.text(19, 150, "きめるボタンで さいしょにもどる", 7, self.app.font)
