# title: エスターマスタル
# author: おの まさたか と パパ


import pyxel

from audio import init_audio
from data.events import EventFlag
from models.repository import GameRepository
from scenes.base_scene import BaseScene
from scenes.title_scene import TitleScene


class App:
    def __init__(self):
        # 画面サイズ: 192x192ピクセル（レトロ感のある低解像度）
        pyxel.init(192, 192, title="エスターマスタル", fps=30)
        init_audio()

        pyxel.load("./assets/game.pyxres")

        self.font = pyxel.Font("./assets/font/PixelMplus10-Regular.ttf", 10)

        # リポジトリとグローバル状態の保持
        self.repo = GameRepository()
        self.player = self.repo.create_initial_player("といろ")
        self.flags: set[EventFlag] = set()
        self.flags.add(EventFlag.GOT_ORB)

        # 初期状態はタイトル画面
        self.current_scene: BaseScene = TitleScene(self)

        # Pyxel実行開始
        pyxel.run(self.update, self.draw)

    def change_state(self, new_state):
        """ステートの切り替え"""
        self.current_scene = new_state

    def update(self):
        """現在のステートのupdateを呼ぶだけ"""
        self.current_scene.update()

    def draw(self):
        """現在のステートのdrawを呼ぶだけ"""
        self.current_scene.draw()
        pyxel.blt(1, 176, 0, 32, 0, 16, 16, 8)
        pyxel.text(18, 179, "いどう", 7, self.font)
        pyxel.blt(50, 176, 0, 48, 0, 16, 16, 8)
        pyxel.text(67, 179, "きめる", 7, self.font)
        pyxel.blt(99, 176, 0, 64, 0, 16, 16, 8)
        pyxel.text(117, 179, "やめる/メニュー", 7, self.font)


if __name__ == "__main__":
    App()
