from models.monster import Monster, MonsterCode

MONSTER_MASTER: dict[MonsterCode, Monster] = {
    MonsterCode.ENTENSTR: Monster(
        MonsterCode.ENTENSTR.value, 18, 18, 7, 3, 2, 4, False, 0, 64, 32, 32, 0
    ),
    MonsterCode.RARUTAES: Monster(
        MonsterCode.RARUTAES.value, 42, 42, 18, 12, 5, 8, False, 32, 64, 32, 32, 0
    ),
    MonsterCode.MENTATOL: Monster(
        MonsterCode.MENTATOL.value, 76, 76, 24, 20, 18, 25, False, 64, 64, 32, 32, 0
    ),
    MonsterCode.SANTROTO: Monster(
        MonsterCode.SANTROTO.value, 200, 200, 48, 30, 36, 100, True, 48, 96, 32, 48, 0
    ),
    MonsterCode.DERAMILE: Monster(
        MonsterCode.DERAMILE.value, 500, 500, 72, 48, 200, 500, True, 0, 96, 48, 64, 0
    ),
}
