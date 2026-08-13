from dataclasses import dataclass, field

from ....data.events import EventFlag
from ....models.item import ItemCode
from ..mode.base_mode import FieldContext
from .event_strategy import BaseEventData
from .message_strategy import MessageEventData, MessageStrategy


@dataclass
class Dialogue(MessageEventData):
    flag: EventFlag | None = None
    reward_gold: int = 0
    reward_item: ItemCode | None = None


@dataclass
class ExtendMessageEventData(BaseEventData):
    dialogues: list[Dialogue] = field(default_factory=list)


class ExtendMessageStrategy(MessageStrategy[ExtendMessageEventData]):
    @staticmethod
    def _get_dialogue(
        dialogues: list[Dialogue], flags: set[EventFlag]
    ) -> Dialogue | None:
        """現在のフラグ状態に適合するダイアログを取得"""
        for d in dialogues:
            required_flag = d.flag
            if required_flag is None or required_flag in flags:
                return d
        return None

    def execute(self, context: FieldContext, data: ExtendMessageEventData):
        player = context.scene.app.player
        flags = context.scene.app.flags

        dialogue = self._get_dialogue(data.dialogues, flags)

        if dialogue is None:
            return super().execute(
                context,
                MessageEventData(
                    name=data.name,  # ★ 修正点3: BaseEventData.name ではなく data.name
                    messages=["..."],
                ),
            )

        if dialogue.reward_gold > 0:
            player.gold += dialogue.reward_gold

        if dialogue.reward_item:
            player.inventory.append(dialogue.reward_item)

        return super().execute(
            context,
            MessageEventData(
                name=data.name,
                set_flag=dialogue.set_flag,
                messages=dialogue.messages,
            ),
        )
