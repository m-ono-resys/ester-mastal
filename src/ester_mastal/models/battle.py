import random

from .monster import Monster
from .player import Player, Spell


class BattleEngine:
    def __init__(self, player: Player, monster: Monster):
        self.player = player
        self.monster = monster
        self.is_finished = False

    def calculate_physical_damage(self, attacker_atk: int, defender_def: int) -> int:
        """ドラクエ1風ダメージ計算式: (攻撃力 - 防御力/2) / 2 + 乱数"""
        base = (attacker_atk - (defender_def // 2)) // 2
        if base <= 0:
            return random.choice([0, 1])  # 低攻撃力時は0か1ダメージ

        # 振れ幅（±16%程度）
        variance = max(1, base // 6)
        damage = base + random.randint(-variance, variance)
        return max(1, damage)

    def player_attack(self) -> list[str]:
        """プレイヤーの「たたかう」"""
        logs = [f"{self.player.name} の こうげき！"]

        # 会心の一撃判定（1/16の確率）
        if random.randint(1, 16) == 1:
            logs.append("かいしんの いちげき！")
            damage = self.player.attack  # 防御無視ダメージ
        else:
            damage = self.calculate_physical_damage(
                self.player.attack, self.monster.defense
            )

        actual_damage = self.monster.take_damage(damage)
        logs.append(f"{self.monster.name} に {actual_damage} の ダメージ！")

        if not self.monster.is_alive:
            logs.extend(self._process_victory())
            self.is_finished = True

        return logs

    def player_cast_spell(self, spell: Spell) -> list[str]:
        """プレイヤーの「じゅもん」"""
        logs = [f"{self.player.name} は {spell.name} を となえた！"]

        if self.player.mp < spell.mp_cost:
            logs.append("しかし MPが たりない！")
            return logs

        self.player.mp -= spell.mp_cost

        # 回復魔法の場合
        if spell.heal_amount > 0:
            healed = self.player.heal(spell.heal_amount)
            logs.append(f"{self.player.name} の HPが {healed} かいふくした！")

        # 攻撃魔法の場合（例：メラなど）
        elif spell.damage_amount > 0:
            damage = spell.damage_amount + random.randint(-2, 2)
            actual_damage = self.monster.take_damage(damage)
            logs.append(f"{self.monster.name} に {actual_damage} の ダメージ！")
            if not self.monster.is_alive:
                logs.extend(self._process_victory())
                self.is_finished = True

        return logs

    def player_escape(self) -> tuple[list[str], bool]:
        """プレイヤーの「にげる」（成功判定付き）"""
        logs = [f"{self.player.name} は にげだした！"]
        # 成功率 50%
        if random.random() < 0.5:
            logs.append("うまく にげきることが できた！")
            self.is_finished = True
            return logs, True
        else:
            logs.append("しかし まわりこまれた！")
            return logs, False

    def monster_turn(self) -> list[str]:
        """モンスターのターン（AI）"""
        if not self.monster.is_alive or self.is_finished:
            return []

        logs = [f"{self.monster.name} の こうげき！"]
        damage = self.calculate_physical_damage(
            self.monster.attack, self.player.defense
        )
        actual_damage = self.player.take_damage(damage)
        logs.append(f"{self.player.name} は {actual_damage} の ダメージを うけた！")

        if not self.player.is_alive:
            logs.append(f"{self.player.name} は しんでしまった！")
            self.is_finished = True

        return logs

    def _process_victory(self) -> list[str]:
        """勝利処理"""
        logs = [
            f"{self.monster.name} を たおした！",
            f"{self.monster.exp_yield} の けいけんちを かくとく！",
            f"{self.monster.gold_yield} ゴールドを てにいれた！",
        ]
        self.player.exp += self.monster.exp_yield
        self.player.gold += self.monster.gold_yield

        # レベルアップチェック
        lvl_logs = self.player.check_level_up()
        logs.extend(lvl_logs)
        return logs
