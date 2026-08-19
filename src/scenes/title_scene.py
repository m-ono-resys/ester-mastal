import pyxel

from data.maps import MapId
from models.item import ItemCode
from models.spell import SpellCode
from ui.input import is_confirm

from .base_scene import BaseScene
from .field.mode.message_mode import MessageMode, MessageModeData


class TitleScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)
        self.app.player = self.app.repo.create_initial_player("といろ")
        self.app.flags.clear()

        # デバッグ用
        # self.app.player = self.app.repo.create_initial_player("デバッグ", 4)
        # self.app.player.x = 4
        # self.app.player.y = 3
        # self.app.player.map_id = MapId.DEMON_CASTLE_3F
        # self.app.player.gold = 1000
        # self.app.player.spells = [
        #     SpellCode.IMARU,
        #     SpellCode.IRAMEI,
        #     SpellCode.AIMETO,
        #     SpellCode.MASARA,
        # ]
        # self.app.player.inventory = [
        #     ItemCode.KING_ARMOR,
        #     ItemCode.KING_SWORD,
        #     ItemCode.IRON_ARMOR,
        #     ItemCode.COPPER_SWORD,
        #     ItemCode.POTION,
        #     ItemCode.POTION,
        #     ItemCode.POTION,
        #     ItemCode.POTION,
        #     ItemCode.POTION,
        #     ItemCode.POTION,
        # ]

    def update(self):
        # 決定キーでゲーム開始
        if is_confirm():
            from .field.field_scene import FieldScene

            field_scene = FieldScene(self.app)
            field_scene.current_event = MessageModeData(
                name="おかあさん",
                messages=[
                    "むかし、大まおうが、おうちにはいってきて、ゆうしゃを見つける どうぐ を おうちの中のどこかにいれたんだ。",
                    "だから ごめんだけど、おうちには入っちゃダメ。",
                    "それで、おしろの王さまが ま王をやっつけてくれといっていたから、",
                    "まずは、きたにあるおしろにいけばいいよ。",
                ],
            )
            field_scene.mode_stack.append(MessageMode(field_scene.context))

            self.app.change_state(field_scene)

    def draw(self):
        pyxel.cls(0)  # 黒でクリア
        pyxel.blt(0, 24, 0, 0, 160, 192, 128, 0)

        # 点滅表示（フレーム数で制御）
        if (pyxel.frame_count // 15) % 2 == 0:
            pyxel.text(40, 128, "きめるボタンではじめる", 7, self.app.font)
