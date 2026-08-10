from dataclasses import dataclass
from enum import Enum, auto


class MapId(Enum):
    WORLD = auto()  # フィールド
    TOWN = auto()  # 街
    DUNGEON = auto()  # ダンジョン


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
    message: str


# ★ 各マップの Tilemap 0 上の位置 (u, v) と エンカウント率の定義
MAP_CONFIG: dict[MapId, MapDefinistion] = {
    MapId.WORLD: MapDefinistion(0, 0, 0.15),
    MapId.TOWN: MapDefinistion(192, 0, 0.0),
    MapId.DUNGEON: MapDefinistion(384, 0, 0.25),
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
    FromPosition(MapId.WORLD, 2, 6): ToPosition(MapId.TOWN, 1, 5, "トーンバットのまち"),
    FromPosition(MapId.TOWN, 0, 4): ToPosition(MapId.WORLD, 2, 7, "そと に でた。"),
    FromPosition(MapId.TOWN, 0, 5): ToPosition(MapId.WORLD, 2, 7, "そと に でた。"),
    FromPosition(MapId.TOWN, 0, 6): ToPosition(MapId.WORLD, 2, 7, "そと に でた。"),
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
