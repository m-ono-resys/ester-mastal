from ui.base_window import BaseWindow


class BattleStatusWindow(BaseWindow):
    def __init__(
        self,
        app,
        x=10,
        y=120,
        width=80,
        height=59,
    ):
        super().__init__(app, x, y, width, height)

    def update_window(self):
        pass

    def draw_content(self):
        p = self.app.player
        stats = [
            f"{p.name}",
            f"HP: {p.hp}/{p.max_hp}",
            f"MP: {p.mp}/{p.max_mp}",
            f"LV:{p.level}",
            # f"けいけん: {p.exp}",
            # f"ゴールド: {p.gold}",
        ]
        for i, text in enumerate(stats):
            self.draw_text(
                6,
                6 + i * 12,
                text,
            )
