from ....ui.message_window import MessageWindow
from .base_mode import BaseMode, FieldContext
from .signals import ModeSignal, PopSignal


class MessageMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)
        self._wm = self.context.scene.window_manager
        self._msg = MessageWindow(
            self.context.scene.app,
            x=10,
            y=130,
            width=172,
            height=50,
            speed=2,
            messages=self.context.scene.current_event["messages"],
        )
        self._wm.push(self._msg)

    def update(self):
        if not self._wm.is_open:
            return PopSignal()
        return ModeSignal()

    def draw(self):
        pass