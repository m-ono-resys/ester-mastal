from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from ....ui.enum_select_window import EnumSelectWindow
from ....ui.message_window import MessageWindow
from .base_mode import BaseMode, BaseModeData
from .signals import ModeSignal, PopSignal

if TYPE_CHECKING:
    from .base_mode import FieldContext


@dataclass
class InnModeData(BaseModeData):
    greeting_messages: list[str] = field(default_factory=list)
    done_messages: list[str] = field(default_factory=list)
    cancel_messages: list[str] = field(default_factory=list)


class InnCommand(Enum):
    Yes = "はい"
    No = "いいえ"


class InnMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)
        self._event_data: InnModeData = self._scene.current_event
        self._player = self._app.player

        self._greeting_msg = MessageWindow(
            self._app,
            x=10,
            y=130,
            width=172,
            height=50,
            speed=2,
            # messages=["おかあさん「おかえりなさい\n やすんでいくかい？」"],
            name=self._event_data.name,
            messages=self._event_data.greeting_messages,
        )
        self._wm.push(self._greeting_msg)

        self._choice_menu = EnumSelectWindow(self._app, 10, 24, 60, list(InnCommand))

        # ★ 進行管理用フラグ
        self._has_pushed_choice = False  # 選択メニューを出したか
        self._has_made_choice = False  # 「はい/いいえ」を選び終えたか

    def update(self):
        # ★ ステップ1: 挨拶メッセージが読み終わったら「はい/いいえ」メニューを出す
        if not self._has_pushed_choice and self._wm.current != self._greeting_msg:
            self._wm.push(self._choice_menu)
            self._has_pushed_choice = True

        if self._has_pushed_choice and not self._has_made_choice:
            if self._choice_menu.result is not None:
                choise = self._choice_menu.result
                self._choice_menu.result = None
                self._has_made_choice = True  # 選択完了フラグをオン

                match choise:
                    case InnCommand.Yes:
                        p = self._app.player
                        p.hp, p.mp = p.max_hp, p.max_mp
                        self._wm.clear()
                        self._wm.push(
                            MessageWindow(
                                app=self._app,
                                x=10,
                                y=130,
                                width=172,
                                height=50,
                                speed=2,
                                # messages=["よく ねむれたかい？", "いってらっしゃい！"],
                                messages=self._event_data.done_messages,
                            )
                        )

                    case _:
                        self._wm.clear()
                        self._wm.push(
                            MessageWindow(
                                app=self._app,
                                x=10,
                                y=130,
                                width=172,
                                height=50,
                                speed=2,
                                # messages=["むりしないでね"],
                                messages=self._event_data.cancel_messages,
                            )
                        )

            elif self._wm.current != self._choice_menu:
                self._has_made_choice = True
                self._wm.clear()
                self._wm.push(
                    MessageWindow(
                        app=self._app,
                        x=10,
                        y=130,
                        width=172,
                        height=50,
                        speed=2,
                        messages=self._event_data.cancel_messages,
                    )
                )

        # ★ ステップ3: 選択後のメッセージも読み終わってウィンドウが全て閉じたら探索に戻る
        if self._has_made_choice and not self._wm.is_open:
            return PopSignal()

        return ModeSignal()

    def draw(self):
        pass
