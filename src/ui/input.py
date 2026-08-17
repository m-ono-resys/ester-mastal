import pyxel


def is_confirm() -> bool:
    """決定キー判定 (Z / SPACE / RETURN)"""
    return (
        pyxel.btnp(pyxel.KEY_Z)
        or pyxel.btnp(pyxel.KEY_SPACE)
        or pyxel.btnp(pyxel.KEY_RETURN)
    )


def is_cancel() -> bool:
    """キャンセルキー判定 (X / ESCAPE)"""
    return pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE)


def navigate_menu(length: int, current_idx: int) -> int:
    """上下キーによるメニュー選択カーソル移動"""
    if length <= 0:
        return 0
    if pyxel.btnp(pyxel.KEY_UP):
        return (current_idx - 1) % length
    elif pyxel.btnp(pyxel.KEY_DOWN):
        return (current_idx + 1) % length
    return current_idx
