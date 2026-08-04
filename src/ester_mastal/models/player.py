from dataclasses import dataclass, field


@dataclass
class Spell:
    name: str
    mp_cost: int
    heal_amount: int = 0
    damage_amount: int = 0


@dataclass
class Player:
    name: str
    max_hp: int
    hp: int
    max_mp: int
    mp: int
    attack: int
    defense: int
    level: int = 1
    exp: int = 0
    gold: int = 0
    spells: list[Spell] = field(default_factory=list)
    items: dict[str, int] = field(default_factory=dict)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def heal(self, amount: int) -> int:
        """HPを回復し、実際に回復した値を返す"""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def take_damage(self, amount: int) -> int:
        """ダメージを受け、実際に受けたダメージを返す"""
        damage = max(1, amount)
        self.hp = max(0, self.hp - damage)
        return damage

    def check_level_up(self) -> list[str]:
        """レベルアップ判定（必要経験値テーブル）"""
        logs = []
        # 次のレベルに必要な累積経験値テーブル
        exp_table = {2: 10, 3: 30, 4: 70, 5: 150}

        next_level = self.level + 1
        if next_level in exp_table and self.exp >= exp_table[next_level]:
            self.level = next_level
            self.max_hp += 5
            self.hp = self.max_hp
            self.max_mp += 3
            self.mp = self.max_mp
            self.attack += 2
            self.defense += 2
            logs.append(f"{self.name} は レベル {self.level} に あがった！")

            # レベル2でホイミ習得例
            if self.level == 2:
                hoimi = Spell(name="ホイミ", mp_cost=3, heal_amount=15)
                self.spells.append(hoimi)
                logs.append(f"{self.name} は {hoimi.name} の じゅもんを おぼえた！")

        return logs
