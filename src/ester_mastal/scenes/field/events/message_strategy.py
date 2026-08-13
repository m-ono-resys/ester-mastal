from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ....ui.message_window import MessageWindow
from ..mode.base_mode import BaseMode, FieldContext
from ..mode.signals import ModeSignal, PopSignal, PushSignal
from .event_strategy import BaseEventData, EventStrategy

if TYPE_CHECKING:
    from ....data.events import EventFlag


@dataclass
class MessageEventData(BaseEventData):
    set_flag: EventFlag | None = None
    messages: list[str] = field(default_factory=list)


class MessageMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)
        self._app = self.context.scene.app
        self._wm = self.context.scene.window_manager
        self._flags = self.context.scene.app.flags
        self._event_data = self.context.scene.current_event

    def update(self):
        messages = self._event_data.messages
        self._wm.push(
            MessageWindow(self._app, 10, 130, 172, 50, speed=2, messages=messages)
        )

        # フラグがあれば設定
        if self._event_data.set_flag:
            self._event_data.add(self._event_data.set_flag)

        if not self._wm.is_open:
            return PopSignal()

        return ModeSignal()

    def draw(self):
        pass


class MessageStrategy(EventStrategy[MessageEventData]):
    def execute(self, context):
        return PushSignal(MessageMode(context))
