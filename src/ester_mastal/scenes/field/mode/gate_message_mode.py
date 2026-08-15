from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .extend_message_mode import ExtendMessageModeData

if TYPE_CHECKING:
    from ....data.events import EventFlag


@dataclass(kw_only=True)
class GateMessageModeData(ExtendMessageModeData):
    """ゲートイベント用データ（スプライト表示付き）"""

    sprite_u: int = 32
    sprite_v: int = 32
    sprite_w: int = 16  # スプライトの幅（16や32など）
    sprite_h: int = 16  # スプライトの高さ
    colkey: int = 8  # 透過色


@dataclass(kw_only=True)
class SwitchModeData(ExtendMessageModeData):
    """スイッチ用データ（ON/OFFでスプライトが変化）"""
    flag_key: EventFlag
    off_sprite: tuple[int, int] = (96, 32)  # OFF状態のスプライト (u, v)
    on_sprite: tuple[int, int] = (112, 32)   # ON状態のスプライト (u, v)
    sprite_w: int = 16
    sprite_h: int = 16
    colkey: int = 0
