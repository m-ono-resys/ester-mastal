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
                    # ★修正: リストが空かどうか直接チェック
                    if not p.items:
                        self.msg_box.push_messages(["どうぐを もっていない！"])
                        self.mode = "MESSAGE"
                    else:
                        self.mode = "ITEM_MENU"
                        self.sub_cursor = 0

        # --- 3. 呪文選択・使用 ---
        elif self.mode == "SPELL_MENU":
            p = self.app.player
            if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.mode = "MAIN_MENU"

            elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN):
                if len(p.spells) > 1:
                    self.sub_cursor = (self.sub_cursor + 1) % len(p.spells)

            elif (
                pyxel.btnp(pyxel.KEY_Z)
                or pyxel.btnp(pyxel.KEY_SPACE)
                or pyxel.btnp(pyxel.KEY_RETURN)
            ):
                selected_spell = p.spells[self.sub_cursor]

                # 回復呪文（ホイミなど）の場合
                if selected_spell.heal_amount > 0:
                    if p.mp < selected_spell.mp_cost:
                        self.msg_box.push_messages(["MPが たりない！"])
                    else:
                        p.mp -= selected_spell.mp_cost
                        healed = p.heal(selected_spell.heal_amount)
                        self.msg_box.push_messages(
                            [
                                f"{p.name} は {selected_spell.name} を となえた！",
                                f"HPが {healed} かいふくした！",
                            ]
                        )
                    self.mode = "MESSAGE"

        # --- 4. 道具選択・使用 ---
        elif self.mode == "ITEM_MENU":
            p = self.app.player
            # item_list = [item_id for item_id, count in p.items.items() if count > 0]

            if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.mode = "MAIN_MENU"

            # カーソル上下移動
            elif pyxel.btnp(pyxel.KEY_UP):
                if p.items:
                    self.sub_cursor = (self.sub_cursor - 1) % len(p.items)
            elif pyxel.btnp(pyxel.KEY_DOWN):
                if p.items:
                    self.sub_cursor = (self.sub_cursor + 1) % len(p.items)

            elif (
                pyxel.btnp(pyxel.KEY_Z)
                or pyxel.btnp(pyxel.KEY_SPACE)
                or pyxel.btnp(pyxel.KEY_RETURN)
            ) and p.items:
                item = p.items.pop(self.sub_cursor)

                if item in ["herb"]:  # やくそう
                    healed = p.heal(15)
                    self.msg_box.push_messages(
                        [
                            f"{p.name} は やくそうを つかった！",
                            f"HPが {healed} かいふくした！",
                        ]
                    )
                    self.mode = "MESSAGE"

        # --- 5. ステータス画面 ---
        elif self.mode == "STATS_MENU":
            # どのボタンを押してもメインメニューへ戻る
            if (
                pyxel.btnp(pyxel.KEY_Z)
                or pyxel.btnp(pyxel.KEY_X)
                or pyxel.btnp(pyxel.KEY_SPACE)
                or pyxel.btnp(pyxel.KEY_RETURN)
                or pyxel.btnp(pyxel.KEY_ESCAPE)
            ):
                self.mode = "MAIN_MENU"

        # --- 6. メッセージ表示中 ---
        elif self.mode == "MESSAGE":
            all_done = self.msg_box.update()
            if all_done:
                self.mode = "MAIN_MENU"

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
        pyxel.text(
            4, 3, f"HERO LV:{p.level} HP:{p.hp}/{p.max_hp} G:{p.gold}", 7, self.app.font
        )
        pyxel.text(4, 110, "MOVE: ARROW KEYS", 7)

        # --- メニュー表示中の重ね描き（オーバーレイ） ---
        if self.mode != "EXPLORE":
            # メインメニュー枠
            draw_window(10, 20, 50, 42)
            pyxel.text(20, 25, "じゅもん", 7, self.app.font)
            pyxel.text(20, 35, "つよさ", 7, self.app.font)
            pyxel.text(20, 45, "どうぐ", 7, self.app.font)
            pyxel.text(14, 25 + self.cursor * 10, ">", 10, self.app.font)

            # 呪文サブメニュー
            if self.mode == "SPELL_MENU":
                draw_window(65, 20, 85, 42)
                for i, spell in enumerate(p.spells):
                    pyxel.text(
                        75,
                        25 + i * 10,
                        f"{spell.name} M:{spell.mp_cost}",
                        7,
                        self.app.font,
                    )
                pyxel.text(69, 25 + self.sub_cursor * 10, ">", 10, self.app.font)

            # 道具サブメニュー
            elif self.mode == "ITEM_MENU":
                draw_window(65, 20, 85, 42)
                for i, item in enumerate(p.items):
                    name = "やくそう" if item == "herb" else item
                    pyxel.text(75, 25 + i * 10, name, 7, self.app.font)
                pyxel.text(69, 25 + self.sub_cursor * 10, ">", 10, self.app.font)

            # つよさ（詳細ステータス）画面
            elif self.mode == "STATS_MENU":
                draw_window(65, 20, 85, 80)
                pyxel.text(70, 25, f"なに: {p.name}", 7, self.app.font)
                pyxel.text(70, 35, f"レベル: {p.level}", 7, self.app.font)
                pyxel.text(70, 45, f"こうげき: {p.attack}", 7, self.app.font)
                pyxel.text(70, 55, f"しゅび: {p.defense}", 7, self.app.font)
                pyxel.text(70, 65, f"けいけん: {p.exp}", 7, self.app.font)
                pyxel.text(70, 75, f"ゴールド: {p.gold}", 7, self.app.font)

            # メッセージウィンドウ
            elif self.mode == "MESSAGE":
                self.msg_box.draw()
