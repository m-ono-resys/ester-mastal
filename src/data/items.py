from models.item import Item, ItemCode, ItemType

ITEM_MASTER: dict[ItemCode, Item] = {
    ItemCode.POTION: Item(
        ItemCode.POTION.value, ItemType.CONSUMABLE_HP, 5, 20, "HPを 20 かいふくする"
    ),
    ItemCode.MAGIC_WATER: Item(
        ItemCode.MAGIC_WATER.value,
        ItemType.CONSUMABLE_MP,
        10,
        15,
        "MPを 15 かいふくする",
    ),
    ItemCode.CLUB: Item(
        ItemCode.CLUB.value,
        ItemType.WEAPON,
        10,
        10,
        "木で できた こんぼう（こうげき+10）",
    ),
    ItemCode.COPPER_SWORD: Item(
        ItemCode.COPPER_SWORD.value,
        ItemType.WEAPON,
        80,
        24,
        "銅で できた 剣（こうげき+24）",
    ),
    ItemCode.KING_SWORD: Item(
        ItemCode.KING_SWORD.value,
        ItemType.WEAPON,
        0,
        32,
        "まおうを ふういんした 剣（こうげき+32）",
    ),
    ItemCode.LEATHER_ARMOR: Item(
        ItemCode.LEATHER_ARMOR.value,
        ItemType.ARMOR,
        15,
        10,
        "革で できた よろい（まもり+10）",
    ),
    ItemCode.IRON_ARMOR: Item(
        ItemCode.IRON_ARMOR.value,
        ItemType.ARMOR,
        60,
        28,
        "鉄で できた よろい（まもり+28）",
    ),
    ItemCode.KING_ARMOR: Item(
        ItemCode.KING_ARMOR.value,
        ItemType.ARMOR,
        0,
        32,
        "まおうと たたかった よろい（まもり+32）",
    ),
    ItemCode.CELESTIAL_ORB: Item(
        ItemCode.CELESTIAL_ORB.value, ItemType.KEY, 0, 0, "まおうのしろに 入るための 玉"
    ),
    ItemCode.CELESTIAL_KEY: Item(
        ItemCode.CELESTIAL_KEY.value,
        ItemType.KEY,
        0,
        0,
        "まおうのへやに 入るための カギ",
    ),
}
