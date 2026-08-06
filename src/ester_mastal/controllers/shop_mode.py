from enum import Enum, auto

import pyxel

from ..ui.input import is_cancel, is_confirm, navigate_menu
from ..ui.menu import EnumMenu
from ..ui.window import draw_window


class ShopState(Enum):
    GREETING = auto()
    BUY = "かう"
    SELL = "うる"
    EXIT = "やめる"


class ShopMode:
    def __init__(self, player, msg_box, font):
        self.player = player
        self.msg_box = msg_box
        self.font = font
        self.sub_cursor = 0
        self.shop_cursor = 0
        self.current_event = None
        self.shop_main_menu = EnumMenu(
            x=50,
            y=60,
            w=60,
            choices=[ShopState.BUY, ShopState.SELL, ShopState.EXIT],
            font=font,
        )

    def start(self, event):
        """道具屋イベント開始時に初期化"""
        self.current_event = event
        self.sub_cursor = 0
        self.shop_cursor = 0

    def update(self) -> bool:
        match self.shop_main_menu.update():
            case ShopState.BUY:
                # 買う処理
                return False

            case ShopState.SELL:
                # 売る処理
                return False

            case ShopState.EXIT | None | _:
                self.msg_box.push_messages(["また おこしください！"])
                return True

    # --- 「かう / うる」選択の処理 ---
    def update_main(self) -> str:  # 次のモード名を文字列またはEnumで返す
        self.sub_cursor = navigate_menu(2, self.sub_cursor)
        if is_cancel():
            self.msg_box.push_messages(["また おこしください！"])
            return "EXIT"
        elif is_confirm():
            if self.sub_cursor == 0:
                return "BUY_MENU"
            else:
                if not self.player.items:
                    self.msg_box.push_messages(["うれる どうぐを もっていない！"])
                    return "MESSAGE_MAIN"
                return "SELL_MENU"
        return "MAIN"

    def draw_main(self):
        draw_window(10, 120, 172, 60)
        pyxel.text(18, 128, "いらっしゃいませ！", 7, self.font)
        pyxel.text(18, 140, "ここは どうぐや です。", 7, self.font)
        pyxel.text(18, 152, "なにに しますか？", 7, self.font)
        draw_menu_window(10, 45, 60, 42, ["かう", "うる"], self.sub_cursor, self.font)

    # --- 「かう」処理 ---
    def update_buy(self) -> str:
        items = self.current_event["items"]
        if is_cancel():
            return "MAIN"

        self.shop_cursor = navigate_menu(len(items), self.shop_cursor)
        if is_confirm():
            item = items[self.shop_cursor]
            if self.player.gold < item["price"]:
                self.msg_box.push_messages(["ゴールド が たりないようです。"])
            else:
                self.player.gold -= item["price"]
                match item["type"]:
                    case "ITEM":
                        self.player.items.append(item["id"])
                    case "WEAPON":
                        self.player.equip_weapon(item["name"], item["atk"])
                    case "ARMOR":
                        self.player.equip_armor(item["name"], item["def"])
                self.msg_box.push_messages(
                    [f"{item['name']} を かった！", "まいど ありがとうございます！"]
                )
            return "MESSAGE_BUY"
        return "BUY"

    def draw_buy(self):
        draw_window(10, 24, 172, 22)
        pyxel.text(18, 31, f"しょじきん: {self.player.gold}G", 7, self.font)
        items_texts = [
            f"{i['name']} ({i['price']}G)" for i in self.current_event["items"]
        ]
        draw_menu_window(10, 50, 172, 70, items_texts, self.shop_cursor, self.font)
