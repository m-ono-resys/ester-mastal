import pyxel
from .window import draw_window

class MessageBox:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        speed: int = 2,
        font=None,
        max_chars_per_line: int = 18,  # 1行あたりの最大文字数
        max_lines_per_page: int = 2    # 1ページあたりの最大行数（ドラクエは2行）
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.font = font
        self.max_chars_per_line = max_chars_per_line
        self.max_lines_per_page = max_lines_per_page

        self.queue: list[str] = []
        self.current_text = ""
        self.visible_char_count = 0
        self.frame_timer = 0
        self.is_waiting_input = False
        self.is_completed = True

    def _split_into_pages(self, text: str) -> list[str]:
        """長文を1行16文字・1ページ2行に自動分割する関数"""
        lines = []
        # \n による手動改行を考慮
        for raw_line in text.split("\n"):
            if not raw_line:
                lines.append("")
                continue
            # 指定文字数ごとに折り返し
            for i in range(0, len(raw_line), self.max_chars_per_line):
                lines.append(raw_line[i : i + self.max_chars_per_line])

        # 指定行数（2行）ごとにページとして結合
        pages = []
        for i in range(0, len(lines), self.max_lines_per_page):
            page_lines = lines[i : i + self.max_lines_per_page]
            pages.append("\n".join(page_lines))

        return pages

    def push_messages(self, messages: list[str]):
        """メッセージを追加（自動的に長文はページ分割される）"""
        for msg in messages:
            pages = self._split_into_pages(msg)
            self.queue.extend(pages)

        if self.is_completed and self.queue:
            self._next_message()

    def _next_message(self):
        """次のページを表示"""
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
        """メッセージ進行処理。全ページ表示完了したら True を返す"""
        if self.is_completed:
            return True

        # 文字列送り中
        if self.visible_char_count < len(self.current_text):
            self.frame_timer += 1
            if self.frame_timer >= self.speed:
                self.frame_timer = 0
                self.visible_char_count += 1

            # 決定キーで「現在ページの早送り（一括表示）」
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self.visible_char_count = len(self.current_text)

        # 1ページ分表示完了 ➔ 入力待ち
        else:
            self.is_waiting_input = True
            # 決定キーで「次のページへ」
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
                self._next_message()

        return False

    def draw(self):
        if self.is_completed and not self.current_text:
            return

        # ウィンドウ背景の描画
        draw_window(self.x, self.y, self.width, self.height)

        # 現在の文字数までを切り出して改行 (\n) で分割描画
        visible_text = self.current_text[: self.visible_char_count]
        lines = visible_text.split("\n")

        line_spacing = 14  # 行間（ピクセル）
        start_padding_x = 8
        start_padding_y = 8

        for i, line in enumerate(lines):
            line_y = self.y + start_padding_y + (i * line_spacing)
            if self.font:
                pyxel.text(self.x + start_padding_x, line_y, line, 7, self.font)
            else:
                pyxel.text(self.x + start_padding_x, line_y, line, 7)

        # 次ページへ促す「▼」カーソルの点滅描画
        if self.is_waiting_input and (pyxel.frame_count // 10) % 2 == 0:
            cursor_x = self.x + self.width - 14
            cursor_y = self.y + self.height - 12
            if self.font:
                pyxel.text(cursor_x, cursor_y, "▼", 7, self.font)
            else:
                pyxel.text(cursor_x, cursor_y, "v", 7)