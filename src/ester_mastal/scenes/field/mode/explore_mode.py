import random

import pyxel

from ....data.events import MAP_EVENTS
from ....data.maps import MAP_CONFIG, WARP_POINTS, FromPosition
from ....ui.message_window import MessageWindow
from .base_mode import BaseMode
from .inn_mode import InnMode
from .main_menu_mode import MainMenuMode
from .message_mode import MessageMode
from .shop_mode import ShopMode
from .signals import ModeSignal, PushSignal


class ExploreMode(BaseMode):
    def is_confirm(self) -> bool:
        """決定キー判定 (Z / SPACE / RETURN)"""
        return (
            pyxel.btnp(pyxel.KEY_Z)
            or pyxel.btnp(pyxel.KEY_SPACE)
            or pyxel.btnp(pyxel.KEY_RETURN)
        )

    def is_cancel(self) -> bool:
        """キャンセルキー判定 (X / ESCAPE)"""
        return pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE)

    def update(self) -> ModeSignal:
        scene = self.context.scene
        wm = scene.window_manager

        # ★ ウィンドウが開いている（会話中・メッセージ表示中など）場合
        if wm.is_open:
            wm.update()  # 最前面の MessageWindow の文字送りや決定キー処理を実行
            return ModeSignal()  # 移動処理は行わずに終了

        dx, dy = 0, 0

        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            dy, scene.direction = -1, scene.direction.UP
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            dy, scene.direction = 1, scene.direction.DOWN
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            dx, scene.direction = -1, scene.direction.LEFT
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            dx, scene.direction = 1, scene.direction.RIGHT

        if dx != 0 or dy != 0:
            next_x, next_y = scene.player_x + dx, scene.player_y + dy
            if scene.can_move_to(next_x, next_y):
                scene.player_x, scene.player_y = next_x, next_y

                # ワープ判定
                warp_key = FromPosition(
                    scene.current_map_id, scene.player_x, scene.player_y
                )
                if warp_key in WARP_POINTS:
                    warp = WARP_POINTS[warp_key]
                    scene.current_map_id = warp.map_id
                    scene.player_x, scene.player_y = warp.x, warp.y
                    if warp.message is not None:
                        message = MessageWindow(
                            app=scene.app,
                            x=10,
                            y=130,
                            width=172,
                            height=50,
                            speed=2,
                            messages=[warp.message],
                        )
                        scene.window_manager.push(message)
                    return ModeSignal()

                # エンカウント判定
                cfg = MAP_CONFIG[scene.current_map_id]
                if (
                    scene.get_tile_type(scene.player_x, scene.player_y) == "GRASS"
                    and random.random() < cfg.encount_rate
                ):
                    scene.trigger_battle()
                    return ModeSignal()

        if self.is_confirm():
            return self._interact()
            # pass

        elif self.is_cancel():
            return PushSignal(MainMenuMode(self.context))

        return ModeSignal()

    def _interact(self) -> ModeSignal:
        scene = self.context.scene
        target_pos = scene.get_facing_pos()
        event_key = (scene.current_map_id, target_pos[0], target_pos[1])
        event = MAP_EVENTS.get(event_key)

        if not event:
            return ModeSignal()

        scene.current_event = event

        match event["type"]:
            case "NPC":
                return PushSignal(MessageMode(self.context))

            #         case "CHEST":
            #             if event["is_opened"]:
            #                 return PushSignal(MessageMode(self.context, ["たからばこ は からっぽ だ。"]))
            #             else:
            #                 event["is_opened"] = True
            #                 p = self.context.app.player
            #                 if event["reward_type"] == "gold":
            #                     p.gold += event["reward_value"]
            #                     return PushSignal(MessageMode(self.context, ["たからばこ を あけた！", f"{event['reward_value']} ゴールド を てにいれた！"]))
            #                 elif event["reward_type"] == "item":
            #                     p.items.append(event["reward_value"])
            #                     return PushSignal(MessageMode(self.context, ["たからばこ を あけた！", f"{event['reward_value']} を てにいれた！"]))

            case "INN":
                return PushSignal(InnMode(self.context))

            case "SHOP":
                return PushSignal(ShopMode(self.context, event))

        #         case "BOSS":
        #             scene.pending_boss_id = event["monster_id"]
        #             return PushSignal(MessageMode(self.context, event["messages"], start_boss_battle=True))

        return ModeSignal()

    def draw(self) -> None:
        pass
