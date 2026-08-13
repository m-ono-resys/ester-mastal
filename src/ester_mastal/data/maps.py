from dataclasses import dataclass
from enum import Enum, auto


class MapId(Enum):
    WORLD = auto()  # 世界（トレートロット）
    TOWN = auto()  # まち（トーンバット）
    CASTLE_1F = auto()  # おしろ（メーマント）1F
    CASTLE_2F = auto()  # おしろ（メーマント）2F
    DUNGEON_B1F = auto()  # ダンジョン（ギントのどうくつ） B1F
    DUNGEON_B2F = auto()  # ダンジョン（ギントのどうくつ） B2F
    DEMON_CASTLE_1F = auto()  # まおうのしろ 1F
    DEMON_CASTLE_2F = auto()  # まおうのしろ 2F
    DEMON_CASTLE_3F = auto()  # まおうのしろ 3F


@dataclass(frozen=True)
class MapDefinistion:
    u: int
    v: int
    encount_rate: float


@dataclass(frozen=True)
class FromPosition:
    map_id: MapId
    x: int
    y: int


@dataclass(frozen=True)
class ToPosition:
    map_id: MapId
    x: int
    y: int
    message: str | None


# ★ 各マップの Tilemap 0 上の位置 (u, v) と エンカウント率の定義
MAP_CONFIG: dict[MapId, MapDefinistion] = {
    MapId.WORLD: MapDefinistion(0, 0, 0.2),
    MapId.TOWN: MapDefinistion(192, 0, 0.0),
    MapId.CASTLE_1F: MapDefinistion(768, 0, 0),
    MapId.CASTLE_2F: MapDefinistion(960, 0, 0),
    MapId.DUNGEON_B1F: MapDefinistion(384, 0, 0),
    MapId.DUNGEON_B2F: MapDefinistion(576, 0, 0),
    MapId.DEMON_CASTLE_1F: MapDefinistion(0, 192, 0),
    MapId.DEMON_CASTLE_2F: MapDefinistion(192, 192, 0),
    MapId.DEMON_CASTLE_3F: MapDefinistion(384, 192, 0),
    # MapId.TOWN: {
    #     "u": 192,  # 例: Tilemap 0 上で横に 192px (24タイル) ズレた場所
    #     "v": 0,
    #     "encount_rate": 0.0,
    # },
    # MapId.DUNGEON: {
    #     "u": 384,  # 例: Tilemap 0 上で横に 384px (48タイル) ズレた場所
    #     "v": 0,
    #     "encount_rate": 0.0,  # エンカウント率　25%
    # },
}

# ★ ワープ地点の定義: (現在のMapId, x, y) -> 遷移先情報
WARP_POINTS: dict[FromPosition, ToPosition] = {
    # トーンバットのまち
    FromPosition(MapId.WORLD, 4, 8): ToPosition(MapId.TOWN, 1, 5, "トーンバットのまち"),
    FromPosition(MapId.TOWN, 0, 4): ToPosition(MapId.WORLD, 4, 9, "そと に でた。"),
    FromPosition(MapId.TOWN, 0, 5): ToPosition(MapId.WORLD, 4, 9, "そと に でた。"),
    FromPosition(MapId.TOWN, 0, 6): ToPosition(MapId.WORLD, 4, 9, "そと に でた。"),
    # ギントのどうくつ
    FromPosition(MapId.WORLD, 2, 2): ToPosition(
        MapId.DUNGEON_B1F, 5, 9, "ギントのどうくつ に はいった…"
    ),
    FromPosition(MapId.DUNGEON_B1F, 5, 9): ToPosition(
        MapId.WORLD, 1, 5, "そと に でた。"
    ),
    # ぎんとのどうくつ階段
    FromPosition(MapId.DUNGEON_B1F, 6, 5): ToPosition(MapId.DUNGEON_B2F, 6, 5, None),
    FromPosition(MapId.DUNGEON_B2F, 6, 5): ToPosition(MapId.DUNGEON_B1F, 6, 5, None),
    FromPosition(MapId.DUNGEON_B2F, 2, 5): ToPosition(MapId.DUNGEON_B1F, 2, 5, None),
    FromPosition(MapId.DUNGEON_B1F, 2, 5): ToPosition(MapId.DUNGEON_B2F, 2, 5, None),
    FromPosition(MapId.DUNGEON_B1F, 1, 1): ToPosition(MapId.DUNGEON_B2F, 1, 1, None),
    FromPosition(MapId.DUNGEON_B2F, 1, 1): ToPosition(MapId.DUNGEON_B1F, 1, 1, None),
    FromPosition(MapId.DUNGEON_B2F, 10, 1): ToPosition(MapId.DUNGEON_B1F, 10, 1, None),
    FromPosition(MapId.DUNGEON_B1F, 10, 1): ToPosition(MapId.DUNGEON_B2F, 10, 1, None),
    FromPosition(MapId.DUNGEON_B1F, 10, 9): ToPosition(MapId.DUNGEON_B2F, 10, 9, None),
    FromPosition(MapId.DUNGEON_B2F, 10, 9): ToPosition(MapId.DUNGEON_B1F, 10, 9, None),
    # メーマントのしろ
    FromPosition(MapId.WORLD, 6, 4): ToPosition(
        MapId.CASTLE_1F, 6, 9, "メーマントのしろ"
    ),
    FromPosition(MapId.CASTLE_1F, 4, 10): ToPosition(
        MapId.WORLD, 6, 5, "そと に でた。"
    ),
    FromPosition(MapId.CASTLE_1F, 5, 10): ToPosition(
        MapId.WORLD, 6, 5, "そと に でた。"
    ),
    FromPosition(MapId.CASTLE_1F, 6, 10): ToPosition(
        MapId.WORLD, 6, 5, "そと に でた。"
    ),
    FromPosition(MapId.CASTLE_1F, 7, 10): ToPosition(
        MapId.WORLD, 6, 5, "そと に でた。"
    ),
    # メーマントのしろ階段
    FromPosition(MapId.CASTLE_1F, 6, 4): ToPosition(MapId.CASTLE_2F, 6, 7, None),
    FromPosition(MapId.CASTLE_2F, 6, 7): ToPosition(MapId.CASTLE_1F, 6, 4, None),
    # まおうのしろ
    FromPosition(MapId.WORLD, 10, 1): ToPosition(
        MapId.DEMON_CASTLE_1F, 5, 9, "まおうのしろ"
    ),
    FromPosition(MapId.DEMON_CASTLE_1F, 5, 10): ToPosition(
        MapId.WORLD, 10, 2, "そと に でた。"
    ),
    FromPosition(MapId.DEMON_CASTLE_1F, 6, 10): ToPosition(
        MapId.WORLD, 10, 2, "そと に でた。"
    ),
    # まおうのしろ階段
    FromPosition(MapId.DEMON_CASTLE_1F, 5, 4): ToPosition(
        MapId.DEMON_CASTLE_2F, 5, 6, None
    ),
    FromPosition(MapId.DEMON_CASTLE_1F, 6, 6): ToPosition(
        MapId.DEMON_CASTLE_2F, 6, 8, None
    ),
    FromPosition(MapId.DEMON_CASTLE_2F, 5, 6): ToPosition(
        MapId.DEMON_CASTLE_1F, 5, 4, None
    ),
    FromPosition(MapId.DEMON_CASTLE_2F, 6, 8): ToPosition(
        MapId.DEMON_CASTLE_1F, 6, 6, None
    ),
    FromPosition(MapId.DEMON_CASTLE_2F, 6, 1): ToPosition(
        MapId.DEMON_CASTLE_3F, 6, 8, None
    ),
    FromPosition(MapId.DEMON_CASTLE_3F, 6, 8): ToPosition(
        MapId.DEMON_CASTLE_2F, 6, 1, None
    ),
    # FromPosition(MapId.DUNGEON, 5, 9): ToPosition(MapId.WORLD, 1, 5, "そと に でた。"),
    # # 3. フィールドの洞窟 (x=8, y=2) ➔ ダンジョンへ
    # (MapId.WORLD, 1, 4): {
    #     "target_map": MapId.DUNGEON,
    #     "target_x": 1,
    #     "target_y": 1,
    #     "message": "ギントのどうくつ に はいった…",
    # },
    # # 4. ダンジョンの出口 (x=1, y=0) ➔ フィールドへ
    # (MapId.DUNGEON, 1, 0): {
    #     "target_map": MapId.WORLD,
    #     "target_x": 1,
    #     "target_y": 5,
    #     "message": "ギントのどうくつ から でた。",
    # },
}

# マップごとのエンカウント率設定
# ENCOUNT_RATES = {
#     MapId.WORLD: 0.15,   # 15%
#     MapId.TOWN: 0.0,     # 街の中は敵が出ない (0%)
#     MapId.DUNGEON: 0.25  # ダンジョンは高め (25%)
# }
