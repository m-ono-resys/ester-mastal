from ester_mastal.ui.base_window import BaseWindow


class HudStatusWindow(BaseWindow):
    def __init__(
        self,
        app,
        x,
        y,
        width,
        height,
    ):
        super().__init__(app, x, y, width, height)

    def update_window(self):
        pass

    def draw_content(self):
        p = self.app.player
        self.draw_text(
            5,
            3,
            f"{p.name} LV:{p.level} HP:{p.hp}/{p.max_hp} MP:{p.mp}/{p.max_mp} G:{p.gold}",
        )
