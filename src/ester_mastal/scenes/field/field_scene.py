import random
from enum import Enum, auto
from typing import Any

import pyxel

from ...data.events import MAP_EVENTS
from ...data.maps import MAP_CONFIG, FromPosition, MapId
from ...scenes.field.mode.chest_message_mode import ChestModeData
from ...ui.hud_status_window import HudStatusWindow
from ...ui.window_manager import WindowManager
from ..base_scene import BaseScene
from .mode.base_mode import BaseMode, FieldContext
from .mode.explore_mode import ExploreMode
from .mode.signals import PopSignal, PushSignal

TILE_MAPPING = {
    (0, 1): "GRASS",
    (1, 0): "ENTRANCE",
    (2, 0): "MOUNTAIN",
    (0, 2): "VILLAGE",
    (2, 2): "CASTLE",
    (4, 2): "CAVE",
    (6, 2): "DEMON_CASTLE",
    (0, 6): "WALL",
    (2, 6): "TABLE",
    (0, 8): "FLOOR",
    (4, 6): "BED",
    (0, 10): "CAVE_WALL",
}


class Direction(Enum):
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()


class Mode(Enum):
    EXPLORE = auto()
    MAIN_MENU = auto()
    # SPELL_MENU = auto()
    # ITEM_MENU = auto()
    # STATS_MENU = auto()
    # MESSAGE = auto()
    # INN_CONFIRM = auto()
    # SHOP_MAIN_MENU = auto()
    # SHOP_BUY_MENU = auto()
    # SHOP_SELL_MENU = auto()
    # START_BOSS_BATTLE = auto()


# --- 2. FieldState メインクラス ---


class FieldScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        self.hud = HudStatusWindow(app, 0, 0, 192, 16)

        self.tile_size = 16
        self.player_x = 1
        self.player_y = 1
        self.direction: Direction = Direction.DOWN
        self.current_map_id: MapId = MapId.TOWN

        self.current_event: Any = None
        self.pending_boss_id = None

        self.window_manager = WindowManager()

        self.context = FieldContext(scene=self)

        self.mode_stack: list[BaseMode] = [ExploreMode(self.context)]

    @property
    def current_mode(self) -> BaseMode:
        return self.mode_stack[-1]

    def get_facing_pos(self) -> tuple[int, int]:
        match self.direction:
            case Direction.UP:
                return (self.player_x, self.player_y - 1)
            case Direction.DOWN:
                return (self.player_x, self.player_y + 1)
            case Direction.LEFT:
                return (self.player_x - 1, self.player_y)
            case Direction.RIGHT:
                return (self.player_x + 1, self.player_y)

    def get_tile_type(self, grid_x: int, grid_y: int) -> str:
        cfg = MAP_CONFIG[self.current_map_id]
        tm_x = (cfg.u // 8) + (grid_x * 2)
        tm_y = (cfg.v // 8) + (grid_y * 2)
        tile_info = pyxel.tilemaps[0].pget(tm_x, tm_y)
        return TILE_MAPPING.get(tile_info, "GRASS")

    def can_move_to(self, grid_x: int, grid_y: int) -> bool:
        if grid_x < 0 or grid_x >= 12 or grid_y < 0 or grid_y >= 11:
            return False
        if FromPosition(self.current_map_id, grid_x, grid_y) in MAP_EVENTS:
            return False

        tile_type = self.get_tile_type(grid_x, grid_y)
        return tile_type not in ["MOUNTAIN", "WALL", "CAVE_WALL"]

    def trigger_battle(self):
        from ..battle_scene import BattleScene

        monster_id = random.choice(["entenstr", "rarutaes"])
        monster = self.app.repo.create_monster(monster_id)
        self.app.change_state(BattleScene(self.app, monster))

    def update(self):
        self.window_manager.update()
        signal = self.current_mode.update()

        match signal:
            case PushSignal(new_mode):
                self.mode_stack.append(new_mode)
            case PopSignal():
                if len(self.mode_stack) > 1:
                    self.mode_stack.pop()

    def _draw_map_objects(self):
        """現在のマップにある宝箱などのスプライトを描画"""
        flags = self.app.flags
        for key, (_, data) in MAP_EVENTS.items():
            if key.map_id == self.current_map_id and isinstance(data, ChestModeData):
                px = key.x * self.tile_size
                py = key.y * self.tile_size + 16

                # ★ 中央管理フラグ (app.flags) に flag_key が入っているかでスプライト決定！
                if data.flag_key in flags:
                    u, v = data.opened_sprite  # 開いた宝箱
                else:
                    u, v = data.closed_sprite  # 閉じた宝箱

                pyxel.blt(px, py, 0, u, v, 16, 16, 0)

    def draw(self):
        pyxel.cls(0)

        # 1. マップ & プレイヤー描画
        cfg = MAP_CONFIG[self.current_map_id]
        pyxel.bltm(0, 16, 0, cfg.u, cfg.v, 192, 176)

        self._draw_map_objects()

        pyxel.blt(
            self.player_x * self.tile_size,
            self.player_y * self.tile_size + 16,
            0,
            0,
            0,
            16,
            16,
            8,
        )

        # 2. 上部HUD
        self.hud.draw()

        self.window_manager.draw()
        self.current_mode.draw()
