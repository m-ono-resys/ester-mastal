from enum import StrEnum

from models.item import ItemCode
from models.monster import MonsterCode
from scenes.field.mode.base_mode import BaseModeData
from scenes.field.mode.boss_message_mode import BossMessageMode, BossMessageModeData
from scenes.field.mode.chest_message_mode import ChestMessageMode, ChestModeData
from scenes.field.mode.extend_message_mode import (
    Dialogue,
    ExtendMessageMode,
    ExtendMessageModeData,
)
from scenes.field.mode.gate_message_mode import GateMessageModeData, SwitchModeData
from scenes.field.mode.inn_mode import InnMode, InnModeData
from scenes.field.mode.message_mode import MessageMode, MessageModeData
from scenes.field.mode.shop_mode import ShopMode, ShopModeData
from scenes.field.strategies.event_strategies import ModeLauncherStrategy
from scenes.field.strategies.event_strategy import EventStrategy

from .maps import FromPosition, MapId

message_strat = ModeLauncherStrategy(MessageMode)
ext_message_strat = ModeLauncherStrategy(ExtendMessageMode)
inn_strat = ModeLauncherStrategy(InnMode)
shop_strat = ModeLauncherStrategy(ShopMode)
chest_strat = ModeLauncherStrategy(ChestMessageMode)
boss_strat = ModeLauncherStrategy(BossMessageMode)


class EventFlag(StrEnum):
    TALKED_TO_KING = "TALKED_TO_KING"
    GOT_ORB = "GOT_ORB"
    OPENED_CHEST_CASTLE_1 = "CHEST_C_10_9"
    OPENED_CHEST_CASTLE_2 = "CHEST_C_9_1"
    OPENED_CHEST_CASTLE_3 = "CHEST_C_10_1"
    OPENED_CHEST_DUNGEON_1 = "OPENED_CHEST_DUNGEON_1"
    OPENED_CHEST_DUNGEON_2 = "OPENED_CHEST_DUNGEON_2"
    OPENED_CHEST_DUNGEON_3 = "OPENED_CHEST_DUNGEON_3"
    OPENED_CHEST_DUNGEON_4 = "OPENED_CHEST_DUNGEON_4"
    DEFEATED_SANTROTO = "DEFEATED_SANTROTO"
    OPENED_MOUNTAIN = "OPENED_MOUNTAIN"
    SWITCH_DEMON_CASTLE_1 = "SWITCH_DEMON_CASTLE_1"
    SWITCH_DEMON_CASTLE_2 = "SWITCH_DEMON_CASTLE_2"
    SWITCH_DEMON_CASTLE_3 = "SWITCH_DEMON_CASTLE_3"
    SWITCH_DEMON_CASTLE_4 = "SWITCH_DEMON_CASTLE_4"
    DEFEATED_DERAMILE = "DEFEATED_DERAMILE"
    PLAYER_DIED = "PLAYER_DIED"


MAP_EVENTS: dict[FromPosition, tuple[EventStrategy, BaseModeData | None]] = {
    FromPosition(MapId.WORLD, 10, 2): (
        ext_message_strat,
        GateMessageModeData(
            name=None,
            dialogues=[
                Dialogue(
                    set_flag=EventFlag.OPENED_MOUNTAIN,
                    flag=EventFlag.GOT_ORB,
                    messages=[
                        f"{ItemCode.CELESTIAL_ORB.value} が ひかりかがやく！",
                        "やま が くずれさった！",
                    ],
                ),
                Dialogue(
                    flag=None,
                    messages=[
                        "なにかの くぼみ が ある...",
                        "ふしぎな ちから で つうこう できない！",
                    ],
                ),
            ],
            sprite_u=48,
            sprite_v=32,
            colkey=8,
        ),
    ),
    FromPosition(MapId.TOWN, 5, 5): (
        message_strat,
        MessageModeData(name="むらびと", messages=["きたに おしろが あるよ"]),
    ),
    FromPosition(MapId.TOWN, 8, 3): (
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
                ItemCode.CLUB,
                ItemCode.COPPER_SWORD,
                ItemCode.LEATHER_ARMOR,
                ItemCode.IRON_ARMOR,
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
    FromPosition(MapId.CASTLE_1F, 10, 8): (
        chest_strat,
        ChestModeData(flag_key=EventFlag.OPENED_CHEST_CASTLE_1, reward_gold=30),
    ),
    FromPosition(MapId.CASTLE_1F, 9, 1): (
        chest_strat,
        ChestModeData(
            flag_key=EventFlag.OPENED_CHEST_CASTLE_2, reward_item=ItemCode.POTION
        ),
    ),
    FromPosition(MapId.CASTLE_1F, 10, 1): (
        chest_strat,
        ChestModeData(
            flag_key=EventFlag.OPENED_CHEST_CASTLE_3, reward_item=ItemCode.LEATHER_ARMOR
        ),
    ),
    FromPosition(MapId.DUNGEON_B2F, 3, 3): (
        chest_strat,
        ChestModeData(flag_key=EventFlag.OPENED_CHEST_DUNGEON_1, reward_gold=50),
    ),
    FromPosition(MapId.DUNGEON_B2F, 8, 2): (
        chest_strat,
        ChestModeData(
            flag_key=EventFlag.OPENED_CHEST_DUNGEON_2, reward_item=ItemCode.POTION
        ),
    ),
    FromPosition(MapId.DUNGEON_B2F, 10, 4): (
        chest_strat,
        ChestModeData(
            flag_key=EventFlag.OPENED_CHEST_DUNGEON_3, reward_item=ItemCode.KING_ARMOR
        ),
    ),
    FromPosition(MapId.DUNGEON_B2F, 10, 5): (
        chest_strat,
        ChestModeData(
            flag_key=EventFlag.OPENED_CHEST_DUNGEON_4, reward_item=ItemCode.KING_SWORD
        ),
    ),
    FromPosition(MapId.DUNGEON_B2F, 8, 6): (
        boss_strat,
        BossMessageModeData(
            name=MonsterCode.SANTROTO.value,
            messages=[
                "よくここまできた。わたしのうしろには、たからばこがある。",
                "それを手に入れたいのなら、わたしとたたかえ。",
            ],
            monster_code=MonsterCode.SANTROTO,
            sprite_u=0,
            sprite_v=16,
            sprite_w=16,
            sprite_h=16,
            colkey=14,
            defeated_flag=EventFlag.DEFEATED_SANTROTO,
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_2F, 2, 2): (
        ext_message_strat,
        SwitchModeData(
            name="スイッチ",
            flag_key=EventFlag.SWITCH_DEMON_CASTLE_1,
            dialogues=[
                Dialogue(
                    flag=EventFlag.SWITCH_DEMON_CASTLE_1,
                    messages=["スイッチ は すでに おされている。"],
                ),
                Dialogue(
                    flag=None,
                    set_flag=EventFlag.SWITCH_DEMON_CASTLE_1,  # ★ スイッチONフラグを中央にセット！
                    messages=[
                        "スイッチ を おした！",
                        "どこかで とびら が ひらく おと が した！",
                    ],
                ),
            ],
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_2F, 2, 7): (
        ext_message_strat,
        SwitchModeData(
            name="スイッチ",
            flag_key=EventFlag.SWITCH_DEMON_CASTLE_2,
            dialogues=[
                Dialogue(
                    flag=EventFlag.SWITCH_DEMON_CASTLE_2,
                    messages=["スイッチ は すでに おされている。"],
                ),
                Dialogue(
                    flag=None,
                    set_flag=EventFlag.SWITCH_DEMON_CASTLE_2,  # ★ スイッチONフラグを中央にセット！
                    messages=[
                        "スイッチ を おした！",
                        "どこかで とびら が ひらく おと が した！",
                    ],
                ),
            ],
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_2F, 9, 2): (
        ext_message_strat,
        SwitchModeData(
            name="スイッチ",
            flag_key=EventFlag.SWITCH_DEMON_CASTLE_3,
            dialogues=[
                Dialogue(
                    flag=EventFlag.SWITCH_DEMON_CASTLE_3,
                    messages=["スイッチ は すでに おされている。"],
                ),
                Dialogue(
                    flag=None,
                    set_flag=EventFlag.SWITCH_DEMON_CASTLE_3,  # ★ スイッチONフラグを中央にセット！
                    messages=[
                        "スイッチ を おした！",
                        "どこかで とびら が ひらく おと が した！",
                    ],
                ),
            ],
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_2F, 9, 7): (
        ext_message_strat,
        SwitchModeData(
            name="スイッチ",
            flag_key=EventFlag.SWITCH_DEMON_CASTLE_4,
            dialogues=[
                Dialogue(
                    flag=EventFlag.SWITCH_DEMON_CASTLE_4,
                    messages=["スイッチ は すでに おされている。"],
                ),
                Dialogue(
                    flag=None,
                    set_flag=EventFlag.SWITCH_DEMON_CASTLE_4,  # ★ スイッチONフラグを中央にセット！
                    messages=[
                        "スイッチ を おした！",
                        "どこかで とびら が ひらく おと が した！",
                    ],
                ),
            ],
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_3F, 2, 3): (
        ext_message_strat,
        GateMessageModeData(
            dialogues=[
                Dialogue(
                    set_flag=EventFlag.SWITCH_DEMON_CASTLE_1,
                    flag=EventFlag.SWITCH_DEMON_CASTLE_1,
                    messages=["とびら は ひらいている。"],
                ),
                Dialogue(
                    messages=["とびらがしまっている。", "かぎでは あかないみたいだ"],
                ),
            ],
            sprite_u=80,
            sprite_v=32,
            colkey=0,
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_3F, 3, 3): (
        ext_message_strat,
        GateMessageModeData(
            dialogues=[
                Dialogue(
                    set_flag=EventFlag.SWITCH_DEMON_CASTLE_2,
                    flag=EventFlag.SWITCH_DEMON_CASTLE_2,
                    messages=["とびら は ひらいている。"],
                ),
                Dialogue(
                    messages=["とびらがしまっている。", "かぎでは あかないみたいだ"],
                ),
            ],
            sprite_u=80,
            sprite_v=32,
            colkey=0,
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_3F, 8, 3): (
        ext_message_strat,
        GateMessageModeData(
            dialogues=[
                Dialogue(
                    set_flag=EventFlag.SWITCH_DEMON_CASTLE_3,
                    flag=EventFlag.SWITCH_DEMON_CASTLE_3,
                    messages=["とびら は ひらいている。"],
                ),
                Dialogue(
                    messages=["とびらがしまっている。", "かぎでは あかないみたいだ"],
                ),
            ],
            sprite_u=80,
            sprite_v=32,
            colkey=0,
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_3F, 9, 3): (
        ext_message_strat,
        GateMessageModeData(
            dialogues=[
                Dialogue(
                    set_flag=EventFlag.SWITCH_DEMON_CASTLE_4,
                    flag=EventFlag.SWITCH_DEMON_CASTLE_4,
                    messages=["とびら は ひらいている。"],
                ),
                Dialogue(
                    messages=["とびらがしまっている。", "かぎでは あかないみたいだ"],
                ),
            ],
            sprite_u=80,
            sprite_v=32,
            colkey=0,
        ),
    ),
    FromPosition(MapId.DEMON_CASTLE_3F, 6, 1): (
        boss_strat,
        BossMessageModeData(
            name=MonsterCode.DERAMILE.value,
            messages=[
                "よくぞここまできた。もうむかしのしっぱいはぜったいにしない かかってこい！",
            ],
            monster_code=MonsterCode.DERAMILE,
            sprite_u=16,
            sprite_v=16,
            sprite_w=16,
            sprite_h=16,
            colkey=0,
            defeated_flag=EventFlag.DEFEATED_DERAMILE,
            # victory_messages=[
            #     "まおう デラミール は ついに たおれた！",
            #     "せかい に へいわ が もどった！",
            #     "ありがとう たびの ゆうしゃ よ！",
            # ],
        ),
    ),
}
