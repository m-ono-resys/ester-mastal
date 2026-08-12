from ..models.item import ItemCode
from .maps import MapId

MAP_EVENTS = {
    # 村人NPC (x=5, y=5)
    (MapId.TOWN, 5, 5): {
        "type": "NPC",
        "name": "むらびと",
        "messages": ["きたに おしろが あるよ"],
    },
    (MapId.CASTLE_1F, 2, 2): {
        "type": "NPC",
        "name": "イフロ",
        "dialogues": [
            {
                "flag": "GOT_ORB",
                "messages": ["イフロ「あとはたのんだぞ！」"],
            },
            {
                "flag": "TALKED_TO_KING",
                "set_flag": "GOT_ORB",
                "give_item": ItemCode.CELESTIAL_ORB,
                "messages": [
                    "イフロ「王さまにきいて ここにきたんだろ。",
                    "ま王のしろのまえには とても高いやまがあるだろ。",
                    "だからぼくがもっている 天の玉をつかうといい。」",
                    "天の玉を てにいれた！",
                ],
            },
            {
                "flag": None,
                "messages": [
                    "イフロ「まずは ２かいの 王さまから話をきいてくれ。」",
                ],
            },
        ],
    },
    (MapId.CASTLE_2F, 6, 3): {
        "type": "NPC",
        "name": "まさたか王",
        "dialogues": [
            {
                "flag": "TALKED_TO_KING",
                "messages": [
                    "まさたか王「といろ よ たのんだぞ。」",
                ],
            },
            {
                "flag": None,
                "set_flag": "TALKED_TO_KING",
                "messages": [
                    "まさたか王「おねがいします どうか ま王をたおしてくれ。",
                    "そのまえに、１かいにいる イフロに話したらいい",
                    "きっと やくに たつだろう。」",
                ],
            },
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
            ItemCode.POTION,
            ItemCode.COPPER_SWORD,
            ItemCode.LEATHER_ARMOR,
        ],
    },
    # 宝箱 (x=8, y=4)
    (MapId.DUNGEON_B1F, 8, 4): {
        "type": "CHEST",
        "reward_type": "gold",  # "gold" または "item"
        "reward_value": 50,
        "is_opened": False,
    },
    # ダンジョンの最奥 (x=5, y=2) に竜王を配置
    # (MapId.DUNGEON, 5, 2): {
    #     "type": "BOSS",
    #     "name": "りゅうおう",
    #     "messages": [
    #         "よくぞ ここまで たどりついた！",
    #         "わしが あくの しはいしゃ りゅうおう だ！",
    #         "わしの てかとなれば せかいの はんぶんを やろう！",
    #         "…と でも いうとおもったか！ くらえ！",
    #     ],
    #     "monster_id": "deramil",
    # },
}
