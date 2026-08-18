from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .base_mode import BaseModeData
from .extend_message_mode import ExtendMessageMode

if TYPE_CHECKING:
    from data.events import EventFlag
    from models.item import ItemCode


@dataclass(kw_only=True)
class ChestModeData(BaseModeData):
    """宝箱専用のデータ構造（デフォルトメッセージは自動生成されるため指定不要）"""

    flag_key: EventFlag
    reward_gold: int = 0
    reward_item: ItemCode | None = None
    closed_sprite: tuple[int, int] = (16, 32)
    opened_sprite: tuple[int, int] = (32, 32)
    # 独自メッセージで上書きしたい場合のみ使用（通常は空でOK）
    open_messages: list[str] = field(default_factory=list)
    empty_messages: list[str] = field(default_factory=list)


class ChestMessageMode(ExtendMessageMode):
    """宝箱専用のメッセージモード（固定メッセージ自動生成＋スプライト切り替え）"""

    def _setup_dialogue(self):
        data: ChestModeData = self._scene.current_event
        self._event_name = data.name

        # ★ 開封済みかどうかの判定を「中央管理フラグ (self._flags)」のみで行う！
        is_opened = data.flag_key in self._flags

        if is_opened:
            # 1. ★ 開封済みの場合（固定空っぽメッセージ）
            self._messages = (
                data.empty_messages
                if data.empty_messages
                else ["たからばこ は からっぽ だ。"]
            )
            self._set_flag = None
        else:
            # 2. ★ 未開封の場合 ➔ 親クラス(MessageMode)にこのフラグをONにさせるよう設定
            self._set_flag = None

            # 報酬の付与と固定ログの生成
            reward_texts = []

            if data.reward_gold > 0:
                self._player.gold += data.reward_gold
                reward_texts.append(f"{data.reward_gold} ゴールド を てにいれた！")

            if data.reward_item:
                # self._player.inventory.append(data.reward_item)
                item_name = getattr(data.reward_item, "value", str(data.reward_item))
                if self._player.add_item(data.reward_item):
                    reward_texts.append(f"{item_name} を てにいれた！")
                    self._set_flag = data.flag_key
                else:
                    reward_texts.append(
                        f"しかし もちものが いっぱいで {item_name} は もてなかった！"
                    )

            # 固定メッセージの構築（「たからばこ を あけた！」 ＋ 獲得報酬）
            if data.open_messages:
                self._messages = data.open_messages
            else:
                default_msgs = ["たからばこ を あけた！"]
                default_msgs.extend(reward_texts)
                self._messages = default_msgs
