from dataclasses import dataclass

from ..models.spell import SpellCode


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
    ExpRow(2, 7, 22, 6, 12, 8, SpellCode.IMARU),
    ExpRow(3, 22, 30, 12, 18, 12, SpellCode.IRAMEI),
    ExpRow(4, 50, 42, 18, 26, 18, SpellCode.AIMETO),
    ExpRow(5, 100, 60, 26, 36, 25, SpellCode.MASARA),
]
