import pyxel

from .base_scene import BaseScene


class TitleScene(BaseScene):
    def update(self):
        # SPACEキーまたはZキーでゲーム開始
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z):
            from .field.field_scene import FieldScene

            self.app.change_state(FieldScene(self.app))

    def draw(self):
        pyxel.cls(0)  # 黒でクリア
        # pyxel.text(50, 40, "エスターマスタル", 10, self.app.font)
        pyxel.blt(0, 24, 0, 0, 160, 192, 128, 0)

        # 点滅表示（フレーム数で制御）
        if (pyxel.frame_count // 15) % 2 == 0:
            pyxel.text(36, 128, "けっていボタンではじめる", 7, self.app.font)
