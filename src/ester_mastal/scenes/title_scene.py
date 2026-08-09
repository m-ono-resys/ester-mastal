import pyxel

from .base_scene import BaseScene


class TitleScene(BaseScene):
    def update(self):
        # SPACEキーまたはZキーでゲーム開始
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z):
            from .field.field_scene import FieldScene

            # プレイヤー初期化してフィールドへ
            # self.app.player = self.app.repo.create_initial_player("ゆうしゃ")
            self.app.change_state(FieldScene(self.app))

    def draw(self):
        pyxel.cls(0)  # 黒でクリア
        pyxel.text(50, 40, "DRAGON QUEST 1-LIKE", 10)

        # 点滅表示（フレーム数で制御）
        if (pyxel.frame_count // 15) % 2 == 0:
            pyxel.text(42, 80, "PRESS SPACE TO START", 7)
