import pyxel
from .base_state import BaseState
from ..models.battle import BattleEngine
from ..ui.message_box import MessageBox
from ..ui.window import draw_window

class BattleState(BaseState):
    def __init__(self, app, monster):
        super().__init__(app)
        self.engine = BattleEngine(self.app.player, monster)
        self.cursor = 0  # 0: たたかう, 1: にげる
        self.state = "MESSAGE"  # 最初は「〇〇があらわれた！」表示からスタート

        self.msg_box = MessageBox(x=10, y=120, width=172, height=58, speed=2, font=self.app.font)
        self.msg_box.push_messages([f"{monster.name} が あらわれた！"])


    def update(self):
        if self.state == "COMMAND":
            # コマンド選択 (上下移動)
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN):
                self.cursor = 1 - self.cursor
            
            # 決定
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                if self.cursor == 0:  # たたかう
                    logs = self.engine.player_attack()
                    if not self.engine.monster.is_alive:
                        # 勝利時はレベルアップチェックも含む
                        lvl_logs = self.app.repo.check_level_up(self.app.player)
                        logs.extend(lvl_logs)
                    else:
                        # 敵の反撃
                        m_logs = self.engine.monster_turn()
                        logs.extend(m_logs)

                    self.msg_box.push_messages(logs)
                    self.state = "MESSAGE"
                        
                elif self.cursor == 1:  # にげる
                    logs, success = self.engine.player_escape()
                    if not success:
                        m_logs = self.engine.monster_turn()
                        logs.extend(m_logs)

                    self.msg_box.push_messages(logs)
                    self.state = "MESSAGE"


        elif self.state == "MESSAGE":
            is_all_done = self.msg_box.update()

            if is_all_done:
                # 戦闘終了判定
                if self.engine.is_finished:
                    if self.app.player.is_alive:
                        from .field_state import FieldState
                        self.app.change_state(FieldState(self.app))
                    else:
                        from .game_over_state import GameOverState
                        self.app.change_state(GameOverState(self.app))
                else:
                    self.state = "COMMAND"


    def draw(self):
        pyxel.cls(0) # 背景黒
        
        # モンスター枠・表示
        m = self.engine.monster
        draw_window(56, 16, 80, 50)
        pyxel.text(68, 32, m.name, 10, self.app.font)
        
        # プレイヤー状態ウィンドウ
        p = self.app.player
        draw_window(10, 120, 75, 58)
        pyxel.text(16, 126, f"{p.name}", 7, self.app.font)
        pyxel.text(16, 138, f"HP: {p.hp}/{p.max_hp}", 7, self.app.font)
        pyxel.text(16, 150, f"MP: {p.mp}/{p.max_mp}", 7, self.app.font)
        pyxel.text(16, 162, f"LV:{p.level}", 7, self.app.font)

        # コマンドウィンドウ（コマンド選択時）
        if self.state == "COMMAND":
            draw_window(95, 120, 87, 58)
            pyxel.text(112, 134, " たたかう", 7, self.app.font)
            pyxel.text(112, 152, " にげる", 7, self.app.font)
            # カーソル描画
            cursor_y = 134 if self.cursor == 0 else 152
            pyxel.text(102, cursor_y, ">", 10, self.app.font)

        # メッセージウィンドウ（テキスト表示時）
        if self.state == "MESSAGE":
            self.msg_box.draw()
            