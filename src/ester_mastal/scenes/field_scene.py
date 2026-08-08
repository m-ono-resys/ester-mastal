import random
from enum import Enum, auto

import pyxel

from ester_mastal.ui.hud_status_window import HudStatusWindow

from ..data.events import MAP_EVENTS
from ..data.maps import MAP_CONFIG, WARP_POINTS, MapId
from ..ui.input import is_cancel, is_confirm, navigate_menu
from ..ui.menu import draw_menu_window
from ..ui.message_window import MessageWindow
from ..ui.window import draw_window
from .base_scene import BaseScene

# --- 1. 定数・共通ヘルパー関数 (DRY原則) ---

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
}


class Direction(Enum):
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()


class Mode(Enum):
    EXPLORE = auto()
    MAIN_MENU = auto()
    SPELL_MENU = auto()
    ITEM_MENU = auto()
    STATS_MENU = auto()
    MESSAGE = auto()
    INN_CONFIRM = auto()
    SHOP_MAIN_MENU = auto()
    SHOP_BUY_MENU = auto()
    SHOP_SELL_MENU = auto()
    START_BOSS_BATTLE = auto()


# --- 2. FieldState メインクラス ---


class FieldScene(BaseScene):
    def __init__(self, app):
        super().__init__(app)

        self.hud = HudStatusWindow(app, 0, 0, 192, 16)

        self.tile_size = 16
        self.player_x = 1
        self.player_y = 1
        self.direction: Direction = Direction.DOWN
        self.current_map_id: MapId = MapId.WORLD

        self.mode: Mode = Mode.EXPLORE
        self.return_mode: Mode = Mode.EXPLORE
        self.cursor = 0
        self.sub_cursor = 0
        self.shop_cursor = 0

        self.current_event = None
        self.pending_boss_id = None

        self.msg_box = MessageWindow(
            app=app,
            x=10,
            y=130,
            width=172,
            height=50,
            speed=2,
        )

        # ★ Dispatcher テーブル（モードと更新/描画メソッドのバインディング）
        self._update_handlers = {
            Mode.EXPLORE: self._update_explore,
            Mode.MAIN_MENU: self._update_main_menu,
            Mode.SPELL_MENU: self._update_spell_menu,
            Mode.ITEM_MENU: self._update_item_menu,
            Mode.STATS_MENU: self._update_stats_menu,
            Mode.INN_CONFIRM: self._update_inn_confirm,
            Mode.SHOP_MAIN_MENU: self._update_shop_main_menu,
            Mode.SHOP_BUY_MENU: self._update_shop_buy_menu,
            Mode.SHOP_SELL_MENU: self._update_shop_sell_menu,
            Mode.MESSAGE: self._update_message,
        }

        self._draw_handlers = {
            Mode.MAIN_MENU: self._draw_menu_overlay,
            Mode.SPELL_MENU: self._draw_menu_overlay,
            Mode.ITEM_MENU: self._draw_menu_overlay,
            Mode.STATS_MENU: self._draw_menu_overlay,
            Mode.INN_CONFIRM: self._draw_inn_confirm,
            Mode.SHOP_MAIN_MENU: self._draw_shop_main_menu,
            Mode.SHOP_BUY_MENU: self._draw_shop_buy_menu,
            Mode.SHOP_SELL_MENU: self._draw_shop_sell_menu,
            Mode.MESSAGE: self.msg_box.draw,
        }

    # --- ヘルパーメソッド ---

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
        tm_x = (cfg["u"] // 8) + (grid_x * 2)
        tm_y = (cfg["v"] // 8) + (grid_y * 2)
        tile_info = pyxel.tilemaps[0].pget(tm_x, tm_y)
        return TILE_MAPPING.get(tile_info, "GRASS")

    def can_move_to(self, grid_x: int, grid_y: int) -> bool:
        if grid_x < 0 or grid_x >= 12 or grid_y < 0 or grid_y >= 11:
            return False
        if (self.current_map_id, grid_x, grid_y) in MAP_EVENTS:
            return False

        tile_type = self.get_tile_type(grid_x, grid_y)
        return tile_type not in ["MOUNTAIN", "WALL"]

    def show_message(self, messages: list[str], return_mode: Mode = Mode.EXPLORE):
        """メッセージを表示して完了後に指定モードへ遷移する汎用メソッド"""
        self.msg_box.push_messages(messages)
        self.return_mode = return_mode
        self.mode = Mode.MESSAGE

    # --- メインループ (update / draw) ---

    def update(self):
        handler = self._update_handlers.get(self.mode)
        if handler:
            handler()

    def draw(self):
        pyxel.cls(0)

        # 1. マップ & プレイヤー描画
        cfg = MAP_CONFIG[self.current_map_id]
        pyxel.bltm(0, 16, 0, cfg["u"], cfg["v"], 192, 176)
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
        # draw_window(0, 0, 192, 16)
        # p = self.app.player
        # pyxel.text(
        #     6, 4, f"HERO LV:{p.level} HP:{p.hp}/{p.max_hp} G:{p.gold}", 7, self.app.font
        # )

        # 3. 各モード別UIの描画（Dispatcher）
        handler = self._draw_handlers.get(self.mode)
        if handler:
            handler()

    # --- モード別 Update ハンドラー群 ---

    def _update_explore(self):
        dx, dy = 0, 0
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            dy, self.direction = -1, Direction.UP
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            dy, self.direction = 1, Direction.DOWN
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            dx, self.direction = -1, Direction.LEFT
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            dx, self.direction = 1, Direction.RIGHT

        if dx != 0 or dy != 0:
            next_x, next_y = self.player_x + dx, self.player_y + dy
            if self.can_move_to(next_x, next_y):
                self.player_x, self.player_y = next_x, next_y

                # ワープ判定
                warp_key = (self.current_map_id, self.player_x, self.player_y)
                if warp_key in WARP_POINTS:
                    warp = WARP_POINTS[warp_key]
                    self.current_map_id, self.player_x, self.player_y = (
                        warp["target_map"],
                        warp["target_x"],
                        warp["target_y"],
                    )
                    if "message" in warp:
                        self.show_message([warp["message"]])
                    return

                # エンカウント判定
                cfg = MAP_CONFIG[self.current_map_id]
                if (
                    self.get_tile_type(self.player_x, self.player_y) == "GRASS"
                    and random.random() < cfg["encount_rate"]
                ):
                    self.trigger_battle()

        if is_confirm():
            self.interact()
        elif is_cancel():
            self.mode = Mode.MAIN_MENU
            self.cursor = 0

    def interact(self):
        target_pos = self.get_facing_pos()
        event_key = (self.current_map_id, target_pos[0], target_pos[1])
        event = MAP_EVENTS.get(event_key)
        if not event:
            return

        self.current_event = event

        match event["type"]:
            case "NPC":
                self.show_message(event["messages"])
            case "CHEST":
                if event["is_opened"]:
                    self.show_message(["たからばこ は からっぽ だ。"])
                else:
                    event["is_opened"] = True
                    if event["reward_type"] == "gold":
                        self.app.player.gold += event["reward_value"]
                        self.show_message(
                            [
                                "たからばこ を あけた！",
                                f"{event['reward_value']} ゴールド を てにいれた！",
                            ]
                        )
                    elif event["reward_type"] == "item":
                        self.app.player.items.append(event["reward_value"])
                        self.show_message(
                            [
                                "たからばこ を あけた！",
                                f"{event['reward_value']} を てにいれた！",
                            ]
                        )
            case "INN":
                self.sub_cursor = 0
                self.mode = Mode.INN_CONFIRM
            case "SHOP":
                self.sub_cursor = 0
                greeting = event.get(
                    "greeting", "いらっしゃいませ！\nなにに しますか？"
                )
                self.show_message([greeting], return_mode=Mode.SHOP_MAIN_MENU)
            case "BOSS":
                self.pending_boss_id = event["monster_id"]
                self.show_message(event["messages"], return_mode=Mode.START_BOSS_BATTLE)

    def _update_main_menu(self):
        self.cursor = navigate_menu(3, self.cursor)
        if is_cancel():
            self.mode = Mode.EXPLORE
        elif is_confirm():
            p = self.app.player
            match self.cursor:
                case 0:  # じゅもん
                    if not p.spells:
                        self.show_message(
                            ["じゅもんを おぼえていない！"], return_mode=Mode.MAIN_MENU
                        )
                    else:
                        self.mode = Mode.SPELL_MENU
                        self.sub_cursor = 0
                case 1:  # つよさ
                    self.mode = Mode.STATS_MENU
                case 2:  # どうぐ
                    if not p.items:
                        self.show_message(
                            ["どうぐを もっていない！"], return_mode=Mode.MAIN_MENU
                        )
                    else:
                        self.mode = Mode.ITEM_MENU
                        self.sub_cursor = 0

    def _update_spell_menu(self):
        p = self.app.player
        if is_cancel():
            self.mode = Mode.MAIN_MENU
        else:
            self.sub_cursor = navigate_menu(len(p.spells), self.sub_cursor)
            if is_confirm() and p.spells:
                spell = p.spells[self.sub_cursor]
                if spell.heal_amount > 0:
                    if p.mp < spell.mp_cost:
                        self.show_message(
                            ["MPが たりない！"], return_mode=Mode.SPELL_MENU
                        )
                    else:
                        p.mp -= spell.mp_cost
                        healed = p.heal(spell.heal_amount)
                        self.show_message(
                            [
                                f"{p.name} は {spell.name} を となえた！",
                                f"HPが {healed} かいふくした！",
                            ],
                            return_mode=Mode.EXPLORE,
                        )

    def _update_item_menu(self):
        p = self.app.player
        if is_cancel():
            self.mode = Mode.MAIN_MENU
        else:
            self.sub_cursor = navigate_menu(len(p.items), self.sub_cursor)
            if is_confirm() and p.items:
                item = p.items.pop(self.sub_cursor)
                if item in ["herb"]:
                    healed = p.heal(15)
                    self.show_message(
                        [
                            f"{p.name} は やくそうを つかった！",
                            f"HPが {healed} かいふくした！",
                        ],
                        return_mode=Mode.EXPLORE,
                    )

    def _update_stats_menu(self):
        if is_confirm() or is_cancel():
            self.mode = Mode.MAIN_MENU

    def _update_inn_confirm(self):
        if not self.current_event:
            self.mode = Mode.EXPLORE
            return

        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
            self.sub_cursor = 1 - self.sub_cursor

        if is_cancel():
            self.mode = Mode.EXPLORE
        elif is_confirm():
            p = self.app.player
            if self.sub_cursor == 0:  # はい
                p.hp, p.mp = p.max_hp, p.max_mp
                self.show_message(["よく ねむれたかい？", "いってらっしゃい！"])
            else:  # いいえ
                self.show_message(["むりしないでね"])

    def _update_shop_main_menu(self):
        self.sub_cursor = navigate_menu(2, self.sub_cursor)
        if is_cancel():
            self.show_message(["また おこしください！"])
        elif is_confirm():
            if self.sub_cursor == 0:  # かう
                self.shop_cursor = 0
                self.mode = Mode.SHOP_BUY_MENU
            else:  # うる
                p = self.app.player
                if not p.items:
                    self.show_message(
                        ["うれる どうぐを もっていない！"],
                        return_mode=Mode.SHOP_MAIN_MENU,
                    )
                else:
                    self.shop_cursor = 0
                    self.mode = Mode.SHOP_SELL_MENU

    def _update_shop_buy_menu(self):
        if not self.current_event:
            self.mode = Mode.EXPLORE
            return

        items = self.current_event["items"]
        if is_cancel():
            self.mode = Mode.SHOP_MAIN_MENU
        else:
            self.sub_cursor = navigate_menu(len(items), self.sub_cursor)
            if is_confirm():
                p = self.app.player
                item = items[self.sub_cursor]
                if p.gold < item["price"]:
                    self.show_message(
                        ["ゴールド が たりないようです。"],
                        return_mode=Mode.SHOP_BUY_MENU,
                    )
                else:
                    p.gold -= item["price"]
                    match item["type"]:
                        case "ITEM":
                            p.items.append(item["id"])
                            msg = f"{item['name']} を かった！"
                        case "WEAPON":
                            p.equip_weapon(item["name"], item["atk"])
                            msg = f"{item['name']} を そうびした！"
                        case "ARMOR":
                            p.equip_armor(item["name"], item["def"])
                            msg = f"{item['name']} を そうびした！"

                    self.show_message(
                        [msg, "まいど ありがとうございます！"],
                        return_mode=Mode.SHOP_BUY_MENU,
                    )

    def _update_shop_sell_menu(self):
        p = self.app.player
        if not p.items or is_cancel():
            self.mode = Mode.SHOP_MAIN_MENU
            return

        self.shop_cursor = navigate_menu(len(p.items), self.shop_cursor)
        if is_confirm():
            item_id = p.items.pop(self.shop_cursor)
            item_name = "やくそう" if item_id == "herb" else item_id
            sell_price = 5 if item_id == "herb" else 10
            p.gold += sell_price

            next_mode = Mode.SHOP_SELL_MENU if p.items else Mode.SHOP_MAIN_MENU
            self.show_message(
                [
                    f"{item_name} を {sell_price}G で うった！",
                    "ありがとう ございました！",
                ],
                return_mode=next_mode,
            )

    def _update_message(self):
        if self.msg_box.update():
            if self.return_mode == Mode.START_BOSS_BATTLE:
                monster = self.app.repo.create_monster(self.pending_boss_id)
                from .battle_scene import BattleScene

                self.app.change_state(BattleScene(self.app, monster))
            else:
                self.mode = self.return_mode

    def trigger_battle(self):
        from .battle_scene import BattleScene

        monster_id = random.choice(["entenstr", "rarutaes"])
        monster = self.app.repo.create_monster(monster_id)
        self.app.change_state(BattleScene(self.app, monster))

    # --- モード別 Draw ハンドラー群 ---

    def _draw_menu_overlay(self):
        p = self.app.player
        # 左側メインメニュー描画
        draw_menu_window(
            10, 24, 56, 44, ["じゅもん", "つよさ", "どうぐ"], self.cursor, self.app.font
        )

        # 右側サブメニューの重ね描き
        match self.mode:
            case Mode.SPELL_MENU:
                spell_texts = [f"{s.name} M:{s.mp_cost}" for s in p.spells]
                draw_menu_window(
                    70, 24, 110, 44, spell_texts, self.sub_cursor, self.app.font
                )
            case Mode.ITEM_MENU:
                item_texts = [
                    "やくそう" if item == "herb" else item for item in p.items
                ]
                draw_menu_window(
                    70, 24, 110, 44, item_texts, self.sub_cursor, self.app.font
                )
            case Mode.STATS_MENU:
                draw_window(70, 24, 110, 85)
                stats = [
                    f"なに: {p.name}",
                    f"レベル: {p.level}",
                    f"こうげき: {p.attack}",
                    f"まもり: {p.defense}",
                    f"ぶき: {p.equipped_weapon}",
                    f"よろい: {p.equipped_armor}",
                    f"けいけん: {p.exp}",
                    f"ゴールド: {p.gold}",
                ]
                for i, text in enumerate(stats):
                    pyxel.text(76, 30 + i * 10, text, 7, self.app.font)

    def _draw_inn_confirm(self):
        if not self.current_event:
            return
        draw_window(10, 130, 172, 48)
        pyxel.text(
            18, 138, "おかあさん「おかえりなさい やすんでいくかい？」", 7, self.app.font
        )
        yes_col = 10 if self.sub_cursor == 0 else 7
        no_col = 10 if self.sub_cursor == 1 else 7
        pyxel.text(50, 156, "はい", yes_col, self.app.font)
        pyxel.text(110, 156, "いいえ", no_col, self.app.font)

    def _draw_shop_main_menu(self):
        self.msg_box.draw()
        draw_menu_window(
            10, 45, 60, 42, ["かう", "うる"], self.sub_cursor, self.app.font
        )

    def _draw_shop_buy_menu(self):
        if not self.current_event:
            return
        p = self.app.player
        draw_window(10, 24, 172, 22)
        pyxel.text(18, 31, f"しょじきん: {p.gold}G", 7, self.app.font)

        items_texts = [
            f"{item['name']} ({item['price']}G)" for item in self.current_event["items"]
        ]
        draw_menu_window(10, 50, 172, 70, items_texts, self.sub_cursor, self.app.font)

    def _draw_shop_sell_menu(self):
        p = self.app.player
        draw_window(10, 24, 172, 22)
        pyxel.text(18, 31, f"しょじきん: {p.gold}G", 7, self.app.font)

        item_texts = [
            f"{('やくそう' if i == 'herb' else i)} (うる: {5 if i == 'herb' else 10}G)"
            for i in p.items
        ]
        draw_menu_window(10, 50, 172, 70, item_texts, self.shop_cursor, self.app.font)
