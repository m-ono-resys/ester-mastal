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
    IMARU = auto()
    IRAMEI = auto()
    AIMETO = auto()
    MASARA = auto()