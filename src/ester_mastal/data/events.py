from .maps import MapId

MAP_EVENTS = {
    # 村人NPC (x=5, y=5)
    (MapId.TOWN, 5, 5): {
        "type": "NPC",
        "name": "むらびと",
        "messages": [
            "りゅうおう は みなみ の ほらあな に いるぞ！",
            "しっかり じゅんび していってね！",
        ],
    },
    # 宿屋 (x=1, y=3)
    (MapId.TOWN, 8, 8): {"type": "INN", "name": "やどや", "price": 10},
    # 武器屋 (x=4, y=2)
    (MapId.TOWN, 4, 2): {
        "type": "SHOP",
        "name": "どうぐや",
        "greeting": "いらっしゃいませ！\nここは どうぐや です。\nなにに しますか？",
        "items": [
            {"id": "herb", "name": "やくそう", "price": 10, "type": "ITEM"},
            {
                "id": "copper_sword",
                "name": "どうのつるぎ",
                "price": 120,
                "type": "WEAPON",
                "atk": 10,
            },
            {
                "id": "leather_armor",
                "name": "かわのよろい",
                "price": 70,
                "type": "ARMOR",
                "def": 4,
            },
        ],
    },
    # 宝箱 (x=8, y=4)
    (MapId.DUNGEON, 8, 4): {
        "type": "CHEST",
        "reward_type": "gold",  # "gold" または "item"
        "reward_value": 50,
        "is_opened": False,
    },
    # ダンジョンの最奥 (x=5, y=2) に竜王を配置
    (MapId.DUNGEON, 5, 2): {
        "type": "BOSS",
        "name": "りゅうおう",
        "messages": [
            "よくぞ ここまで たどりついた！",
            "わしが あくの しはいしゃ りゅうおう だ！",
            "わしの てかとなれば せかいの はんぶんを やろう！",
            "…と でも いうとおもったか！ くらえ！",
        ],
        "monster_id": "deramil",
    },
}
