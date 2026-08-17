import copy

from data.monsters import MONSTER_MASTER
from models.monster import Monster, MonsterCode, MonsterRepository


class InMemoryMonsterRepository(MonsterRepository):
    def __init__(self, master_data: dict[MonsterCode, Monster] = MONSTER_MASTER):
        self._master_data = master_data

    def find_by_code(self, code):
        monster = self._master_data.get(code)
        if monster is not None:
            # ★ copy.deepcopy() で原本を変更させない「独立したコピー」を返します！
            return copy.deepcopy(monster)
        return None

    def get_all(self):
        return list(self._master_data.values())
