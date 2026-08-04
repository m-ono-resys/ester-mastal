import pyxel
from ui.window import draw_window

class MessageBox:
    def __init__(self, x: int, y: int, width: int, height: int, speed: int = 2, font=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed  # 1文字表示にかかるフレーム数（小さいほど早い）
        self.font = font

        self.queue = []
        self.current_text = ""
        self.visible_char_count = 0
        self.frame_timer = 0
        self.is_waiting_input = False
        self.is_completed = True

    def push_messages(self, messages: list[str]):
        """メッセージリストをキューに追加"""
        self.queue.extend(messages)
        if self.is_completed and self.queue:
            self._next_message()

    def _next_message(self):
        """次のメッセージへ進む"""
        if self.queue:
            self.current_text = self.queue.pop(0)
            self.visible_char_count = 0
            self.frame_timer = 0
            self.is_waiting_input = False
            self.is_completed = False
        else:
            self.current_text = ""
            self.is_completed = True
            self.is_waiting_input = False

    def update(self) -> bool:
        """
        毎フレーム呼び出す。
        メッセージが完全に消化し終わった場合は True を返す。
        """
        if self.is_completed:
            return True

        # 文字がまだ表示しきっていない場合（タイプライター進行中）
        if self.visible_char_count < len(self.current_text):
            self.frame_timer += 1
            if self.frame_timer >= self.speed:
                self.frame_timer = 0
                self.visible_char_count += 1

            # 決定キーで「一括表示（早送り）」
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.visible_char_count = len(self.current_text)
                
        # 全文字表示完了 ➔ 入力待ちモードへ
        else:
            self.is_waiting_input = True
            # 決定キーで「次のメッセージへ」
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self._next_message()

        return False

    def draw(self):
        """ウィンドウと文字を描画"""
        if self.is_completed and not self.current_text:
            return

        # ウィンドウ描画
        draw_window(self.x, self.y, self.width, self.height)

        # 表示中の部分文字列を抽出
        text_to_show = self.current_text[:self.visible_char_count]
        
        # テキスト描画（font指定があれば使用）
        if self.font:
            pyxel.text(self.x + 8, self.y + 8, text_to_show, 7, self.font)
        else:
            pyxel.text(self.x + 8, self.y + 8, text_to_show, 7)

        # 入力待ちカーソル「▼」の点滅表示（20フレーム周期）
        if self.is_waiting_input and (pyxel.frame_count // 10) % 2 == 0:
            cursor_x = self.x + self.width - 15
            cursor_y = self.y + self.height - 12
            if self.font:
                pyxel.text(cursor_x, cursor_y, "▼", 7, self.font)
            else:
                pyxel.text(cursor_x, cursor_y, "v", 7)