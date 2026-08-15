import json
from pathlib import Path

from ..data.exp_table import EXP_TABLE
from ..data.items import ItemCode
from ..data.spells import SPELL_MASTER, SpellCode
from .monster import Monster
from .player import Player
from .spell import Spell


class GameRepository:
    def __init__(self, data_dir: str | None = None):
        if data_dir is None:
            # repository.py の位置から自動的に data ディレクトリの絶対パスを求める
            # repository.py から見て 1つ上のフォルダ(ester_mastal)の data を探す
            base_path = Path(__file__).resolve().parent.parent / "data"

            # もしプロジェクトルート直下に data がある場合のフォールバック
            if not base_path.exists():
                base_path = Path(__file__).resolve().parent.parent.parent / "data"

            self.data_dir = base_path
        else:
            self.data_dir = Path(data_dir)
        self.monsters_data = self._load_json("monsters.json")
        self.spells_data = SPELL_MASTER
        self.exp_table_data = EXP_TABLE
        self.items_data = self._load_json("items.json")

    def _load_json(self, filename: str):
        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(
                f"\n[エラー] データファイルが見つかりません。\n"
                f"探したパス: {path.resolve()}\n"
                f"data ディレクトリの中に {filename} が配置されているか確認してください。"
            )
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def create_monster(self, monster_id: str) -> Monster:
        """IDからモンスターインスタンスを生成"""
        if monster_id not in self.monsters_data:
            raise ValueError(f"Monster ID '{monster_id}' not found.")

        data = self.monsters_data[monster_id]
        sprite = data.get("sprite", {})
        return Monster(
            name=data["name"],
            max_hp=data["hp"],
            hp=data["hp"],
            attack=data["attack"],
            defense=data["defense"],
            exp_yield=data["exp"],
            gold_yield=data["gold"],
            is_boss=data.get("is_boss", False),
            sprite_u=sprite.get("u", 0),
            sprite_v=sprite.get("v", 32),
            sprite_w=sprite.get("w", 16),
            sprite_h=sprite.get("h", 16),
            colkey=sprite.get("colkey", 0),
        )

    def get_spell(self, spell_id: SpellCode) -> Spell:
        """IDから呪文インスタンスを取得"""
        return self.spells_data[spell_id]

    def create_initial_player(self, name: str) -> Player:
        """初期（LV1）のプレイヤーを生成"""
        lv1_data = self.exp_table_data[0]
        return Player(
            name=name,
            max_hp=lv1_data.max_hp,
            hp=lv1_data.max_hp,
            max_mp=lv1_data.max_mp,
            mp=lv1_data.max_mp,
            base_attack=lv1_data.base_attack,
            base_defense=lv1_data.base_defense,
            level=1,
            exp=0,
            gold=10,
            inventory=[ItemCode.POTION],
        )

    def check_level_up(self, player: Player) -> list[str]:
        """JSONデータに基づいたレベルアップ処理"""
        logs = []
        # 現在のレベルより上データを確認
        for entry in self.exp_table_data:
            target_lv = entry.level
            if target_lv > player.level and player.exp >= entry.required_exp:
                player.level = target_lv
                player.max_hp = entry.max_hp
                player.hp = player.max_hp  # レベルアップ時全回復
                player.max_mp = entry.max_mp
                player.mp = player.max_mp
                player.base_attack = entry.base_attack
                player.base_defense = entry.base_defense
                logs.append(f"{player.name} は レベル {player.level} に あがった！")

                # 習得呪文があるかチェック
                spell_code = entry.learn_spell
                if spell_code:
                    player.spells.append(spell_code)
                    logs.append(
                        f"{player.name} は {spell_code.value} の じゅもんを おぼえた！"
                    )

        return logs
