from enum import Enum

from ..main import App
from ..ui.enum_select_window import EnumSelectWindow, wait_for_menu
from ..ui.window_manager import WindowManager


class MenuCommand(Enum):
    Item = "アイテム"
    Spell = "じゅもん"
    Status = "つよさ"

def menu_routine(app: App, window_manager: WindowManager):
    command_menu = EnumSelectWindow(app, 10, 10, 60, list(MenuCommand))

    selected_cmd: MenuCommand | None = yield from wait_for_menu(window_manager, command_menu)

    match selected_cmd:
        case MenuCommand.Item:
            print("アイテム")

        case MenuCommand.Spell:
            print("じゅもん")

        case MenuCommand.Status:
            print("つよさ")