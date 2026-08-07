from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class ItemType(Enum):
    CONSUMABLE_HP = auto()  # 消耗品
    CONSUMABLE_MP = auto()
    WEAPON = auto()      # 武器
    ARMOR = auto()       # 防具
    KEY = auto()         # 鍵

@dataclass(frozen=True)
class Item:
    name: str
    item_type: ItemType
    price: int
    effect_value: int
    description: str = ""

class ItemCode(Enum):
    # 消耗品
    POTION = auto()
    MAGIC_WATER = auto()

    # 武器
    CLUB = auto()
    COPPER_SWORD = auto()
    KING_SWORD = auto()

    # 防具
    LEATHER_ARMOR = auto()
    IRON_ARMOR = auto()
    KING_ARMOR = auto()

    # 特殊
    CELESTIAL_ORB = auto()
    CELESTIAL_KEY = auto()

class ItemRepository(ABC):
    @abstractmethod
    def find_by_code(self, code: ItemCode) -> Item | None:
        """アイテムコードから Item を取得する（存在しない場合は None）"""

    @abstractmethod
    def get_all(self) -> list[Item]:
        """全アイテムを取得する"""
