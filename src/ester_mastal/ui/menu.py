import pyxel

from .window import draw_window


def draw_menu_window(
    x: int,
    y: int,
    w: int,
    h: int,
    items: list[str],
    selected_idx: int,
    font,
    line_height: int = 11,
    padding_x: int = 14,
    padding_y: int = 8,
):
    """二重枠線付きのリスト選択メニュー描画関数"""
    draw_window(x, y, w, h)
    for i, item_text in enumerate(items):
        pyxel.text(x + padding_x, y + padding_y + i * line_height, item_text, 7, font)
    if 0 <= selected_idx < len(items):
        pyxel.text(
            x + padding_x - 8, y + padding_y + selected_idx * line_height, ">", 10, font
        )
