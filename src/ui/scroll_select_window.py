from enum import Enum

import pyxel

from .enum_select_window import EnumSelectWindow


class ScrollSelectWindow[T: Enum](EnumSelectWindow[T]):
    """
    最大表示件数（デフォルト4件）に制限し、上下スクロールと ▲ / ▼ インジケーター表示に対応した選択ウィンドウ
    """

    def __init__(
        self,
        app,
        choices: list[T],
        x: int = 95,
        y: int = 115,
        width: int = 87,
        max_visible: int = 4,  # ★ 最大表示件数（デフォルト4件）
        line_height: int = 12,
        padding_x: int = 14,
        padding_y: int = 6,
    ):
        self.max_visible = max_visible
        self._scroll_top: int = 0  # ★ 現在表示されている最上部のインデックス

        # 表示件数が max_visible を超える場合は、max_visible 分の高さで固定計算する
        visible_count = min(len(choices), max_visible) if choices else 1
        height = (padding_y * 2) + (visible_count * line_height) - (line_height - 11)

        super().__init__(app, x, y, width, choices, line_height, padding_x, padding_y)
        # 高さを計算した値に更新
        self.height = height

    def handle_input(self, window_manager):
        super().handle_input(window_manager)

        # ★ カーソル位置に合わせてスクロール位置（_scroll_top）を自動追従補正
        if self._selected_idx < self._scroll_top:
            # カーソルが画面上端より上に行った場合 ➔ スクロールアップ
            self._scroll_top = self._selected_idx
        elif self._selected_idx >= self._scroll_top + self.max_visible:
            # カーソルが画面下端を超えた場合 ➔ スクロールダウン
            self._scroll_top = self._selected_idx - self.max_visible + 1

    def draw_content(self):
        # ★ 画面内に収まる範囲（_scroll_top から max_visible 件分）の選択肢だけを切り出す
        visible_choices = self.choices[
            self._scroll_top : self._scroll_top + self.max_visible
        ]

        # 1. 選択肢ラベルの描画
        for i, choice in enumerate(visible_choices):
            label = self._get_item_label(choice)
            self.draw_text(
                self.padding_x,
                self.padding_y + i * self.line_height,
                label,
                7,
            )

        # 2. カーソル (>) の描画（画面表示範囲内の相対位置に表示）
        relative_idx = self._selected_idx - self._scroll_top
        if 0 <= relative_idx < len(visible_choices):
            self.draw_text(
                self.padding_x - 8,
                self.padding_y + relative_idx * self.line_height,
                ">",
                10,
            )

        # 3. ★ 上下にまだ選択肢があることを示すインジケーター（▲ / ▼）の点滅描画
        if (pyxel.frame_count // 10) % 2 == 0:
            # 上にまだ隠れているアイテムがある場合
            if self._scroll_top > 0:
                self.draw_text(self.width - 14, self.padding_y, "▲", 7)

            # 下にまだ隠れているアイテムがある場合
            if self._scroll_top + self.max_visible < len(self.choices):
                self.draw_text(
                    self.width - 14,
                    self.height - self.padding_y - 10,
                    "▼",
                    7,
                )
