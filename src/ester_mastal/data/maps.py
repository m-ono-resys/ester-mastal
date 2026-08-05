from enum import Enum, auto


class MapId(Enum):
    WORLD = auto()  # フィールド
    TOWN = auto()  # 街
    DUNGEON = auto()  # ダンジョン


# ★ 各マップの Tilemap 0 上の位置 (u, v) と エンカウント率の定義
MAP_CONFIG = {
    MapId.WORLD: {
        "u": 0,
        "v": 0,
        "encount_rate": 0.0,  # エンカウント率　15%
    },
    MapId.TOWN: {
        "u": 192,  # 例: Tilemap 0 上で横に 192px (24タイル) ズレた場所
        "v": 0,
        "encount_rate": 0.0,
    },
    MapId.DUNGEON: {
        "u": 384,  # 例: Tilemap 0 上で横に 384px (48タイル) ズレた場所
        "v": 0,
        "encount_rate": 0.0,  # エンカウント率　25%
    },
}

# ★ ワープ地点の定義: (現在のMapId, x, y) -> 遷移先情報
WARP_POINTS = {
    # 1. フィールドの村 (x=2, y=6) ➔ 街の中へ
    (MapId.WORLD, 2, 6): {
        "target_map": MapId.TOWN,
        "target_x": 1,
        "target_y": 5,
        "message": "トーンバットのまち",
    },
    # 2. 街の出口 (x=2, y=7) ➔ フィールドへ（街のすぐ下のマスに出る）
    (MapId.TOWN, 0, 4): {
        "target_map": MapId.WORLD,
        "target_x": 2,
        "target_y": 7,
        "message": "そと に でた。",
    },
    (MapId.TOWN, 0, 5): {
        "target_map": MapId.WORLD,
        "target_x": 2,
        "target_y": 7,
        "message": "そと に でた。",
    },
    (MapId.TOWN, 0, 6): {
        "target_map": MapId.WORLD,
        "target_x": 2,
        "target_y": 7,
        "message": "そと に でた。",
    },
    # 3. フィールドの洞窟 (x=8, y=2) ➔ ダンジョンへ
    (MapId.WORLD, 1, 4): {
        "target_map": MapId.DUNGEON,
        "target_x": 1,
        "target_y": 1,
        "message": "ギントのどうくつ に はいった…",
    },
    # 4. ダンジョンの出口 (x=1, y=0) ➔ フィールドへ
    (MapId.DUNGEON, 1, 0): {
        "target_map": MapId.WORLD,
        "target_x": 1,
        "target_y": 5,
        "message": "ギントのどうくつ から でた。",
    },
}

# マップごとのエンカウント率設定
# ENCOUNT_RATES = {
#     MapId.WORLD: 0.15,   # 15%
#     MapId.TOWN: 0.0,     # 街の中は敵が出ない (0%)
#     MapId.DUNGEON: 0.25  # ダンジョンは高め (25%)
# }
