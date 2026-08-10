from ester_mastal.ui.base_window import BaseWindow


class StatusWindow(BaseWindow):
    def __init__(
        self,
        app,
        x=75,
        y=24,
        width=110,
        height=104,
    ):
        super().__init__(app, x, y, width, height)

    def update_window(self):
        pass

    def draw_content(self):
        p = self.app.player
        stats = [
            f"なまえ: {p.name}",
            f"レベル: {p.level}",
            f"こうげき: {p.attack}",
            f"まもり: {p.defense}",
            f"ぶき: {getattr(p.equipped_weapon, 'name', 'なし')}",
            f"よろい: {getattr(p.equipped_armor, 'name', 'なし')}",
            f"けいけん: {p.exp}",
            f"ゴールド: {p.gold}",
        ]
        for i, text in enumerate(stats):
            self.draw_text(
                5,
                5 + i * 12,
                text,
            )
