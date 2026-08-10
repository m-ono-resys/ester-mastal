from __future__ import annotations

from typing import TYPE_CHECKING

import pyxel

from .base_window import BaseWindow

if TYPE_CHECKING:
    from .window_manager import WindowManager


class MessageWindow(BaseWindow):
    def __init__(
        self,
        app,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: list[str] | None = None,  # 初期メッセージを直接受け取れるように拡張
        speed: int = 2,
        max_chars_per_line: int = 18,
        max_lines_per_page: int = 2,
    ):
        super().__init__(app, x, y, width, height)
        self.speed = speed
        self.max_chars_per_line = max_chars_per_line
        self.max_lines_per_page = max_lines_per_page

        self.queue: list[str] = []
        self.current_text = ""
        self.visible_char_count = 0
        self.frame_timer = 0
        self.is_waiting_input = False
        self.is_completed = True

        # 初期メッセージが指定されている場合は即座にキューに追加
        if messages:
            self.push_messages(messages)

    def _split_into_pages(self, text: str) -> list[str]:
        """長文を1行18文字・1ページ2行に自動分割する関数"""
        lines = []
        for raw_line in text.split("\n"):
            if not raw_line:
                lines.append("")
                continue
            for i in range(0, len(raw_line), self.max_chars_per_line):
                lines.append(raw_line[i : i + self.max_chars_per_line])

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

    def handle_input(self, window_manager: WindowManager):
        """入力処理とタイマーアニメーション更新（WindowManager.update から呼ばれる）"""
        # ★ 1. キーを押していなくても文字送りアニメーションを毎フレーム進行させる
        self.update_window()

        if self.is_completed:
            return

        # 2. 決定キーが押された時の処理
        if self.is_confirm():
            # 文字送り中の場合は「一括全表示（早送り）」
            if self.visible_char_count < len(self.current_text):
                self.visible_char_count = len(self.current_text)
                self.is_waiting_input = True

            # 入力待ち中の場合は「次のページへ」
            elif self.is_waiting_input:
                self._next_message()
                # すべてのメッセージを表示し終えたらウィンドウを閉じる
                if self.is_completed:
                    window_manager.pop()

    def update_window(self):
        """タイマーによる1文字ずつの文字送り処理"""
        if self.is_completed:
            return

        # 文字列送りアニメーション
        if self.visible_char_count < len(self.current_text):
            self.frame_timer += 1
            if self.frame_timer >= self.speed:
                self.frame_timer = 0
                self.visible_char_count += 1
        else:
            self.is_waiting_input = True

    def draw_content(self):
        """ウィンドウ内部のメッセージと「▼」カーソルの描画"""
        if self.is_completed and not self.current_text:
            return

        # 現在の文字数までを切り出して改行 (\n) で分割
        visible_text = self.current_text[: self.visible_char_count]
        lines = visible_text.split("\n")

        line_spacing = 14  # 行間（ピクセル）
        padding_x = 8
        padding_y = 8

        # 描画（self.draw_text が相対座標とフォント指定を自動処理してくれる）
        for i, line in enumerate(lines):
            line_y = padding_y + (i * line_spacing)
            self.draw_text(padding_x, line_y, line, 7)

        # 次ページへ促す「▼」カーソルの点滅描画
        if self.is_waiting_input and (pyxel.frame_count // 10) % 2 == 0:
            cursor_x = self.width - 14
            cursor_y = self.height - 12
            self.draw_text(cursor_x, cursor_y, "▼", 7)
