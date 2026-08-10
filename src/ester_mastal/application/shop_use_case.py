from ..models.item import ItemCode, ItemRepository
from ..models.player import Player


class ShopUseCase:
    def __init__(self, item_repository: ItemRepository):
        self._item_repository = item_repository

    def buy_item(self, player: Player, item_code: ItemCode) -> str:
        item = self._item_repository.find_by_code(item_code)

        if not item:
            return "アイテムが存在しません"

        if player.gold < item.price:
            return ["おかね が たりないよ！"]

        else:
            player.gold -= item.price
            player.inventory.append(item_code)
            return [f"{item.name} を かった！", "まいどあり！"]
