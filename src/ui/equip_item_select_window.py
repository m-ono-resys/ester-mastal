from collections.abc import Collection
from enum import Enum
from typing import Any

from .enum_select_window import EnumSelectWindow


class EquipItemSelectWindow[T: Enum](EnumSelectWindow[T]):
    def __init__(
        self,
        app,
        x: int,
        y: int,
        width: int,
        choices: list[T],
        equipped_items: Collection[Any] | None = None,  # ★ 装備中のアイテム集合
        line_height: int = 12,
        padding_x: int = 14,
        padding_y: int = 6,
    ):
        super().__init__(
            app, x, y, width, choices, line_height, padding_x, padding_y
        )
        # 高速検索用に set に変換して保持
        self.equipped_items: set[Any] = set(equipped_items) if equipped_items else set()

    def _get_item_label(self, choice: T) -> str:
        """★ 装備中であれば末尾に「 E」を付与して返す"""
        label = str(choice.value)
        if choice in self.equipped_items or choice.value in self.equipped_items:
            return f"{label} E"
        return label
