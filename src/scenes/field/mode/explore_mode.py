import random

import pyxel

from data.events import MAP_EVENTS, EventFlag
from data.maps import MAP_CONFIG, WARP_POINTS, FromPosition
from ui.input import is_cancel, is_confirm
from ui.message_window import MessageWindow

from .base_mode import BaseMode, FieldContext
from .main_menu_mode import MainMenuMode
from .signals import ModeSignal, PushSignal


class ExploreMode(BaseMode):
    def __init__(self, context: FieldContext):
        super().__init__(context)

        flags = self._app.flags

        # ★ 全滅復活フラグが立っている場合、復活メッセージを自動表示！
        if EventFlag.PLAYER_DIED in flags:
            flags.remove(EventFlag.PLAYER_DIED)  # 1回だけ表示するためにフラグ解除

            self._wm.push(
                MessageWindow(
                    self._app,
                    messages=[
                        "おかあさん「だいじょうぶかい？",
                        "いってらっしゃい。」",
                    ],
                )
            )

    def update(self) -> ModeSignal:

        # ★ ウィンドウが開いている（会話中・メッセージ表示中など）場合
        if self._wm.is_open:
            self._wm.update()  # 最前面の MessageWindow の文字送りや決定キー処理を実行
            return ModeSignal()  # 移動処理は行わずに終了

        dx, dy = 0, 0

        if (
            pyxel.btnp(pyxel.KEY_UP)
            or pyxel.btnp(pyxel.KEY_W)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)
        ):
            dy, self._scene.direction = -1, self._scene.direction.UP
        elif (
            pyxel.btnp(pyxel.KEY_DOWN)
            or pyxel.btnp(pyxel.KEY_S)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)
        ):
            dy, self._scene.direction = 1, self._scene.direction.DOWN
        elif (
            pyxel.btnp(pyxel.KEY_LEFT)
            or pyxel.btnp(pyxel.KEY_A)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
        ):
            dx, self._scene.direction = -1, self._scene.direction.LEFT
        elif (
            pyxel.btnp(pyxel.KEY_RIGHT)
            or pyxel.btnp(pyxel.KEY_D)
            or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
        ):
            dx, self._scene.direction = 1, self._scene.direction.RIGHT

        if dx != 0 or dy != 0:
            next_x, next_y = self._scene.player_x + dx, self._scene.player_y + dy
            if self._scene.can_move_to(next_x, next_y):
                self._scene.player_x, self._scene.player_y = next_x, next_y
                self._app.player.x, self._app.player.y = next_x, next_y

                # ワープ判定
                warp_key = FromPosition(
                    self._scene.current_map_id,
                    self._scene.player_x,
                    self._scene.player_y,
                )
                if warp_key in WARP_POINTS:
                    warp = WARP_POINTS[warp_key]
                    self._scene.current_map_id = warp.map_id
                    self._scene.player_x, self._scene.player_y = warp.x, warp.y
                    self._app.player.map_id = warp.map_id
                    self._app.player.x, self._app.player.y = warp.x, warp.y
                    if warp.message is not None:
                        message = MessageWindow(
                            app=self._app,
                            messages=[warp.message],
                        )
                        self._wm.push(message)
                    return ModeSignal()

                # エンカウント判定
                cfg = MAP_CONFIG[self._scene.current_map_id]
                if random.random() < cfg.encount_rate:
                    if cfg.monsters is not None:
                        monster_code = random.choice(cfg.monsters)
                        self._scene.trigger_battle_with_monster(monster_code)
                    return ModeSignal()

        if is_confirm():
            return self._interact()

        elif is_cancel():
            return PushSignal(MainMenuMode(self._context))

        return ModeSignal()

    def _interact(self) -> ModeSignal:
        target_pos = self._scene.get_facing_pos()
        event_key = FromPosition(
            self._scene.current_map_id, target_pos[0], target_pos[1]
        )
        event_entry = MAP_EVENTS.get(event_key)

        if not event_entry:
            return ModeSignal()

        strategy, event_data = event_entry
        self._scene.current_event = event_data

        return strategy.execute(self._context)

    def draw(self) -> None:
        pass
