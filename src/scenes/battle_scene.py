from enum import Enum, auto

import pyxel

from application.item_use_case import ItemUseCase
from audio import play_se
from data.events import EventFlag
from data.maps import MapId
from infrastructure.in_memory_item_repository import InMemoryItemRepository
from infrastructure.in_memory_spell_repository import InMemorySpellRepository
from models.battle import BattleEngine
from models.item import ItemCode
from models.monster import MonsterCode
from models.spell import SpellCode
from ui.battle_status_window import BattleStatusWindow
from ui.enum_select_window import EnumSelectWindow
from ui.message_window import MessageWindow
from ui.window_manager import WindowManager

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
        self._item_usecase = ItemUseCase(InMemoryItemRepository())

        # UI
        self.window_manager = WindowManager()
        self.battle_status_window = BattleStatusWindow(app)
        self.cmd_window: EnumSelectWindow[BattleCommand] | None = None
        self.item_window: EnumSelectWindow[ItemCode] | None = None
        self.spell_window: EnumSelectWindow[SpellCode] | None = None

        # 戦闘開始メッセージの表示
        self.show_message([f"{monster.name} が あらわれた！"])

    def show_message(self, messages: list[str]):
        """メッセージウィンドウを WindowManager に追加"""
        self.window_manager.push(
            MessageWindow(self.app, y=115, height=59, messages=messages)
        )

    def show_command_menu(self):
        """コマンド選択ウィンドウを WindowManager に追加"""
        self.cmd_window = EnumSelectWindow(
            self.app, x=95, y=115, width=87, choices=list(BattleCommand)
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
                    # from .field.field_scene import FieldScene
                    # from .field.mode.message_mode import MessageMode, MessageModeData

                    # field_scene = FieldScene(self.app)

                    # # ボスごとの撃破フラグと捨て台詞メッセージの定義テーブル
                    # boss_defeat_data = {
                    #     MonsterCode.SANTROTO.value: (
                    #         EventFlag.DEFEATED_SANTROTO,
                    #         ["このわたしがたおされるとは・・・"],
                    #     ),
                    #     MonsterCode.DERAMILE.value: (
                    #         EventFlag.DEFEATED_DERAMILE,
                    #         [
                    #             "このかんむりがあるかぎり、やみはほろびない",
                    #             "またふっかつして こんどこそぜったいにたおしてやる。",
                    #         ],
                    #     ),
                    # }

                    monster_name = self.engine.monster.name

                    match monster_name:
                        # ★ A. 中ボス（サントーロート）: MessageMode を使って会話後にフィールド復帰
                        case MonsterCode.SANTROTO.value:
                            self.app.flags.add(EventFlag.DEFEATED_SANTROTO)
                            from .field.field_scene import FieldScene
                            from .field.mode.message_mode import (
                                MessageMode,
                                MessageModeData,
                            )

                            field_scene = FieldScene(self.app)
                            field_scene.current_event = MessageModeData(
                                name=monster_name,
                                messages=["このわたしがたおされるとは・・・"],
                            )
                            field_scene.mode_stack.append(
                                MessageMode(field_scene.context)
                            )
                            self.app.change_state(field_scene)
                            return

                        # ★ B. ラスボス（デラミール）: BossMessageMode を使って会話後にエンディングへ遷移！
                        case MonsterCode.DERAMILE.value:
                            self.app.flags.add(EventFlag.DEFEATED_DERAMILE)
                            from .field.field_scene import FieldScene
                            from .field.mode.boss_message_mode import (
                                BossMessageMode,
                                BossMessageModeData,
                            )

                            field_scene = FieldScene(self.app)
                            field_scene.current_event = BossMessageModeData(
                                name=monster_name,
                                monster_code=MonsterCode.DERAMILE,
                                defeated_flag=EventFlag.DEFEATED_DERAMILE,
                                victory_messages=[
                                    "このかんむりがあるかぎり、やみはほろびない",
                                    "またふっかつして こんどこそぜったいにたおしてやる。",
                                ],
                            )
                            field_scene.mode_stack.append(
                                BossMessageMode(field_scene.context)
                            )
                            self.app.change_state(field_scene)
                            return

                        case _:
                            # 通常モンスター勝利時
                            from .field.field_scene import FieldScene

                            self.app.change_state(FieldScene(self.app))
                            return

                    # # ボスモンスターの場合はフラグ加算と捨て台詞メッセージを設定
                    # if monster_name in boss_defeat_data:
                    #     flag, messages = boss_defeat_data[monster_name]
                    #     self.app.flags.add(flag)

                    #     field_scene.current_event = MessageModeData(
                    #         name=monster_name,
                    #         messages=messages,
                    #     )
                    #     field_scene.mode_stack.append(MessageMode(field_scene.context))

                    # # 勝利時は一括で FieldScene へ切り替え
                    # self.app.change_state(field_scene)

                else:
                    p = self.app.player
                    p.hp = p.max_hp  # HP全回復
                    p.mp = p.max_mp  # MP全回復
                    p.gold //= 2  # 所持金半分

                    # 初期位置に移動
                    p.x = 8
                    p.y = 4
                    p.map_id = MapId.TOWN

                    # 全滅復活フラグをONにする
                    self.app.flags.add(EventFlag.PLAYER_DIED)

                    # 自宅へ復帰
                    from .field.field_scene import FieldScene

                    self.app.change_state(FieldScene(self.app))
                    # from .game_over_scene import GameOverScene

                    # self.app.change_state(GameOverScene(self.app))
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
                        self.show_message(["つかえるじゅもんがない！"])
                    else:
                        self.spell_window = EnumSelectWindow(
                            self.app,
                            x=95,
                            y=115,
                            width=87,
                            choices=_spells,
                        )
                        self.window_manager.push(self.spell_window)

                case BattleCommand.ITEM:
                    _items = self.app.player.inventory
                    if not _items:
                        self.show_message(["アイテムをもっていない！"])
                    else:
                        self.item_window = EnumSelectWindow(
                            self.app,
                            x=95,
                            y=115,
                            width=87,
                            choices=_items,
                        )
                        self.window_manager.push(self.item_window)

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

        elif self.item_window is not None and self.item_window.result is not None:
            item_code = self.item_window.result
            self.window_manager.pop()  # コマンドウィンドウを閉じる
            self.item_window = None

            if item_code is not None:
                logs = self._item_usecase.use_item(self.app.player, item_code)
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
