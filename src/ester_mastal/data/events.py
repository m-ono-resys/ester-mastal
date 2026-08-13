from enum import StrEnum

from ..models.item import ItemCode
from ..scenes.field.mode.base_mode import BaseModeData
from ..scenes.field.mode.chest_message_mode import ChestMessageMode, ChestModeData
from ..scenes.field.mode.extend_message_mode import (
    Dialogue,
    ExtendMessageMode,
    ExtendMessageModeData,
)
from ..scenes.field.mode.inn_mode import InnMode, InnModeData
from ..scenes.field.mode.message_mode import MessageMode, MessageModeData
from ..scenes.field.mode.shop_mode import ShopMode, ShopModeData
from ..scenes.field.strategies.event_strategies import ModeLauncherStrategy
from ..scenes.field.strategies.event_strategy import EventStrategy
from .maps import FromPosition, MapId

message_strat = ModeLauncherStrategy(MessageMode)
ext_message_strat = ModeLauncherStrategy(ExtendMessageMode)
inn_strat = ModeLauncherStrategy(InnMode)
shop_strat = ModeLauncherStrategy(ShopMode)
chest_strat = ModeLauncherStrategy(ChestMessageMode)


class EventFlag(StrEnum):
    TALKED_TO_KING = "TALKED_TO_KING"
    GOT_ORB = "GOT_ORB"
    OPENED_CHEST_CASTLE_1 = "CHEST_C_10_9"
    OPENED_CHEST_CASTLE_2 = "CHEST_C_9_1"
    OPENED_CHEST_CASTLE_3 = "CHEST_C_10_1"
    OPENED_CHEST_DUNGEON_1 = "CHEST_D_8_4"


MAP_EVENTS: dict[FromPosition, tuple[EventStrategy, BaseModeData | None]] = {
    # 村人NPC (x=5, y=5)
    FromPosition(MapId.TOWN, 5, 5): (
        message_strat,
        MessageModeData(name="むらびと", messages=["きたに おしろが あるよ"]),
    ),
    # 宿屋 (x=1, y=3)
    FromPosition(MapId.TOWN, 8, 8): (
        inn_strat,
        InnModeData(
            name="おかあさん",
            greeting_messages=["おかえりなさい\n やすんでいくかい？"],
            done_messages=["よく ねむれたかい？", "いってらっしゃい！"],
            cancel_messages=["むりしないでね"],
        ),
    ),
    FromPosition(MapId.TOWN, 4, 2): (
        shop_strat,
        ShopModeData(
            name="どうぐや",
            items=[
                ItemCode.POTION,
                ItemCode.COPPER_SWORD,
                ItemCode.LEATHER_ARMOR,
            ],
            greeting_messages=[
                "いらっしゃいませ！\nここは どうぐや です。\nなにに しますか？"
            ],
            cancel_messages=["また おこしください！"],
        ),
    ),
    FromPosition(MapId.CASTLE_1F, 2, 2): (
        ext_message_strat,
        ExtendMessageModeData(
            name="イフロ",
            dialogues=[
                Dialogue(flag=EventFlag.GOT_ORB, messages=["あとはたのんだぞ！"]),
                Dialogue(
                    set_flag=EventFlag.GOT_ORB,
                    messages=[
                        "王さまにきいて ここにきたんだろ。",
                        "ま王のしろのまえには とても高いやまがあるだろ。",
                        "だからぼくがもっている 天の玉をつかうといい。",
                        "天の玉を てにいれた！",
                    ],
                    flag=EventFlag.TALKED_TO_KING,
                    reward_item=ItemCode.CELESTIAL_ORB,
                ),
                Dialogue(messages=["まずは ２かいの 王さまから話をきいてくれ。"]),
            ],
        ),
    ),
    FromPosition(MapId.CASTLE_2F, 6, 3): (
        ext_message_strat,
        ExtendMessageModeData(
            name="まさたか王",
            dialogues=[
                Dialogue(
                    flag=EventFlag.TALKED_TO_KING, messages=["といろ よ たのんだぞ。"]
                ),
                Dialogue(
                    set_flag=EventFlag.TALKED_TO_KING,
                    messages=[
                        "おねがいします どうか ま王をたおしてくれ。",
                        "そのまえに、１かいにいる イフロに話したらいい",
                        "きっと やくに たつだろう。",
                    ],
                ),
            ],
        ),
    ),
    FromPosition(MapId.CASTLE_1F, 10, 9): (
        chest_strat,
        ChestModeData(flag_key=EventFlag.OPENED_CHEST_CASTLE_1, reward_gold=30),
    ),
    FromPosition(MapId.CASTLE_1F, 9, 1): (
        chest_strat,
        ChestModeData(flag_key=EventFlag.OPENED_CHEST_CASTLE_2, reward_item=ItemCode.POTION),
    ),
    FromPosition(MapId.CASTLE_1F, 10, 1): (
        chest_strat,
        ChestModeData(flag_key=EventFlag.OPENED_CHEST_CASTLE_3, reward_item=ItemCode.LEATHER_ARMOR),
    ),
    FromPosition(MapId.DUNGEON_B1F, 8, 4): (
        chest_strat,
        ChestModeData(flag_key=EventFlag.OPENED_CHEST_DUNGEON_1, reward_gold=100),
    ),
    # {
    #     "type": "CHEST",
    #     "reward_type": "gold",  # "gold" または "item"
    #     "reward_value": 50,
    #     "is_opened": False,
    #     "closed_sprite": (16, 32),  # ★ 閉じた宝箱の (u, v) 座標
    #     "opened_sprite": (32, 32),  # ★ 開いた宝箱の (u, v) 座標
    # },
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
