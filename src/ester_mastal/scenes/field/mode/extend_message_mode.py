from ....ui.message_window import MessageWindow
from .base_mode import BaseMode, FieldContext
from .signals import ModeSignal, PopSignal


def get_npc_dialogue(event: dict, flags: set[str]) -> dict:
    """現在のフラグ状態に適合するダイアログ辞書（まるごと）を取得"""
    if "dialogues" in event:
        for d in event["dialogues"]:
            required_flag = d.get("flag")
            if required_flag is None or required_flag in flags:
                return d
    return event


class MessageMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)
        self._wm = self.context.scene.window_manager
        self._flags = self.context.scene.app.flags
        self._event = self.context.scene.current_event
        self._player = self.context.scene.app.player
        self._dialogue = get_npc_dialogue(self._event, self._flags)
        self._messages = self._dialogue.get("messages", ["..."])

        if self._event.get("type") == "CHEST":
            self._event["is_opened"] = True

        # 2. ★ アイテムやゴールドの獲得処理
        if "give_item" in self._dialogue:
            self._player.inventory.append(
                self._dialogue["give_item"]
            )  # 手持ちにアイテム追加 (p.inventory など)
        elif "give_item" in self._event:
            self._player.inventory.append(self._event["give_item"])

        if "give_gold" in self._dialogue:
            self._player.gold += self._dialogue["give_gold"]  # お金加算
        elif "give_gold" in self._event:
            self._player.gold += self._event["give_gold"]

        self._msg = MessageWindow(
            self.context.scene.app,
            x=10,
            y=130,
            width=172,
            height=50,
            speed=2,
            messages=self._messages,
        )
        self._wm.push(self._msg)
        if "set_flag" in self._dialogue:
            self._flags.add(self._dialogue["set_flag"])
        elif "set_flag" in self._event:
            self._flags.add(self._event["set_flag"])

    def update(self):
        if not self._wm.is_open:
            return PopSignal()
        return ModeSignal()

    def draw(self):
        pass
