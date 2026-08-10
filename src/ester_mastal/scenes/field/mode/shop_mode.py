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


class _ShopSubState(Enum):
    GREETING = auto()  # 挨拶表示中
    MAIN_MENU = auto()  # 「かう / うる」選択中
    BUY_LIST = auto()  # かう商品リスト選択中
    SELL_LIST = auto()  # うる商品リスト選択中
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
        self._shopping_window: ShopItemSelectWindow | None = None
        self._confirm_window: EnumSelectWindow[ChoiceCommand] | None = None
        self._confirm_msg: MessageWindow | None = None
        self._no_item_msg: MessageWindow | None = None
        self._farewell_msg: MessageWindow | None = None

        self._pending_item: ItemCode | None = None
        self._sub_state = _ShopSubState.GREETING
        self._sell_mode: bool = False

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
                                self._sell_mode = False
                                _shop_items = self._event["items"]

                                self._shopping_window = ShopItemSelectWindow(
                                    self.context.scene.app,
                                    75,
                                    24,
                                    110,
                                    _shop_items,
                                    self._item_repository,
                                )
                                self._wm.push(self._shopping_window)
                                self._sub_state = _ShopSubState.BUY_LIST

                            case ShopCommand.SELL:
                                _shop_items = self.context.scene.app.player.inventory

                                if not _shop_items:
                                    self._no_item_msg = MessageWindow(
                                        self.context.scene.app,
                                        x=10,
                                        y=130,
                                        width=172,
                                        height=50,
                                        speed=2,
                                        messages=["うれるものが ないようだ！"],
                                    )
                                    self._wm.push(self._no_item_msg)

                                else:
                                    self._sell_mode = True
                                    self._shopping_window = ShopItemSelectWindow(
                                        self.context.scene.app,
                                        75,
                                        24,
                                        110,
                                        _shop_items,
                                        self._item_repository,
                                        sell_flag=self._sell_mode,
                                    )
                                    self._wm.push(self._shopping_window)
                                    self._sub_state = _ShopSubState.SELL_LIST

                    # B. キャンセルされた場合
                    else:
                        is_no_item_msg_active = (
                            self._no_item_msg is not None
                            and self._wm.current == self._no_item_msg
                        )

                        if (
                            not self._wm.is_open
                            or self._wm.current != self._shop_command
                        ) and not is_no_item_msg_active:
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

            # ★ 3. かう商品リスト選択中
            case _ShopSubState.BUY_LIST:
                if self._shopping_window is not None:
                    if self._shopping_window.result is not None:
                        self._pending_item = self._shopping_window.result
                        self._shopping_window.result = None

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

                    elif self._wm.current == self._shop_command:
                        self._shopping_window = None
                        self._sub_state = _ShopSubState.MAIN_MENU

            # ★ 4. うる商品リスト選択中
            case _ShopSubState.SELL_LIST:
                p = self.context.scene.app.player

                # 手持ちが売り切れていて売却画面も閉じた場合、売却メッセージ終了後に安全に MAIN_MENU へ戻る
                if not p.inventory and self._shopping_window is None:
                    if self._wm.current == self._shop_command:
                        self._sub_state = _ShopSubState.MAIN_MENU
                    return ModeSignal()

                if self._shopping_window is not None:
                    if self._shopping_window.result is not None:
                        self._pending_item = self._shopping_window.result
                        self._shopping_window.result = None

                        self._confirm_msg = MessageWindow(
                            app=self.context.scene.app,
                            x=10,
                            y=130,
                            width=172,
                            height=50,
                            speed=2,
                            messages=[f"{self._pending_item.value} を うりますか？"],
                        )
                        self._wm.push(self._confirm_msg)
                        self._sub_state = _ShopSubState.CONFIRM

                    elif self._wm.current == self._shop_command:
                        self._shopping_window = None
                        self._sub_state = _ShopSubState.MAIN_MENU

            # ★ 5. 「〇〇をかいますか？ / はい・いいえ」確認中
            case _ShopSubState.CONFIRM:
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
                                if not self._sell_mode:
                                    logs = self._shop_use_case.buy_item(
                                        p, self._pending_item
                                    )
                                else:
                                    logs = self._shop_use_case.sell_item(
                                        p, self._pending_item
                                    )

                                self._wm.pop()
                                if self._wm.current == self._confirm_msg:
                                    self._wm.pop()

                                self._confirm_window = None
                                self._confirm_msg = None

                                # ★ 売り切れた場合はアイテム選択ウィンドウを消去して SELL_LIST 状態を維持する
                                if self._sell_mode and not p.inventory:
                                    if self._shopping_window in self._wm._windows:
                                        self._wm._windows.remove(self._shopping_window)
                                    self._shopping_window = None
                                    self._sub_state = _ShopSubState.SELL_LIST
                                else:
                                    self._sub_state = (
                                        _ShopSubState.SELL_LIST
                                        if self._sell_mode
                                        else _ShopSubState.BUY_LIST
                                    )

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

                            case ChoiceCommand.No:
                                self._wm.pop()
                                if self._wm.current == self._confirm_msg:
                                    self._wm.pop()
                                self._confirm_window = None
                                self._confirm_msg = None
                                self._sub_state = (
                                    _ShopSubState.SELL_LIST
                                    if self._sell_mode
                                    else _ShopSubState.BUY_LIST
                                )

                    # B. キャンセルされた場合
                    elif self._wm.current != self._confirm_window:
                        if self._confirm_msg and self._wm.current == self._confirm_msg:
                            self._wm.pop()
                        self._confirm_window = None
                        self._confirm_msg = None
                        self._sub_state = (
                            _ShopSubState.SELL_LIST
                            if self._sell_mode
                            else _ShopSubState.BUY_LIST
                        )

            # ★ 6. お店を出るメッセージ表示中
            case _ShopSubState.EXITING:
                if not self._wm.is_open:
                    return PopSignal()

        return ModeSignal()

    def draw(self):
        pass
