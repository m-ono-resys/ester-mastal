import pyxel

def draw_window(x: int, y: int, width: int, height: int, bg_col: int = 0, border_col: int = 7):
    """
    ドラクエ風の黒背景＋二重白枠ウィンドウを描画する
    """
    # 1. 外側の背景（黒）
    pyxel.rect(x, y, width, height, bg_col)
    
    # 2. 外枠（白）
    pyxel.rectb(x, y, width, height, border_col)
    
    # 3. 内側の線（1ピクセル内側に細い枠線を描くことでDQ風二重枠を再現）
    pyxel.rectb(x + 2, y + 2, width - 4, height - 4, border_col)