from __future__ import annotations

from dataclasses import dataclass
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


class BossMessageMode(MessageMode):
    def _setup_dialogue(self):
        data: BossMessageModeData = self._scene.current_event
        self._event_name = data.name

        self._messages = data.messages
        self._set_flag = data.set_flag
        self.monster_code = data.monster_code

    def update(self) -> ModeSignal:
        # メッセージウィンドウが閉じられた時の処理
        if not self._wm.is_open:
            if self.monster_code is not None:
                self._scene.trigger_battle_with_monster(self.monster_code)
                return ModeSignal()

            return PopSignal()  # 通常の会話終了は PopSignal

        return ModeSignal()
