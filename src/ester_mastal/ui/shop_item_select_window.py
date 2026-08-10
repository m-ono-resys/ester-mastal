import math

from ..models.item import ItemCode, ItemRepository
from .base_window import BaseWindow


class ShopItemSelectWindow(BaseWindow):
    def __init__(
        self,
        app,
        x: int,
        y: int,
        width: int,
        choices: list[ItemCode],
        item_repository: ItemRepository,
        sell_flag: bool = False,
        line_height: int = 12,
        padding_x: int = 14,
        padding_y: int = 6,
    ):
        height = (padding_y * 2) + (len(choices) * line_height) - (line_height - 11)
        super().__init__(app, x, y, width, height)

        self.choices = choices
        self.item_repository = item_repository
        self.sell_flag = sell_flag
        self.line_height = line_height
        self.padding_x = padding_x
        self.padding_y = padding_y

        self._selected_idx: int = 0
        # ★ 選択結果を保持するプロパティ（未選択は None）
        self.result: ItemCode | None = None

    def handle_input(self, window_manager):
        if not self.choices or self.result is not None:
            return

        # 上下キー移動
        self._selected_idx = self.navigate_menu(len(self.choices), self._selected_idx)

        # 決定キー処理
        if self.is_confirm():
            self.result = self.choices[self._selected_idx]
            # window_manager.pop()  # 選択完了したら自身を閉じる

        # キャンセルキー処理
        elif self.is_cancel():
            self.result = None
            window_manager.pop()

    def update_window(self):
        pass

    def draw_content(self):
        # ラベルの描画
        for i, choice in enumerate(self.choices):
            item = self.item_repository.find_by_code(choice)
            item_name = item.name
            item_price = math.ceil(item.price / 2) if self.sell_flag else item.price
            self.draw_text(
                self.padding_x,
                self.padding_y + i * self.line_height,
                f"{item_name} ({item_price}G)",
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
