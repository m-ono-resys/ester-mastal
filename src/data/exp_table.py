from dataclasses import dataclass

from models.spell import SpellCode


@dataclass(frozen=True)
class ExpRow:
    level: int
    required_exp: int
    max_hp: int
    max_mp: int
    base_attack: int
    base_defense: int
    learn_spell: SpellCode | None


EXP_TABLE: list[ExpRow] = [
    ExpRow(1, 0, 15, 0, 8, 5, None),
    ExpRow(2, 7, 28, 8, 16, 8, SpellCode.IMARU),
    ExpRow(3, 30, 42, 16, 24, 18, SpellCode.IRAMEI),
    ExpRow(4, 60, 60, 24, 32, 24, SpellCode.AIMETO),
    ExpRow(5, 200, 84, 36, 40, 32, SpellCode.MASARA),
]
