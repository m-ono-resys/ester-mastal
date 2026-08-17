from enum import Enum

from .base_window import BaseWindow
from .input import is_cancel, is_confirm, navigate_menu


class EnumSelectWindow[T: Enum](BaseWindow):
    def __init__(
        self,
        app,
        x: int,
        y: int,
        width: int,
        choices: list[T],
        line_height: int = 12,
        padding_x: int = 14,
        padding_y: int = 6,
    ):
        height = (padding_y * 2) + (len(choices) * line_height) - (line_height - 11)
        super().__init__(app, x, y, width, height)

        self.choices = choices
        self.line_height = line_height
        self.padding_x = padding_x
        self.padding_y = padding_y

        self._selected_idx: int = 0
        # ★ 選択結果を保持するプロパティ（未選択は None）
        self.result: T | None = None

    def handle_input(self, window_manager):
        if not self.choices or self.result is not None:
            return

        # 上下キー移動
        self._selected_idx = navigate_menu(len(self.choices), self._selected_idx)

        # 決定キー処理
        if is_confirm():
            self.result = self.choices[self._selected_idx]
            # window_manager.pop()  # 選択完了したら自身を閉じる

        # キャンセルキー処理
        elif is_cancel():
            self.result = None
            window_manager.pop()

    def update_window(self):
        pass

    def _get_item_label(self, choice: T) -> str:
        """★ アイテムテキストを取得するフックメソッド（子クラスでオーバーライド用）"""
        return str(choice.value)

    def draw_content(self):
        # ラベルの描画
        for i, choice in enumerate(self.choices):
            label = self._get_item_label(choice)  # ★ 呼び出し
            self.draw_text(
                self.padding_x,
                self.padding_y + i * self.line_height,
                label,
                7,
            )

        # カーソル (>) の描画
        if 0 <= self._selected_idx < len(self.choices):
            self.draw_text(
                self.padding_x - 8,
                self.padding_y + self._selected_idx * self.line_height,
                ">",
                10,
            )


def wait_for_menu[T: Enum](window_manager, select_window: EnumSelectWindow[T]):
    """
    メニューを開き、選択されるまで毎フレーム yield して待機する。
    選択されたら Enum メンバー（キャンセル時は None）を返す。
    """
    window_manager.push(select_window)

    # 選択結果がセットされる（またはウィンドウが閉じられる）までフレームを進める
    while select_window.result is None and window_manager.is_open:
        yield  # 1フレーム待機

    if window_manager.current == select_window:
        window_manager.pop()

    return select_window.result
