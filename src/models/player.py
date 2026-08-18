from dataclasses import dataclass, field

from data.maps import MapId

from .item import Item, ItemCode, ItemType
from .spell import SpellCode


@dataclass
class Player:
    name: str
    max_hp: int
    hp: int
    max_mp: int
    mp: int
    base_attack: int  # ★ 素の攻撃力
    base_defense: int  # ★ 素の防御力
    level: int = 1
    exp: int = 0
    gold: int = 0
    spells: list[SpellCode] = field(default_factory=list)
    inventory: list[ItemCode] = field(default_factory=list)

    # ★ インベントリの最大所持数定数（10個）
    MAX_INVENTORY_SIZE: int = 10

    # ★ 装備品データ（初期は何も装備していない）
    equipped_weapon: Item | None = None
    equipped_armor: Item | None = None

    # ★ シーンを跨いで保持する位置データ（初期値を指定）
    x: int = 8
    y: int = 4
    map_id: MapId = MapId.TOWN

    # ★ 実際の攻撃力（素の攻撃力 ＋ 武器の攻撃力）
    @property
    def attack(self) -> int:
        if self.equipped_weapon and self.equipped_weapon.item_type == ItemType.WEAPON:
            return self.base_attack + self.equipped_weapon.effect_value
        return self.base_attack

    # ★ 実際の防御力（素の防御力 ＋ 防具の防御力）
    @property
    def defense(self) -> int:
        if self.equipped_armor and self.equipped_armor.item_type == ItemType.ARMOR:
            return self.base_defense + self.equipped_armor.effect_value
        return self.base_defense

    def equip_weapon(self, weapon: Item) -> bool:
        """武器を装備する。成功すれば True"""
        if weapon.item_type == ItemType.WEAPON:
            self.equipped_weapon = weapon
            return True
        return False

    def equip_armor(self, armor: Item) -> bool:
        """防具を装備する。成功すれば True"""
        if armor.item_type == ItemType.ARMOR:
            self.equipped_armor = armor
            return True
        return False

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def heal_hp(self, amount: int) -> int:
        """HPを回復し、実際に回復した値を返す"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def heal_mp(self, amount: int) -> int:
        """MPを回復し、実際に回復した値を返す"""
        old_mp = self.mp
        self.mp = min(self.max_mp, self.mp + amount)
        return self.hp - old_mp

    def take_damage(self, amount: int) -> int:
        """ダメージを受け、実際に受けたダメージを返す"""
        damage = max(1, amount)
        self.hp = max(0, self.hp - damage)
        return damage

    # --- インベントリ操作 ---

    @property
    def is_inventory_full(self) -> bool:
        """インベントリが満タン（10個以上）か判定"""
        return len(self.inventory) >= self.MAX_INVENTORY_SIZE

    def add_item(self, item_code: ItemCode) -> bool:
        """アイテムをインベントリに追加する。追加成功で True、満タンで失敗なら False"""
        if self.is_inventory_full:
            return False
        self.inventory.append(item_code)
        return True

    def has_item(self, item_code: ItemCode) -> bool:
        return item_code in self.inventory

    def remove_item(self, item_code: ItemCode) -> None:
        if self.has_item(item_code):
            self.inventory.remove(item_code)
