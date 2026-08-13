from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum


class MonsterCode(StrEnum):
    ENTENSTR = "エンテンストル"
    RARUTAES = "ラルターエス"
    MENTATOL = "メンタートル"
    SANTROTO = "サントーロート"
    DERAMILE = "まおう デラミール"

@dataclass
class Monster:
    name: str
    max_hp: int
    hp: int
    attack: int
    defense: int
    exp_yield: int
    gold_yield: int
    is_boss: bool = False
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

class MonsterRepository(ABC):
    @abstractmethod
    def find_by_code(self, code: MonsterCode) -> Monster | None:
        """モンスターコードから Monster を取得する（存在しない場合は None）"""

    @abstractmethod
    def get_all(self) -> list[Monster]:
        """全モンスターを取得する"""
