MAP_EVENTS = {
    # 村人NPC (x=3, y=1)
    (3, 1): {
        "type": "NPC",
        "name": "むらびと",
        "messages": [
            "りゅうおう は みなみ の ほらあな に いるぞ！",
            "しっかり じゅんび していってね！",
        ],
    },
    # 宿屋 (x=1, y=3)
    (1, 3): {"type": "INN", "name": "やどや", "price": 10},
    # 武器屋 (x=8, y=1)
    (8, 1): {
        "type": "SHOP",
        "name": "ぶきや",
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
    (8, 4): {
        "type": "CHEST",
        "reward_type": "gold",  # "gold" または "item"
        "reward_value": 50,
        "is_opened": False,
    },
}
