import pyxel

from ester_mastal.audio import init_audio
from ester_mastal.models.repository import GameRepository
from ester_mastal.states.base_scene import BaseScene
from ester_mastal.states.title_scene import TitleScene


class App:
    def __init__(self):
        # 画面サイズ: 192x192ピクセル（レトロ感のある低解像度）
        pyxel.init(192, 192, title="DQ1-Like RPG", fps=30)
        init_audio()

        pyxel.load("./assets/game.pyxres")

        self.font = pyxel.Font("./assets/font/PixelMplus10-Regular.ttf", 10)

        # リポジトリとグローバル状態の保持
        self.repo = GameRepository()
        self.player = None

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


if __name__ == "__main__":
    App()
