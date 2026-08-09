# controllers/event_runner.py
from collections.abc import Generator
from typing import Any
import pyxel


class EventRunner:
    """
    ジェネレータ（コルーチン）ベースのイベント＆スクリプト実行ランナー。
    yield / yield from による非同期進行と WindowManager を統合制御する。
    """

    def __init__(self, app, window_manager):
        self.app = app
        self.window_manager = window_manager
        self.active_script: Generator | None = None
        self._wait_frames: int = 0
        self._is_waiting_frame: bool = False

    @property
    def is_running(self) -> bool:
        """スクリプトが実行中またはウィンドウが開いているか"""
        return self.active_script is not None or self.window_manager.is_open

    def start_script(self, script_gen: Generator):
        """新しいコルーチンスクリプトを開始"""
        self.active_script = script_gen
        self._wait_frames = 0
        self._is_waiting_frame = False
        self.resume()  # 最初の yield まで実行を開始

    def resume(self):
        """コルーチンを 1 ステップ（次の yield）まで進行させる"""
        if not self.active_script:
            return

        try:
            # 次の yield まで処理を進めてアクションを取得
            action = next(self.active_script)
            self._handle_action(action)
        except StopIteration:
            # スクリプト（ジェネレータ）が最後まで到達したら終了
            self.active_script = None

    def update(self):
        """毎フレーム呼び出されるメイン更新処理"""
        if not self.active_script:
            return

        # 1. ウィンドウが開いている場合は最前面ウィンドウの入力・描画アニメーションを更新
        if self.window_manager.is_open:
            self.window_manager.update()

        # 2. 指定フレーム数のウェイト処理 (例: yield 30)
        if self._wait_frames > 0:
            self._wait_frames -= 1
            if self._wait_frames == 0:
                self.resume()
            return

        # 3. 1フレーム待機 (例: yield や wait_for_menu 内の yield)
        if self._is_waiting_frame:
            self._is_waiting_frame = False
            self.resume()

    def _handle_action(self, action: Any):
        """yield された内容（アクション）に応じた処理の割り振りを実行"""

        # --- A. 1フレーム待機 (yield) ---
        if action is None:
            self._is_waiting_frame = True
            return

        # --- B. メッセージ表示 (yield ["文章1", "文章2"]) ---
        if isinstance(action, list):
            from ester_mastal.ui.message_window import MessageWindow

            self._is_waiting_frame = False
            self.window_manager.push(
                MessageWindow(
                    self.app,
                    10,
                    130,
                    172,
                    50,
                    messages=action,
                    # ★ メッセージが閉じた瞬間に on_close から resume() を呼んでスクリプト再開！
                    on_close=self.resume,
                )
            )

        # --- C. 指定フレーム数の待機 (yield 30 で1秒待機) ---
        elif isinstance(action, int):
            self._is_waiting_frame = False
            self._wait_frames = action

        # --- D. 即時関数の実行 (yield lambda: start_battle()) ---
        elif callable(action):
            self._is_waiting_frame = False
            action()
            self.resume()

    def stop(self):
        """実行中のスクリプトおよびウィンドウを強制停止"""
        self.active_script = None
        self._wait_frames = 0
        self._is_waiting_frame = False
        self.window_manager.clear()