from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_window import BaseWindow


class WindowManager:
    def __init__(self):
        self._windows: list[BaseWindow] = []

    def push(self, window: BaseWindow):
        """新しいウィンドウを開いて最前面に追加する"""
        self._windows.append(window)

    def pop(self) -> BaseWindow | None:
        """最前面のウィンドウを閉じる（削除する）"""
        if self._windows:
            return self._windows.pop()
        return None

    def clear(self):
        """すべてのウィンドウを閉じる"""
        self._windows.clear()

    @property
    def current(self) -> BaseWindow | None:
        """現在アクティブ（最前面）なウィンドウを取得"""
        if self._windows:
            return self._windows[-1]
        return None

    @property
    def is_open(self) -> bool:
        """表示中のウィンドウが存在するかどうか"""
        return len(self._windows) > 0

    def update(self):
        """最前面のウィンドウのみ update を呼ぶ（フォーカス制御）"""
        if self.current:
            self.current.handle_input(self)

    def draw(self):
        """画面奥（リストの先頭）から順番に描画する"""
        for window in self._windows:
            window.draw()
