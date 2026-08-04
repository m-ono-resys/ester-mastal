from dataclasses import dataclass


@dataclass
class Monster:
    name: str
    max_hp: int
    hp: int
    attack: int
    defense: int
    exp_yield: int
    gold_yield: int
    sprite_u: int = 0
    sprite_v: int = 64
    sprite_w: int = 32
    sprite_h: int = 32
    colkey: int = 8

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        damage = max(1, amount)
        self.hp = max(0, self.hp - damage)
        return damage
