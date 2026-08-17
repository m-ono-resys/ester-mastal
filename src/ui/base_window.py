from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pyxel

from .input import is_cancel

if TYPE_CHECKING:
    from ..main import App
    from .window_manager import WindowManager


class BaseWindow(ABC):
    def __init__(
        self,
        app: App,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw_frame(self):
        pyxel.rect(
            self.x,
            self.y,
            self.width,
            self.height,
            0,
        )

        pyxel.rectb(
            self.x,
            self.y,
            self.width,
            self.height,
            7,
        )

        pyxel.rectb(
            self.x + 2,
            self.y + 2,
            self.width - 4,
            self.height - 4,
            7,
        )

    def draw_text(
        self,
        x: int,
        y: int,
        text: str,
        color: int = 7,
    ):
        pyxel.text(
            self.x + x,
            self.y + y,
            text,
            color,
            self.app.font,
        )

    def update(self):
        self.update_window()

    def draw(self):
        self.draw_frame()
        self.draw_content()

    def handle_input(self, window_manager: WindowManager):
        """キー入力処理のデフォルト実装（必要に応じて子クラスでオーバーライド）"""
        # 基本のキャンセルキー処理（Xキー）
        if is_cancel():
            window_manager.pop()

    # --- サブクラスで実装するメソッド ---
    @abstractmethod
    def update_window(self):
        """ウィンドウ固有の更新処理"""

    @abstractmethod
    def draw_content(self):
        """ウィンドウ内部コンテンツ（テキストやカーソル）の描画処理"""
