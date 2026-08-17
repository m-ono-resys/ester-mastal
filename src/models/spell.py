from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto


class SpellType(Enum):
    HEAL = auto()
    ATTACK = auto()
    DEFENCE_BUFF = auto()


@dataclass
class Spell:
    name: str
    spell_type: SpellType
    mp_cost: int
    effect_value: int
    description: str = ""


class SpellCode(Enum):
    IMARU = "イマル"
    IRAMEI = "イラメイ"
    AIMETO = "アイメト"
    MASARA = "マサラ"


class SpellRepository(ABC):
    @abstractmethod
    def find_by_code(self, code: SpellCode) -> Spell | None:
        """じゅもんコードから Spell を取得する（存在しない場合は None）"""

    @abstractmethod
    def get_all(self) -> list[Spell]:
        """全じゅもんを取得する"""
