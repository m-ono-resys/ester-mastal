from enum import Enum

import pyxel

from .input import is_confirm, navigate_menu
from .window import draw_window


class EnumMenu[T: Enum]:
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        choices: list[T],
        font,
        line_height: int = 11,
        padding_x: int = 14,
        padding_y: int = 8,
    ):
        self.x = x
        self.y = y
        self.w = w
        self.choices = choices
        self.font = font
        self.line_height = line_height
        self.padding_x = padding_x
        self.padding_y = padding_y

        # 呼び出し元で管理させない内部状態
        self._selected_idx: int = 0

        # 高さを自動計算して保持
        self.h = (padding_y * 2) + (len(choices) * line_height) - (line_height - 8)

    def update(self) -> T | None:
        """
        毎フレーム呼び出すキー入力監視メソッド。
        決定された瞬間だけ、そのEnumメンバーを返す（それ以外はNone）。
        """
        # 内部でメニュー移動を完結
        self._selected_idx = navigate_menu(len(self.choices), self._selected_idx)

        if is_confirm():
            return self.choices[self._selected_idx]  # 選択されたEnumメンバーを返す

        return None

    def draw(self) -> None:
        """ウィンドウの描画からテキスト、カーソルまで全てを閉じ込めた描画メソッド"""
        # ウィンドウ描画を内部で実行
        draw_window(self.x, self.y, self.w, self.h)

        # テキストの描画
        for i, choice in enumerate(self.choices):
            label = str(choice.value)
            pyxel.text(
                self.x + self.padding_x,
                self.y + self.padding_y + i * self.line_height,
                label,
                7,
                self.font,
            )

        # カーソルの描画
        if 0 <= self._selected_idx < len(self.choices):
            pyxel.text(
                self.x + self.padding_x - 8,
                self.y + self.padding_y + self._selected_idx * self.line_height,
                ">",
                10,
                self.font,
            )


# def draw_enum_menu[T: Enum](
#     x: int,
#     y: int,
#     w: int,
#     h: int,
#     choices: list[T],
#     selected_idx: int,
#     font,
#     line_height: int = 11,
#     padding_x: int = 14,
#     padding_y: int = 8,
# ):
#     """Enumのリストから .value (画面表示文字) を自動抽出してメニュー枠を描画"""
#     labels = [choice.value for choice in choices]

#     draw_window(x, y, w, h)
#     for i, label in enumerate(labels):
#         pyxel.text(x + padding_x, y + padding_y + i * line_height, label, 7, font)
#     if 0 <= selected_idx < len(choices):
#         pyxel.text(
#             x + padding_x - 8, y + padding_y + selected_idx * line_height, ">", 10, font
#         )


# def handle_enum_menu[T: Enum](choices: list[T], current_idx: int) -> T | None:
#     """
#     Enumリストからキー入力を判定し、選択されたEnumメンバーを返す関数
#     戻り値: (新しいカーソル位置, 選択されたEnum値 | None, キャンセルされたか)
#     """
#     new_idx = navigate_menu(len(choices), current_idx)

#     if is_confirm():
#         return choices[new_idx]  # 選択されたEnumメンバーを返す！

#     return None
