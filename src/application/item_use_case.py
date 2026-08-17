from models.item import ItemCode, ItemRepository, ItemType
from models.player import Player


class ItemUseCase:
    def __init__(self, item_repository: ItemRepository):
        self._item_repository = item_repository

    def use_item(self, player: Player, item_code: ItemCode) -> list[str]:
        item = self._item_repository.find_by_code(item_code)

        if not item:
            return "アイテムが存在しません"

        if not player.has_item(item_code):
            return "このアイテムをもっていません"

        match item.item_type:
            case ItemType.CONSUMABLE_HP:
                healed = player.heal_hp(
                    item.effect_value
                )  # ★ 実際に回復した値を受け取る
                player.remove_item(item_code)
                return [f"{item.name} を つかった！\nHPが {healed} かいふくした！"]

            case ItemType.CONSUMABLE_MP:
                healed = player.heal_mp(
                    item.effect_value
                )  # ★ 実際に回復した値を受け取る
                player.remove_item(item_code)
                return [f"{item.name} を つかった！\nMPが {healed} かいふくした！"]

            case ItemType.WEAPON:
                if player.equip_weapon(item):
                    return [f"{item.name} を そうびした！"]
                return ["これはそうびできない"]

            case ItemType.ARMOR:
                if player.equip_armor(item):
                    return [f"{item.name} を そうびした！"]
                return ["これはそうびできない"]

            case ItemType.KEY:
                return [f"{item.name} は ここでは つかえない"]

            case _:
                return ["ここでは つかえない"]
