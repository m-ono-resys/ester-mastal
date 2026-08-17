from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .message_mode import MessageMode, MessageModeData
from .signals import ModeSignal, PopSignal

if TYPE_CHECKING:
    from ....data.events import EventFlag
    from ....models.monster import MonsterCode


@dataclass(kw_only=True)
class BossMessageModeData(MessageModeData):
    """ボス・強敵イベント用データ（スプライト表示＆撃破時消去機能付き）"""

    monster_code: MonsterCode
    sprite_u: int = 32
    sprite_v: int = 32
    sprite_w: int = 16  # スプライトの幅（16や32など）
    sprite_h: int = 16  # スプライトの高さ
    colkey: int = 8  # 透過色
    defeated_flag: EventFlag | None = None  # ★ 倒したらONになるフラグ
    victory_messages: list[str] = field(default_factory=list)


class BossMessageMode(MessageMode):
    def _setup_dialogue(self):
        data: BossMessageModeData = self._scene.current_event
        self._event_name = data.name

        # すでにデラミールを撃破しているか判定
        is_defeated = (
            data.defeated_flag is not None and data.defeated_flag in self._flags
        )

        if is_defeated:
            # 撃破後 ➔ victory_messages をメッセージにセット
            self._messages = data.victory_messages
            self._set_flag = None
            self.monster_code = None
            self._is_victory_mode = True
        else:
            self._messages = data.messages
            self._set_flag = data.set_flag
            self.monster_code = data.monster_code
            self._is_victory_mode = False

    def update(self) -> ModeSignal:
        if not self._wm.is_open:
            # ★ 1. 捨て台詞が読み終わった場合 ➔ 自動的にエンディング画面へ移行！
            if getattr(self, "_is_victory_mode", False):
                from ...ending_scene import EndingScene

                self._scene.app.change_state(EndingScene(self._scene.app))
                return ModeSignal()

            # 2. 戦闘前メッセージが読み終わった場合 ➔ ボス戦開始
            if self.monster_code is not None:
                self._scene.trigger_battle_with_monster(self.monster_code)
                return ModeSignal()

            return PopSignal()  # 通常の会話終了は PopSignal

        return ModeSignal()
