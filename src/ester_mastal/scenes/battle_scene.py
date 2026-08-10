from enum import Enum, auto

import pyxel

from ..audio import play_se
from ..infrastructure.in_memory_spell_repository import InMemorySpellRepository
from ..models.battle import BattleEngine
from ..ui.battle_status_window import BattleStatusWindow
from ..ui.enum_select_window import EnumSelectWindow
from ..ui.message_window import MessageWindow
from ..ui.window_manager import WindowManager
from .base_scene import BaseScene


class States(Enum):
    MESSAGE = auto()
    COMMAND = auto()


class BattleCommand(Enum):
    ATTACK = "たたかう"
    SPELL = "じゅもん"
    ITEM = "アイテム"
    ESCAPE = "にげる"


class BattleScene(BaseScene):
    def __init__(self, app, monster):
        super().__init__(app)
        self.engine = BattleEngine(self.app.player, monster, self.app.repo)

        self.spell_repository = InMemorySpellRepository()

        # UI
        self.window_manager = WindowManager()
        self.battle_status_window = BattleStatusWindow(app)
        self.cmd_window: EnumSelectWindow[BattleCommand] | None = None
        self.item_window: EnumSelectWindow | None = None
        self.spell_window: EnumSelectWindow | None = None

        # 戦闘開始メッセージの表示
        self.show_message([f"{monster.name} が あらわれた！"])

        self.msg_window = MessageWindow(app, x=10, y=120, width=172, height=60, speed=2)
        self.msg_window.push_messages([f"{monster.name} が あらわれた！"])

    def show_message(self, messages: list[str]):
        """メッセージウィンドウを WindowManager に追加"""
        self.window_manager.push(
            MessageWindow(
                self.app, x=10, y=120, width=172, height=60, speed=2, messages=messages
            )
        )

    def show_command_menu(self):
        """コマンド選択ウィンドウを WindowManager に追加"""
        self.cmd_window = EnumSelectWindow(
            self.app, x=95, y=120, width=87, choices=list(BattleCommand)
        )
        self.window_manager.push(self.cmd_window)

    def update(self):
        # 1. 最前面ウィンドウの入力・文字送りアニメーションを更新
        self.window_manager.update()

        # 2. ウィンドウが全て閉じられた時の処理（メッセージ読み終わり時）
        if not self.window_manager.is_open:
            if self.engine.is_finished:
                # 戦闘終了 ➔ 勝敗に応じたシーン遷移
                if self.app.player.is_alive:
                    if self.engine.monster.is_boss:
                        from .ending_scene import EndingScene

                        self.app.change_state(EndingScene(self.app))
                    else:
                        from .field.field_scene import FieldScene

                        self.app.change_state(FieldScene(self.app))
                else:
                    from .game_over_scene import GameOverScene

                    self.app.change_state(GameOverScene(self.app))
            else:
                # 戦闘継続 ➔ コマンドメニューを表示
                self.show_command_menu()

        # 3. コマンドメニューが開かれており、選択が決定された場合の処理
        elif self.cmd_window is not None and self.cmd_window.result is not None:
            cmd = self.cmd_window.result
            self.window_manager.pop()  # コマンドウィンドウを閉じる
            self.cmd_window = None

            match cmd:
                case BattleCommand.ATTACK:
                    play_se(0)  # 攻撃SE
                    logs = self.engine.player_attack()
                    if self.engine.monster.is_alive:
                        m_logs = self.engine.monster_turn()
                        play_se(2)  # ダメージSE
                        logs.extend(m_logs)
                    self.show_message(logs)

                case BattleCommand.SPELL:
                    _spells = self.app.player.spells
                    if not _spells:
                        self.show_command_menu()
                        self.show_message(["つかえるじゅもんがない！"])
                    else:
                        self.spell_window = EnumSelectWindow(
                            self.app,
                            x=95,
                            y=120,
                            width=87,
                            choices=self.app.player.spells,
                        )
                        self.window_manager.push(self.spell_window)

                case BattleCommand.ESCAPE:
                    logs, success = self.engine.player_escape()
                    if not success:
                        m_logs = self.engine.monster_turn()
                        play_se(2)  # ダメージSE
                        logs.extend(m_logs)
                    self.show_message(logs)

        elif self.spell_window is not None and self.spell_window.result is not None:
            spell_code = self.spell_window.result
            self.window_manager.pop()  # コマンドウィンドウを閉じる
            self.spell_window = None

            spell = self.spell_repository.find_by_code(spell_code)

            if spell is not None:
                logs = self.engine.player_cast_spell(spell)
                if self.engine.monster.is_alive:
                    m_logs = self.engine.monster_turn()
                    play_se(2)  # ダメージSE
                    logs.extend(m_logs)

            self.show_message(logs)

    def draw(self):
        pyxel.cls(0)  # 背景黒

        # 1. モンスター枠＆スプライト描画（大きめ枠: 幅112px、高さ64px）
        m = self.engine.monster
        box_w, box_h = 112, 96
        box_x = (192 - box_w) // 2  # 画面横中央 (X=40)
        box_y = 12

        # 二重枠線の描画
        draw_window(box_x, box_y, box_w, box_h)

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
        self.battle_status_window.draw()

        self.window_manager.draw()


def draw_window(
    x: int, y: int, width: int, height: int, bg_col: int = 0, border_col: int = 7
):
    """
    ドラクエ風の黒背景＋二重白枠ウィンドウを描画する
    """
    # 1. 外側の背景（黒）
    pyxel.rect(x, y, width, height, bg_col)

    # 2. 外枠（白）
    pyxel.rectb(x, y, width, height, border_col)

    # 3. 内側の線（1ピクセル内側に細い枠線を描くことでDQ風二重枠を再現）
    pyxel.rectb(x + 2, y + 2, width - 4, height - 4, border_col)
