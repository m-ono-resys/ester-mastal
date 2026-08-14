from __future__ import annotations

from dataclasses import dataclass

from .extend_message_mode import ExtendMessageModeData


@dataclass(kw_only=True)
class GateMessageModeData(ExtendMessageModeData):
    """ゲートイベント用データ（スプライト表示付き）"""

    sprite_u: int = 32
    sprite_v: int = 32
    sprite_w: int = 16  # スプライトの幅（16や32など）
    sprite_h: int = 16  # スプライトの高さ
    colkey: int = 8  # 透過色
