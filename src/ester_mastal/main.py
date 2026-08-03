import pyxel
from ester_mastal.models.repository import GameRepository
from ester_mastal.states.title_state import TitleState

class App:
    def __init__(self):
        # 画面サイズ: 160x120ピクセル（レトロ感のある低解像度）
        pyxel.init(160, 120, title="DQ1-Like RPG", fps=30)

        self.font = pyxel.Font("./assets/font/misaki_gothic.ttf", 8)
        
        # リポジトリとグローバル状態の保持
        self.repo = GameRepository()
        self.player = None
        
        # 初期状態はタイトル画面
        self.current_state = TitleState(self)

        # Pyxel実行開始
        pyxel.run(self.update, self.draw)

    def change_state(self, new_state):
        """ステートの切り替え"""
        self.current_state = new_state

    def update(self):
        """現在のステートのupdateを呼ぶだけ"""
        self.current_state.update()

    def draw(self):
        """現在のステートのdrawを呼ぶだけ"""
        self.current_state.draw()

if __name__ == "__main__":
    App()