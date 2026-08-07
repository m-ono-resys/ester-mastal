from ester_mastal.models.item import Item, ItemCode, ItemType

ITEM_MASTER: dict[ItemCode, Item] = {
    ItemCode.POTION: Item("きずぐすり", ItemType.CONSUMABLE_HP, 5, 20, "HPを 20 かいふくする"),
    ItemCode.MAGIC_WATER: Item("まほうの水", ItemType.CONSUMABLE_MP, 10, 15, "MPを 15 かいふくする"),
    ItemCode.CLUB: Item("こんぼう", ItemType.WEAPON, 10, 7, "木で できた こんぼう（こうげき+7）"),
    ItemCode.COPPER_SWORD: Item("どうのつるぎ", ItemType.WEAPON, 20, 13, "銅で できた 剣（こうげき+13）"),
    ItemCode.KING_SWORD: Item("王のつるぎ", ItemType.WEAPON, 0, 28, "まおうを ふういんした 剣（こうげき+28）"),
    ItemCode.LEATHER_ARMOR: Item("かわのよろい", ItemType.ARMOR, 15, 10, "革で できた よろい（まもり+10"),
    ItemCode.IRON_ARMOR: Item("てつのよろい", ItemType.ARMOR, 50, 23, "鉄で できた よろい（まもり+23"),
    ItemCode.KING_ARMOR: Item("王のよろい", ItemType.ARMOR, 0, 30, "まおうと たたかった よろい（まもり+30"),
    ItemCode.CELESTIAL_ORB: Item("天の玉", ItemType.KEY, 0, 0, "まおうのしろに 入るための 玉"),
    ItemCode.CELESTIAL_KEY: Item("天のカギ", ItemType.KEY, 0, 0, "まおうのへやに 入るための カギ"),
}