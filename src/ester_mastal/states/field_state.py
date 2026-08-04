import random

import pyxel

from ..ui.message_box import MessageBox
from ..ui.window import draw_window
from .base_state import BaseState

TILE_MAPPING = {
    (0, 1): "GRASS",
    (1, 0): "ENTRANCE",
    (2, 0): "MOUNTAIN",
    (0, 2): "VILLAGE",
    (2, 2): "CASTLE",
    (4, 2): "CAVE",
    (6, 2): "DEMON_CASTLE",
    (0, 6): "WALL",
    (2, 6): "TABLE",
}


class FieldState(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.tile_size = 16  # 16x16ピクセル

        # プレイヤーのグリッド位置（マス目単位）
        self.player_x = 1
        self.player_y = 1

        # モード管理: "EXPLORE", "MAIN_MENU", "SPELL_MENU", "ITEM_MENU", "STATS_MENU", "MESSAGE"
        self.mode = "EXPLORE"

        self.cursor = 0  # メインメニュー用カーソル (0:じゅもん, 1:つよさ, 2:どうぐ)
        self.sub_cursor = 0  # サブメニュー用カーソル

        # メッセージボックス（UI）
        self.msg_box = MessageBox(
            x=10, y=65, width=140, height=45, speed=2, font=self.app.font
        )

    def get_tile_type(self, grid_x: int, grid_y: int) -> str:
        """指定した16x16グリッドのタイル種別を pyxres のタイルマップから取得"""
        # 16x16タイルの左上になる8x8タイルの座標を計算
        tm_x = grid_x * 2
        tm_y = grid_y * 2

        # タイルマップ0からその位置のマップチップ情報(tx, ty)を取得
        tile_info = pyxel.tilemaps[0].pget(tm_x, tm_y)  # (tx, ty) が返る

        # 対応表から属性を取得（未知のタイルは平地扱い）
        return TILE_MAPPING.get(tile_info, "GRASS")

    def can_move_to(self, grid_x: int, grid_y: int) -> bool:
        """衝突判定: マップ端および障害物（山・海）のチェック"""
        # 画面サイズ内チェック (横10マス, 縦6マス)
        if grid_x < 0 or grid_x >= 12 or grid_y < 0 or grid_y >= 8:
            return False

        tile_type = self.get_tile_type(grid_x, grid_y)

        # 壁・山の移動不可判定
        IMPASSABLE = ["MOUNTAIN", "WALL"]
        return tile_type not in IMPASSABLE

    def update(self):
        match self.mode:
            case "EXPLORE":
                dx, dy = 0, 0
                # 上下左右移動
                if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
                    dy = -1
                elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
                    dy = 1
                elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
                    dx = -1
                elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
                    dx = 1

                if dx != 0 or dy != 0:
                    next_x = self.player_x + dx
                    next_y = self.player_y + dy

                    # 衝突判定を通過したら移動
                    if self.can_move_to(next_x, next_y):
                        self.player_x = next_x
                        self.player_y = next_y

                        # タイルに応じたイベント
                        tile_type = self.get_tile_type(self.player_x, self.player_y)
                        match tile_type:
                            case "GRASS":
                                if random.random() < 0.15:
                                    self.trigger_battle()
                            case "VILLAGE":
                                p = self.app.player
                                p.hp = p.max_hp
                                p.mp = p.max_mp
                                self.msg_box.push_messages(
                                    [
                                        "まち に とうちゃくした！",
                                        "HPと MPが かんぜんかいふく！",
                                    ]
                                )
                                self.mode = "MESSAGE"

                # XキーまたはESCキーでメニューを開く
                if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE):
                    self.mode = "MAIN_MENU"
                    self.cursor = 0

            # --- 2. メインメニュー選択 ---
            case "MAIN_MENU":
                if pyxel.btnp(pyxel.KEY_UP):
                    self.cursor = (self.cursor - 1) % 3
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    self.cursor = (self.cursor + 1) % 3

                # XキーまたはESCでメニューを閉じる
                if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE):
                    self.mode = "EXPLORE"

                # 決定
                elif (
                    pyxel.btnp(pyxel.KEY_Z)
                    or pyxel.btnp(pyxel.KEY_SPACE)
                    or pyxel.btnp(pyxel.KEY_RETURN)
                ):
                    p = self.app.player
                    match self.cursor:
                        case 0:  # じゅもん
                            if not p.spells:
                                self.msg_box.push_messages(
                                    ["じゅもんを おぼえていない！"]
                                )
                                self.mode = "MESSAGE"
                            else:
                                self.mode = "SPELL_MENU"
                                self.sub_cursor = 0

                        case 1:  # つよさ
                            self.mode = "STATS_MENU"

                        case 2:  # どうぐ
                            # ★修正: リストが空かどうか直接チェック
                            if not p.items:
                                self.msg_box.push_messages(["どうぐを もっていない！"])
                                self.mode = "MESSAGE"
                            else:
                                self.mode = "ITEM_MENU"
                                self.sub_cursor = 0

            # --- 3. 呪文選択・使用 ---
            case "SPELL_MENU":
                p = self.app.player
                if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE):
                    self.mode = "MAIN_MENU"

                elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN):
                    if len(p.spells) > 1:
                        self.sub_cursor = (self.sub_cursor + 1) % len(p.spells)

                elif (
                    pyxel.btnp(pyxel.KEY_Z)
                    or pyxel.btnp(pyxel.KEY_SPACE)
                    or pyxel.btnp(pyxel.KEY_RETURN)
                ):
                    selected_spell = p.spells[self.sub_cursor]

                    # 回復呪文（ホイミなど）の場合
                    if selected_spell.heal_amount > 0:
                        if p.mp < selected_spell.mp_cost:
                            self.msg_box.push_messages(["MPが たりない！"])
                        else:
                            p.mp -= selected_spell.mp_cost
                            healed = p.heal(selected_spell.heal_amount)
                            self.msg_box.push_messages(
                                [
                                    f"{p.name} は {selected_spell.name} を となえた！",
                                    f"HPが {healed} かいふくした！",
                                ]
                            )
                        self.mode = "MESSAGE"

            # --- 4. 道具選択・使用 ---
            case "ITEM_MENU":
                p = self.app.player

                if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_ESCAPE):
                    self.mode = "MAIN_MENU"

                # カーソル上下移動
                elif pyxel.btnp(pyxel.KEY_UP):
                    if p.items:
                        self.sub_cursor = (self.sub_cursor - 1) % len(p.items)
                elif pyxel.btnp(pyxel.KEY_DOWN):
                    if p.items:
                        self.sub_cursor = (self.sub_cursor + 1) % len(p.items)

                elif (
                    pyxel.btnp(pyxel.KEY_Z)
                    or pyxel.btnp(pyxel.KEY_SPACE)
                    or pyxel.btnp(pyxel.KEY_RETURN)
                ) and p.items:
                    item = p.items.pop(self.sub_cursor)

                    if item in ["herb"]:  # やくそう
                        healed = p.heal(15)
                        self.msg_box.push_messages(
                            [
                                f"{p.name} は やくそうを つかった！",
                                f"HPが {healed} かいふくした！",
                            ]
                        )
                        self.mode = "MESSAGE"

            # --- 5. ステータス画面 ---
            case "STATS_MENU":
                # どのボタンを押してもメインメニューへ戻る
                if (
                    pyxel.btnp(pyxel.KEY_Z)
                    or pyxel.btnp(pyxel.KEY_X)
                    or pyxel.btnp(pyxel.KEY_SPACE)
                    or pyxel.btnp(pyxel.KEY_RETURN)
                    or pyxel.btnp(pyxel.KEY_ESCAPE)
                ):
                    self.mode = "MAIN_MENU"

            # --- 6. メッセージ表示中 ---
            case "MESSAGE":
                all_done = self.msg_box.update()
                if all_done:
                    self.mode = "MAIN_MENU"

    def trigger_battle(self):
        from .battle_state import BattleState

        # スライムまたはドラキーをランダム出現
        monster_id = random.choice(["entenstr", "rarutaes"])
        monster = self.app.repo.create_monster(monster_id)
        self.app.change_state(BattleState(self.app, monster))

    def draw(self):
        pyxel.cls(0)  # 緑色のフィールド背景

        # ★ 1. Pyxel Editorのタイルマップ0を画面描画
        # pyxel.bltm(x, y, tm, u, v, w, h, [colkey])
        # (x=0, y=16 の位置に、タイルマップ0の (0,0) から幅160px、高さ112px分を描画)
        pyxel.bltm(0, 16, 0, 0, 0, 192, 128)

        # # 簡易なグリッド背景描画
        # for x in range(0, 160, 8):
        #     pyxel.line(x, 0, x, 120, 11)
        # for y in range(0, 120, 8):
        #     pyxel.line(0, y, 160, y, 11)

        # ★ 2. 16x16 勇者キャラクターの描画
        player_px = self.player_x * self.tile_size
        player_py = self.player_y * self.tile_size + 16

        # イメージバンク0の (x=0, y=16) に16x16の勇者ドット絵がある場合の例
        # (最後の引数 0 は黒色を透明色として透過描画する指定です)
        pyxel.blt(player_px, player_py, 0, 0, 0, 16, 16, 8)

        # # プレイヤーの描画（ドットまたは文字）
        # px = self.player_x * self.grid_size
        # py = self.player_y * self.grid_size
        # pyxel.rect(px, py, 8, 8, 8)  # 赤い四角をプレイヤーとする

        # 簡易UI
        pyxel.rect(0, 0, 160, 12, 0)
        p = self.app.player
        pyxel.text(
            4, 3, f"HERO LV:{p.level} HP:{p.hp}/{p.max_hp} G:{p.gold}", 7, self.app.font
        )
        pyxel.text(4, 110, "MOVE: ARROW KEYS", 7)

        # --- メニュー表示中の重ね描き（オーバーレイ） ---
        if self.mode != "EXPLORE":
            # メインメニュー枠
            draw_window(10, 20, 50, 42)
            pyxel.text(20, 25, "じゅもん", 7, self.app.font)
            pyxel.text(20, 35, "つよさ", 7, self.app.font)
            pyxel.text(20, 45, "どうぐ", 7, self.app.font)
            pyxel.text(14, 25 + self.cursor * 10, ">", 10, self.app.font)

            match self.mode:
                # 呪文サブメニュー
                case "SPELL_MENU":
                    draw_window(65, 20, 85, 42)
                    for i, spell in enumerate(p.spells):
                        pyxel.text(
                            75,
                            25 + i * 10,
                            f"{spell.name} M:{spell.mp_cost}",
                            7,
                            self.app.font,
                        )
                    pyxel.text(69, 25 + self.sub_cursor * 10, ">", 10, self.app.font)

                # 道具サブメニュー
                case "ITEM_MENU":
                    draw_window(65, 20, 85, 42)
                    for i, item in enumerate(p.items):
                        name = "やくそう" if item == "herb" else item
                        pyxel.text(75, 25 + i * 10, name, 7, self.app.font)
                    pyxel.text(69, 25 + self.sub_cursor * 10, ">", 10, self.app.font)

                # つよさ（詳細ステータス）画面
                case "STATS_MENU":
                    draw_window(65, 20, 85, 80)
                    pyxel.text(70, 25, f"なに: {p.name}", 7, self.app.font)
                    pyxel.text(70, 35, f"レベル: {p.level}", 7, self.app.font)
                    pyxel.text(70, 45, f"こうげき: {p.attack}", 7, self.app.font)
                    pyxel.text(70, 55, f"しゅび: {p.defense}", 7, self.app.font)
                    pyxel.text(70, 65, f"けいけん: {p.exp}", 7, self.app.font)
                    pyxel.text(70, 75, f"ゴールド: {p.gold}", 7, self.app.font)

                # メッセージウィンドウ
                case "MESSAGE":
                    self.msg_box.draw()
