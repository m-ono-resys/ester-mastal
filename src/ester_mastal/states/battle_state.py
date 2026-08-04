import pyxel
from .base_state import BaseState
from ..models.battle import BattleEngine
from ..ui.window import draw_window
from ..ui.message_box import MessageBox

class BattleState(BaseState):
    def __init__(self, app, monster):
        super().__init__(app)
        self.engine = BattleEngine(self.app.player, monster)
        self.cursor = 0  # 0: たたかう, 1: にげる
        self.state = "MESSAGE"  # 最初は「〇〇があらわれた！」表示からスタート

        self.msg_box = MessageBox(
            x=10, y=65, width=140, height=45, speed=2, font=self.app.font
        )
        self.msg_box.push_messages([f"{monster.name} が あらわれた！"])

        # self.message_queue = [f"{monster.name} が あらわれた！"]
        # self.current_message = ""
        # self.state = "COMMAND"  # "COMMAND", "MESSAGE"

        # self.next_message()

    def next_message(self):
        """メッセージキューから1つ取り出して表示"""
        if self.message_queue:
            self.current_message = self.message_queue.pop(0)
        else:
            self.current_message = ""
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
                        
                    # self.message_queue.extend(logs)
                    # self.state = "MESSAGE"
                    # self.next_message()
                    
                elif self.cursor == 1:  # にげる
                    logs, success = self.engine.player_escape()
                    if not success:
                        m_logs = self.engine.monster_turn()
                        logs.extend(m_logs)

                    self.msg_box.push_messages(logs)
                    self.state = "MESSAGE"
                    # self.message_queue.extend(logs)
                    # self.state = "MESSAGE"
                    # self.next_message()

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

            # キーを押したら次のメッセージへ
            # if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                # self.next_message()

    def draw(self):
        pyxel.cls(0) # 背景黒
        
        # モンスター枠・表示
        m = self.engine.monster
        pyxel.rectb(45, 15, 70, 45, 7)
        pyxel.text(55, 30, m.name, 10, self.app.font)
        
        # プレイヤー状態ウィンドウ
        p = self.app.player
        pyxel.rectb(10, 65, 60, 45, 7)
        pyxel.text(15, 70, f"{p.name}", 7, self.app.font)
        pyxel.text(15, 80, f"HP: {p.hp}/{p.max_hp}", 7, self.app.font)
        pyxel.text(15, 90, f"MP: {p.mp}/{p.max_mp}", 7, self.app.font)

        # コマンドウィンドウ（コマンド選択時）
        if self.state == "COMMAND":
            pyxel.rectb(80, 65, 70, 45, 7)
            pyxel.text(90, 75, " たたかう", 7, self.app.font)
            pyxel.text(90, 90, " にげる", 7, self.app.font)
            # カーソル描画
            cursor_y = 75 if self.cursor == 0 else 90
            pyxel.text(84, cursor_y, ">", 10, self.app.font)

        # メッセージウィンドウ（テキスト表示時）
        if self.state == "MESSAGE":
            self.msg_box.draw()
            
            # pyxel.rectb(10, 65, 140, 45, 7)
            # pyxel.text(15, 75, self.current_message, 7, self.app.font)
            # pyxel.text(135, 100, "▼", (pyxel.frame_count // 10) % 2 * 7, self.app.font)