from enum import Enum, auto

from ....application.shop_use_case import ShopUseCase
from ....infrastructure.in_memory_item_repository import InMemoryItemRepository
from ....models.item import ItemCode
from ....ui.enum_select_window import EnumSelectWindow
from ....ui.message_window import MessageWindow
from ....ui.shop_item_select_window import ShopItemSelectWindow
from .base_mode import BaseMode, FieldContext
from .signals import ModeSignal, PopSignal


class ShopCommand(Enum):
    BUY = "かう"
    SELL = "うる"


class ChoiceCommand(Enum):
    Yes = "はい"
    No = "いいえ"


# ★ ShopMode 内部専用のサブステート（買い物進行状態）
class _ShopSubState(Enum):
    GREETING = auto()  # 挨拶表示中
    MAIN_MENU = auto()  # 「かう / うる」選択中
    BUY_LIST = auto()  # 商品リスト選択中
    CONFIRM = auto()  # 「〇〇をかいますか？ / はい・いいえ」処理中
    EXITING = auto()  # お別れメッセージ表示中（店を出る）


class ShopMode(BaseMode):
    def __init__(self, context: FieldContext, event):
        super().__init__(context)
        self._wm = context.scene.window_manager
        self._event = event

        self._item_repository = InMemoryItemRepository()
        self._shop_use_case = ShopUseCase(self._item_repository)

        # 1. 挨拶メッセージ表示
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

        # 各ウィンドウの参照保持
        self._shop_command: EnumSelectWindow[ShopCommand] | None = None
        self._buy_window: EnumSelectWindow[ItemCode] | None = None
        self._sell_window: EnumSelectWindow[ItemCode] | None = None
        self._confirm_window: EnumSelectWindow[ChoiceCommand] | None = None
        self._confirm_msg: MessageWindow | None = None
        self._farewell_msg: MessageWindow | None = None

        self._pending_item: ItemCode | None = None
        self._sub_state = _ShopSubState.GREETING  # ★ 初期状態は挨拶

    def update(self) -> ModeSignal:
        match self._sub_state:
            # ★ 1. 挨拶メッセージ表示中
            case _ShopSubState.GREETING:
                if not self._wm.is_open or self._wm.current != self._greeting_msg:
                    self._shop_command = EnumSelectWindow(
                        self.context.scene.app, 10, 24, 60, list(ShopCommand)
                    )
                    self._wm.push(self._shop_command)
                    self._sub_state = _ShopSubState.MAIN_MENU

            # ★ 2. 「かう / うる」選択中
            case _ShopSubState.MAIN_MENU:
                if self._shop_command is not None:
                    # A. 決定された場合
                    if self._shop_command.result is not None:
                        cmd = self._shop_command.result
                        self._shop_command.result = None

                        match cmd:
                            case ShopCommand.BUY:
                                _shop_items = self._event["items"]

                                self._buy_window = ShopItemSelectWindow(
                                    self.context.scene.app,
                                    75,
                                    24,
                                    110,
                                    _shop_items,
                                    self._item_repository,
                                )
                                self._wm.push(self._buy_window)
                                self._sub_state = _ShopSubState.BUY_LIST

                            case ShopCommand.SELL:
                                pass

                    # B. ★ キャンセルされた場合（_shop_command が閉じた）
                    elif self._wm.current != self._shop_command:
                        self._farewell_msg = MessageWindow(
                            self.context.scene.app,
                            10,
                            130,
                            172,
                            50,
                            speed=2,
                            messages=["また おこしください！"],
                        )
                        self._wm.push(self._farewell_msg)
                        self._sub_state = _ShopSubState.EXITING

            # ★ 3. 商品リスト選択中
            case _ShopSubState.BUY_LIST:
                if self._buy_window is not None:
                    # A. 決定された場合
                    if self._buy_window.result is not None:
                        self._pending_item = self._buy_window.result
                        self._buy_window.result = None

                        self._confirm_msg = MessageWindow(
                            app=self.context.scene.app,
                            x=10,
                            y=130,
                            width=172,
                            height=50,
                            speed=2,
                            messages=[f"{self._pending_item.value} を かいますか？"],
                        )
                        self._wm.push(self._confirm_msg)
                        self._sub_state = _ShopSubState.CONFIRM

                    # B. ★ キャンセルされた場合 ➔ 「かう/うる」メニューに戻る
                    elif self._wm.current == self._shop_command:
                        self._buy_window = None
                        self._sub_state = _ShopSubState.MAIN_MENU

            # ★ 4. 「〇〇をかいますか？ / はい・いいえ」確認中
            case _ShopSubState.CONFIRM:
                # メッセージの文字送りが終わったら「はい/いいえ」ウィンドウを出す
                if (
                    self._confirm_msg is not None
                    and self._confirm_window is None
                    and (
                        self._confirm_msg.is_waiting_input
                        or self._confirm_msg.is_completed
                    )
                ):
                    self._confirm_window = EnumSelectWindow(
                        self.context.scene.app, 10, 80, 60, list(ChoiceCommand)
                    )
                    self._wm.push(self._confirm_window)

                if self._confirm_window is not None:
                    # A. 決定された場合
                    if self._confirm_window.result is not None:
                        choice = self._confirm_window.result
                        self._confirm_window.result = None

                        match choice:
                            case ChoiceCommand.Yes:
                                p = self.context.scene.app.player
                                # 購入処理
                                logs = self._shop_use_case.buy_item(
                                    p, self._pending_item
                                )

                                # ウィンドウを閉じる
                                self._wm.pop()  # _confirm_window を閉じる
                                if self._wm.current == self._confirm_msg:
                                    self._wm.pop()  # _confirm_msg を閉じる

                                self._confirm_window = None
                                self._confirm_msg = None

                                # 完了メッセージ表示
                                self._wm.push(
                                    MessageWindow(
                                        app=self.context.scene.app,
                                        x=10,
                                        y=130,
                                        width=172,
                                        height=50,
                                        speed=2,
                                        messages=logs,
                                    )
                                )
                                self._sub_state = _ShopSubState.BUY_LIST

                            case ChoiceCommand.No:
                                # 「いいえ」の時は閉じて商品リストに戻る
                                self._wm.pop()
                                if self._wm.current == self._confirm_msg:
                                    self._wm.pop()
                                self._confirm_window = None
                                self._confirm_msg = None
                                self._sub_state = _ShopSubState.BUY_LIST

                    # B. ★ キャンセルされた場合 ➔ 商品リストに戻る
                    elif self._wm.current != self._confirm_window:
                        if self._confirm_msg and self._wm.current == self._confirm_msg:
                            self._wm.pop()
                        self._confirm_window = None
                        self._confirm_msg = None
                        self._sub_state = _ShopSubState.BUY_LIST

            # ★ 5. お店を出るメッセージ表示中
            case _ShopSubState.EXITING:
                if not self._wm.is_open:
                    return PopSignal()  # 探索モードへ完全復帰！

        return ModeSignal()

    def draw(self):
        pass
