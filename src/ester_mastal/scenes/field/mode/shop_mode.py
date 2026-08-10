from enum import Enum

from ....ui.enum_select_window import EnumSelectWindow
from ....ui.message_window import MessageWindow
from .base_mode import BaseMode, FieldContext
from .signals import ModeSignal, PopSignal


class ShopCommand(Enum):
    BUY = "かう"
    SELL = "うる"


class ShopMode(BaseMode):
    def __init__(self, context: FieldContext, event):
        super().__init__(context)
        self._wm = context.scene.window_manager

        self._greeting_msg = MessageWindow(
            self.context.scene.app,
            x=10,
            y=130,
            width=172,
            height=50,
            speed=2,
            messages=["いらっしゃいませ！\nなにに しますか？"],
        )
        self._wm.push(self._greeting_msg)

        self._shop_menu = EnumSelectWindow(
            context.scene.app, 10, 24, 60, list(ShopCommand)
        )

        # ★ 進行管理用フラグ
        self._has_pushed_shop = False  # お店メニューを出したか
        self._has_made_choice = False  # 「はい/いいえ」を選び終えたか

    def update(self):
        # ★ ステップ1: 挨拶メッセージが読み終わったらお店メニューを出す
        if not self._has_pushed_shop and self._wm.current != self._greeting_msg:
            self._wm.push(self._shop_menu)
            self._has_pushed_shop = True

        if self._shop_menu.result is not None:
            choise = self._shop_menu.result
            self._shop_menu.result = None
            self._has_made_choice = True  # 選択完了フラグをオン

            match choise:
                case ShopCommand.BUY:
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

                case ShopCommand.SELL:
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
