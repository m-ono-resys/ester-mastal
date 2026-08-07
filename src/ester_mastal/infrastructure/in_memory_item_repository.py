from ester_mastal.data.items import ITEM_MASTER
from ester_mastal.models.item import Item, ItemCode, ItemRepository


class InMemoryItemRepository(ItemRepository):
    def __init__(self, master_data: dict[ItemCode, Item] = ITEM_MASTER):
        self._master_data = master_data

    def find_by_code(self, code):
        return self._master_data.get(code)

    def get_all(self):
        return list(self._master_data.values()) 