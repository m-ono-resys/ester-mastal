import random

import pyxel

from ..ui.message_box import MessageBox
from ..ui.window import draw_window
from .base_state import BaseState


class FieldState(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.grid_size = 8
        self.player_x = 10  # マス目座標
        self.player_y = 7
        self.step_count = 0

        # モード管理: "EXPLORE", "MAIN_MENU", "SPELL_MENU", "ITEM_MENU", "STATS_MENU", "MESSAGE"
        self.mode = "EXPLORE"

        self.cursor = 0  # メインメニュー用カーソル (0:じゅもん, 1:つよさ, 2:どうぐ)
        self.sub_cursor = 0  # サブメニュー用カーソル

        # メッセージボックス（UI）
        self.msg_box = MessageBox(
            x=10, y=65, width=140, height=45, speed=2, font=self.app.font
        )

    def update(self):
        if self.mode == "EXPLORE":
            moved = False
            # 上下左右移動
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
                self.player_y -= 1
                moved = True
            elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
                self.player_y += 1
                moved = True
            elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
                self.player_x -= 1
                moved = True
            elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
                self.player_x += 1
                moved = True

            if moved:
                # 画面端のバウンド
                self.player_x = max(1, min(18, self.player_x))
                self.player_y = max(1, min(13, self.player_y))

                # ランダムエンカウント判定（約15%の確率）
                if random.random() < 0.15:
                    self.trigger_battle()

            # XキーまたはESCキーでメニューを開く
            if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.mode = "MAIN_MENU"
                self.cursor = 0

        # --- 2. メインメニュー選択 ---
        elif self.mode == "MAIN_MENU":
            if pyxel.btnp(pyxel.KEY_UP):
                self.cursor = (self.cursor - 1) % 3
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.cursor = (self.cursor + 1) % 3

            # XキーまたはESCでメニューを閉じる
            if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.mode = "EXPLORE"

            # 決定
            elif (
                pyxel.btnp(pyxel.KEY_Z)
                or pyxel.btnp(pyxel.KEY_SPACE)
                or pyxel.btnp(pyxel.KEY_RETURN)
            ):
                p = self.app.player
                if self.cursor == 0:  # じゅもん
                    if not p.spells:
                        self.msg_box.push_messages(["じゅもんを おぼえていない！"])
                        self.mode = "MESSAGE"
                    else:
                        self.mode = "SPELL_MENU"
                        self.sub_cursor = 0

                elif self.cursor == 1:  # つよさ
                    self.mode = "STATS_MENU"

                elif self.cursor == 2:  # どうぐ
                    # アイテムを1つ以上持っているか確認
                    has_items = any(count > 0 for count in p.items.values())
                    if not has_items:
                        self.msg_box.push_messages(["どうぐを もっていない！"])
                        self.mode = "MESSAGE"
                    else:
                        self.mode = "ITEM_MENU"
                        self.sub_cursor = 0

    def trigger_battle(self):
        from .battle_state import BattleState

        # スライムまたはドラキーをランダム出現
        monster_id = random.choice(["entenstr", "rarutaes"])
        monster = self.app.repo.create_monster(monster_id)
        self.app.change_state(BattleState(self.app, monster))

    def draw(self):
        pyxel.cls(3)  # 緑色のフィールド背景

        # 簡易なグリッド背景描画
        for x in range(0, 160, 8):
            pyxel.line(x, 0, x, 120, 11)
        for y in range(0, 120, 8):
            pyxel.line(0, y, 160, y, 11)

        # プレイヤーの描画（ドットまたは文字）
        px = self.player_x * self.grid_size
        py = self.player_y * self.grid_size
        pyxel.rect(px, py, 8, 8, 8)  # 赤い四角をプレイヤーとする

        # 簡易UI
        pyxel.rect(0, 0, 160, 12, 0)
        p = self.app.player
        pyxel.text(4, 3, f"HERO LV:{p.level} HP:{p.hp}/{p.max_hp} G:{p.gold}", 7)
        pyxel.text(4, 110, "MOVE: ARROW KEYS", 7)
