from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ....ui.message_window import MessageWindow
from .base_mode import BaseMode, BaseModeData
from .signals import ModeSignal, PopSignal

if TYPE_CHECKING:
    from ....data.events import EventFlag
    from .base_mode import FieldContext


@dataclass
class MessageModeData(BaseModeData):
    set_flag: EventFlag | None = None
    messages: list[str] = field(default_factory=list)


class MessageMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)
        self._flags = self._app.flags
        self._event_data: MessageModeData = self._scene.current_event
        self._player = self._app.player

        self._msg = MessageWindow(
            self._app,
            x=10,
            y=130,
            width=172,
            height=50,
            speed=2,
            messages=self._event_data.messages,
            name=self._event_data.name,
        )
        self._wm.push(self._msg)

        if self._event_data.set_flag:
            self._flags.add(self._event_data.set_flag)

    def update(self):
        if not self._wm.is_open:
            return PopSignal()
        return ModeSignal()

    def draw(self):
        pass
