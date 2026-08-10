import math

from ..models.item import ItemCode, ItemRepository
from ..models.player import Player


class ShopUseCase:
    def __init__(self, item_repository: ItemRepository):
        self._item_repository = item_repository

    def buy_item(self, player: Player, item_code: ItemCode) -> str:
        item = self._item_repository.find_by_code(item_code)

        if not item:
            return ["そんなアイテムはないよ！"]

        if player.gold < item.price:
            return ["おかね が たりないよ！"]

        else:
            player.gold -= item.price
            player.inventory.append(item_code)
            return [f"{item.name} を かった！", "まいどあり！"]

    def sell_item(self, player: Player, item_code: ItemCode) -> str:
        item = self._item_repository.find_by_code(item_code)

        if not item:
            return ["そんなアイテムはないよ！"]

        if not item_code in player.inventory:
            return ["そのアイテムはもっていないよ！"]

        else:
            idx = player.inventory.index(item_code)
            item_name = item.name
            sell_price = math.ceil(item.price / 2)
            player.inventory.pop(idx)
            player.gold += sell_price
            return [f"{item_name} を {sell_price}G で うった！", "まいどあり！"]
