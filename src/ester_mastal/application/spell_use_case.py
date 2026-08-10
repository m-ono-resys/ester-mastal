from ..models.player import Player
from ..models.spell import SpellCode, SpellRepository, SpellType


class SpellUseCase:
    def __init__(self, spell_repository: SpellRepository):
        self._spell_repository = spell_repository

    def use_spell(self, player: Player, spell_code: SpellCode) -> list[str]:
        spell = self._spell_repository.find_by_code(spell_code)

        if not spell:
            return ["じゅもんが存在しません"]

        if player.mp < spell.mp_cost:
            return ["MPが たりない！"]

        match spell.spell_type:
            case SpellType.HEAL:
                healed = player.heal_hp(
                    spell.effect_value
                )  # ★ 実際に回復した値を受け取る
                player.mp -= spell.mp_cost
                return [f"{spell.name} を つかった！\nHPが {healed} かいふくした！"]

            case _:
                return ["ここでは つかえない"]
