from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .base_mode import BaseModeData
from .message_mode import MessageMode

if TYPE_CHECKING:
    from data.events import EventFlag
    from models.item import ItemCode


@dataclass
class Dialogue:
    set_flag: EventFlag | None = None
    messages: list[str] = field(default_factory=list)
    flag: EventFlag | None = None
    reward_gold: int = 0
    reward_item: ItemCode | None = None


@dataclass
class ExtendMessageModeData(BaseModeData):
    dialogues: list[Dialogue] = field(default_factory=list)


def get_dialogue(dialogues: list[Dialogue], flags: set[EventFlag]) -> Dialogue | None:
    """現在のフラグ状態に適合するダイアログを取得"""
    for d in dialogues:
        required_flag = d.flag
        if required_flag is None or required_flag in flags:
            return d
    return None


class ExtendMessageMode(MessageMode):
    def _setup_dialogue(self):
        data: ExtendMessageModeData = self._scene.current_event
        self._event_name = data.name

        # フラグに合ったダイアログを取得
        dialogue = get_dialogue(data.dialogues, self._flags)

        # 該当するダイアログがない場合の安全ガード
        if dialogue is None:
            self._messages = ["..."]
            self._set_flag = None
            return

        # メッセージとフラグの作業用変数
        messages = list(dialogue.messages)
        set_flag = dialogue.set_flag

        # 1. 報酬処理（ゴールド＆アイテムの加算）
        if dialogue.reward_gold > 0:
            self._player.gold += dialogue.reward_gold

        if dialogue.reward_item:
            item_code = dialogue.reward_item

            # add_item 実行（10個未満なら成功で True、満タンなら False）
            if not self._player.add_item(item_code):
                # 満タンで受け取れなかった場合！
                item_name = getattr(item_code, "value", str(item_code))
                messages.append(
                    f"しかし もちものが いっぱいで {item_name} は もてなかった！"
                )

                # ★ 重要: フラグをONにしないことで、アイテム欄を空けた後に再度話しかければ受け取れるようにする！
                set_flag = None

            # 3. 親クラス (MessageMode) が使うプロパティにセット
        self._messages = messages
        self._set_flag = set_flag
