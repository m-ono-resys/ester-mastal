from enum import Enum

from ....ui.enum_select_window import EnumSelectWindow
from ....ui.message_window import MessageWindow
from .base_mode import BaseMode, FieldContext
from .signals import ModeSignal, PopSignal


class InnCommand(Enum):
    Yes = "はい"
    No = "いいえ"


class InnMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)
        self._wm = context.scene.window_manager

        self._greeting_msg = MessageWindow(
            self.context.scene.app,
            x=10,
            y=130,
            width=172,
            height=50,
            speed=2,
            messages=["おかあさん「おかえりなさい\n やすんでいくかい？」"],
        )
        self._wm.push(self._greeting_msg)

        self._choice_menu = EnumSelectWindow(
            context.scene.app, 10, 24, 60, list(InnCommand)
        )

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
                        p = self.context.scene.app.player
                        p.hp, p.mp = p.max_hp, p.max_mp
                        self._wm.clear()
                        self._wm.push(
                            MessageWindow(
                                self.context.scene.app,
                                x=10,
                                y=130,
                                width=172,
                                height=50,
                                speed=2,
                                messages=["よく ねむれたかい？", "いってらっしゃい！"],
                            )
                        )

                    case _:
                        self._wm.clear()
                        self._wm.push(
                            MessageWindow(
                                self.context.scene.app,
                                x=10,
                                y=130,
                                width=172,
                                height=50,
                                speed=2,
                                messages=["むりしないでね"],
                            )
                        )

            elif self._wm.current != self._choice_menu:
                self._has_made_choice = True
                self._wm.clear()
                self._wm.push(
                    MessageWindow(
                        self.context.scene.app,
                        x=10,
                        y=130,
                        width=172,
                        height=50,
                        speed=2,
                        messages=["むりしないでね"],
                    )
                )

        # ★ ステップ3: 選択後のメッセージも読み終わってウィンドウが全て閉じたら探索に戻る
        if self._has_made_choice and not self._wm.is_open:
            return PopSignal()

        return ModeSignal()

    def draw(self):
        pass
