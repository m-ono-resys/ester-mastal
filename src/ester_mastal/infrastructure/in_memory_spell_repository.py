from ester_mastal.data.spells import SPELL_MASTER
from ester_mastal.models.spell import Spell, SpellCode, SpellRepository


class InMemorySpellRepository(SpellRepository):
    def __init__(self, master_data: dict[SpellCode, Spell] = SPELL_MASTER):
        self._master_data = master_data

    def find_by_code(self, code):
        return self._master_data.get(code)

    def get_all(self):
        return list(self._master_data.values())
