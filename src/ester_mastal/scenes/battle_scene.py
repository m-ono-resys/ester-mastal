from enum import Enum, auto

import pyxel

from ..audio import play_se
from ..models.battle import BattleEngine
from ..ui.message_window import MessageWindow

# from ..ui.window import draw_window
from .base_scene import BaseScene


class States(Enum):
    MESSAGE = auto()
    COMMAND = auto()


class BattleScene(BaseScene):
    def __init__(self, app, monster):
        super().__init__(app)
        self.engine = BattleEngine(self.app.player, monster, self.app.repo)
        self.cursor = 0  # 0: たたかう, 1: にげる
        self.state: States = (
            States.MESSAGE
        )  # 最初は「〇〇があらわれた！」表示からスタート

        self.msg_window = MessageWindow(app, x=10, y=120, width=172, height=60, speed=2)
        self.msg_window.push_messages([f"{monster.name} が あらわれた！"])

    def update(self):
        match self.state:
            case States.COMMAND:
                # コマンド選択 (上下移動)
                if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN):
                    self.cursor = 1 - self.cursor

                # 決定
                if (
                    pyxel.btnp(pyxel.KEY_Z)
                    or pyxel.btnp(pyxel.KEY_SPACE)
                    or pyxel.btnp(pyxel.KEY_RETURN)
                ):
                    if self.cursor == 0:  # たたかう
                        play_se(0)  # ★ 攻撃SE
                        logs = self.engine.player_attack()
                        if self.engine.monster.is_alive:
                            # 敵の反撃
                            m_logs = self.engine.monster_turn()
                            play_se(2)  # ★ ダメージSE
                            logs.extend(m_logs)

                        self.msg_window.push_messages(logs)
                        self.state = States.MESSAGE

                    elif self.cursor == 1:  # にげる
                        logs, success = self.engine.player_escape()
                        if not success:
                            m_logs = self.engine.monster_turn()
                            logs.extend(m_logs)

                        self.msg_window.push_messages(logs)
                        self.state = States.MESSAGE

            case States.MESSAGE:
                is_all_done = self.msg_window.update()

                if is_all_done:
                    # 戦闘終了判定
                    if self.engine.is_finished:
                        if self.app.player.is_alive:
                            if self.engine.monster.is_boss:
                                from .ending_scene import EndingScene

                                self.app.change_state(EndingScene(self.app))
                            else:
                                from .field_scene import FieldScene

                                self.app.change_state(FieldScene(self.app))
                        else:
                            from .game_over_scene import GameOverScene

                            self.app.change_state(GameOverScene(self.app))
                    else:
                        self.state = States.COMMAND

    def draw(self):
        pyxel.cls(0)  # 背景黒

        # 1. モンスター枠＆スプライト描画（大きめ枠: 幅112px、高さ64px）
        m = self.engine.monster
        box_w, box_h = 112, 96
        box_x = (192 - box_w) // 2  # 画面横中央 (X=40)
        box_y = 12

        # 二重枠線の描画
        # draw_window(box_x, box_y, box_w, box_h)

        # モンスターのスプライトを枠の「完全な中央」に描画
        sprite_x = box_x + (box_w - m.sprite_w) // 2
        sprite_y = box_y + (box_h - m.sprite_h) // 2

        pyxel.blt(
            sprite_x,
            sprite_y,
            0,
            m.sprite_u,
            m.sprite_v,
            m.sprite_w,
            m.sprite_h,
            m.colkey,
        )

        # プレイヤー状態ウィンドウ
        p = self.app.player
        draw_window(10, 120, 80, 60)
        pyxel.text(16, 126, f"{p.name}", 7, self.app.font)
        pyxel.text(16, 138, f"HP: {p.hp}/{p.max_hp}", 7, self.app.font)
        pyxel.text(16, 150, f"MP: {p.mp}/{p.max_mp}", 7, self.app.font)
        pyxel.text(16, 162, f"LV:{p.level}", 7, self.app.font)

        match self.state:
            case States.COMMAND:
                # コマンドウィンドウ（コマンド選択時）
                draw_window(98, 120, 84, 60)
                pyxel.text(112, 134, " たたかう", 7, self.app.font)
                pyxel.text(112, 152, " にげる", 7, self.app.font)
                # カーソル描画
                cursor_y = 134 if self.cursor == 0 else 152
                pyxel.text(104, cursor_y, ">", 10, self.app.font)

            case States.MESSAGE:
                # メッセージウィンドウ（テキスト表示時）
                self.msg_window.draw()
