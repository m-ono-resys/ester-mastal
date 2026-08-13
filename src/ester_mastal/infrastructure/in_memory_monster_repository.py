from ..data.monsters import MONSTER_MASTER
from ..models.monster import Monster, MonsterCode, MonsterRepository


class InMemoryMonsterRepository(MonsterRepository):
    def __init__(self, master_data: dict[MonsterCode, Monster] = MONSTER_MASTER):
        self._master_data = master_data

    def find_by_code(self, code):
        return self._master_data.get(code)

    def get_all(self):
        return list(self._master_data.values())
