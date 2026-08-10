from enum import Enum

from ....application.item_use_case import ItemUseCase
from ....infrastructure.in_memory_item_repository import InMemoryItemRepository
from ....ui.enum_select_window import EnumSelectWindow
from ....ui.message_window import MessageWindow
from .base_mode import BaseMode, FieldContext
from .signals import ModeSignal, PopSignal


class MenuCommand(Enum):
    Item = "アイテム"
    Spell = "じゅもん"
    Status = "つよさ"


class MainMenuMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)
        self._wm = context.scene.window_manager
        self._main_menu = EnumSelectWindow(
            context.scene.app, 10, 24, 60, list(MenuCommand)
        )
        self._wm.push(self._main_menu)

        self._item_window: EnumSelectWindow | None = None
        self._item_usecase = ItemUseCase(InMemoryItemRepository())

    def update(self):
        if self._main_menu.result is not None:
            cmd = self._main_menu.result
            self._main_menu.result = None

            match cmd:
                case MenuCommand.Item:
                    _items = self.context.scene.app.player.inventory
                    if not _items:
                        self._wm.push(
                            MessageWindow(
                                app=self.context.scene.app,
                                x=10,
                                y=130,
                                width=172,
                                height=50,
                                speed=2,
                                messages=["アイテムをもっていません"],
                            )
                        )
                    else:
                        self._item_window = EnumSelectWindow(
                            self.context.scene.app, 80, 24, 100, _items
                        )
                        self._wm.push(self._item_window)
                case MenuCommand.Spell:
                    print("じゅもん")
                case MenuCommand.Status:
                    print("つよさ")

        # 2. アイテム選択ウィンドウが開いている時の判定
        if self._item_window is not None:
            # A. アイテムが選択された場合
            if self._item_window.result is not None:
                selected_item = self._item_window.result
                log = self._item_usecase.use_item(
                    self.context.scene.app.player, selected_item
                )
                self._wm.pop()
                self._wm.push(
                    MessageWindow(
                        app=self.context.scene.app,
                        x=10,
                        y=130,
                        width=172,
                        height=50,
                        speed=2,
                        messages=[log],
                    )
                )
                self._item_window = None

            # B. キャンセルキー等でアイテムウィンドウが閉じられた場合
            elif self._wm.current != self._item_window:
                self._item_window = None

        if not self._wm.is_open:
            return PopSignal()

        return ModeSignal()

    def draw(self):
        pass
