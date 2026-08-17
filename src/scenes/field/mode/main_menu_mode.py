from enum import Enum

from application.item_use_case import ItemUseCase
from application.spell_use_case import SpellUseCase
from infrastructure.in_memory_item_repository import InMemoryItemRepository
from infrastructure.in_memory_spell_repository import InMemorySpellRepository
from ui.enum_select_window import EnumSelectWindow
from ui.equip_item_select_window import EquipItemSelectWindow
from ui.message_window import MessageWindow
from ui.status_window import StatusWindow

from .base_mode import BaseMode, FieldContext
from .signals import ModeSignal, PopSignal


class MenuCommand(Enum):
    Item = "アイテム"
    Spell = "じゅもん"
    Status = "つよさ"


class MainMenuMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)
        self._main_menu = EnumSelectWindow(
            context.scene.app, 10, 24, 60, list(MenuCommand)
        )
        self._wm.push(self._main_menu)

        self._item_window: EnumSelectWindow | None = None
        self._item_usecase = ItemUseCase(InMemoryItemRepository())

        self._spell_window: EnumSelectWindow | None = None
        self._spell_usecase = SpellUseCase(InMemorySpellRepository())

        self._status_window: StatusWindow | None = None

    def update(self):
        if self._main_menu.result is not None:
            cmd = self._main_menu.result
            self._main_menu.result = None

            match cmd:
                case MenuCommand.Item:
                    _items = self._app.player.inventory
                    if not _items:
                        self._wm.push(
                            MessageWindow(
                                app=self._app,
                                messages=["アイテムをもっていない！"],
                            )
                        )
                    else:
                        player = self._app.player
                        equipped_set = {
                            item.name
                            for item in [player.equipped_weapon, player.equipped_armor]
                            if item is not None
                        }

                        self._item_window = EquipItemSelectWindow(
                            self._app,
                            80,
                            24,
                            100,
                            choices=_items,
                            equipped_items=equipped_set,
                        )
                        self._wm.push(self._item_window)
                case MenuCommand.Spell:
                    _spells = self._app.player.spells
                    if not _spells:
                        self._wm.push(
                            MessageWindow(
                                app=self._app,
                                messages=["つかえるじゅもんがない！"],
                            )
                        )
                    else:
                        self._spell_window = EnumSelectWindow(
                            self._app, 80, 24, 100, _spells
                        )
                        self._wm.push(self._spell_window)
                case MenuCommand.Status:
                    self._status_window = StatusWindow(self._app)
                    self._wm.push(self._status_window)

        # 2. アイテム選択ウィンドウが開いている時の判定
        if self._item_window is not None:
            # A. アイテムが選択された場合
            if self._item_window.result is not None:
                selected_item = self._item_window.result
                logs = self._item_usecase.use_item(self._app.player, selected_item)
                self._wm.pop()
                self._wm.push(
                    MessageWindow(
                        app=self._app,
                        messages=logs,
                    )
                )
                self._item_window = None

            # B. キャンセルキー等でアイテムウィンドウが閉じられた場合
            elif self._wm.current != self._item_window:
                self._item_window = None

        if self._spell_window is not None:
            if self._spell_window.result is not None:
                selected_spell = self._spell_window.result
                logs = self._spell_usecase.use_spell(self._app.player, selected_spell)
                self._wm.pop()
                self._wm.push(
                    MessageWindow(
                        app=self._app,
                        messages=logs,
                    )
                )
                self._spell_window = None
            elif self._wm.current != self._spell_window:
                self._spell_window = None

        if self._status_window is not None and self._wm.current != self._status_window:
            self._status_window = None

        if not self._wm.is_open:
            return PopSignal()

        return ModeSignal()

    def draw(self):
        pass
