from enum import Enum, auto

class MapId(Enum):
    WORLD = auto()    # フィールド (tilemap 0)
    TOWN = auto()     # 街 (tilemap 1)
    DUNGEON = auto()  # ダンジョン (tilemap 2)

# ★ ワープ地点の定義: (現在のMapId, x, y) -> 遷移先情報
WARP_POINTS = {
    # 1. フィールドの村 (x=2, y=3) ➔ 街の中へ
    (MapId.WORLD, 2, 3): {
        "target_map": MapId.TOWN,
        "target_x": 5,
        "target_y": 6,
        "message": "まち に はいった！"
    },
    
    # 2. 街の出口 (x=5, y=7) ➔ フィールドへ（街のすぐ下のマスに出る）
    (MapId.TOWN, 5, 7): {
        "target_map": MapId.WORLD,
        "target_x": 2,
        "target_y": 4,
        "message": "フィールド に でた。"
    },
    
    # 3. フィールドの洞窟 (x=8, y=2) ➔ ダンジョンへ
    (MapId.WORLD, 8, 2): {
        "target_map": MapId.DUNGEON,
        "target_x": 1,
        "target_y": 1,
        "message": "くらい ほらあな に はいった…"
    },
    
    # 4. ダンジョンの出口 (x=1, y=0) ➔ フィールドへ
    (MapId.DUNGEON, 1, 0): {
        "target_map": MapId.WORLD,
        "target_x": 8,
        "target_y": 3,
        "message": "ほらあな から でた。"
    }
}

# マップごとのエンカウント率設定
ENCOUNT_RATES = {
    MapId.WORLD: 0.15,   # 15%
    MapId.TOWN: 0.0,     # 街の中は敵が出ない (0%)
    MapId.DUNGEON: 0.25  # ダンジョンは高め (25%)
}