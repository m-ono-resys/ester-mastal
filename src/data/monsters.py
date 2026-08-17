from models.monster import Monster, MonsterCode

MONSTER_MASTER: dict[MonsterCode, Monster] = {
    MonsterCode.ENTENSTR: Monster(
        MonsterCode.ENTENSTR.value, 8, 8, 7, 3, 2, 4, False, 0, 64, 32, 32, 0
    ),
    MonsterCode.RARUTAES: Monster(
        MonsterCode.RARUTAES.value, 12, 12, 11, 6, 5, 8, False, 32, 64, 32, 32, 0
    ),
    MonsterCode.MENTATOL: Monster(
        MonsterCode.MENTATOL.value, 28, 28, 18, 14, 18, 25, False, 64, 64, 32, 32, 0
    ),
    MonsterCode.SANTROTO: Monster(
        MonsterCode.SANTROTO.value, 50, 50, 30, 20, 36, 100, True, 48, 96, 32, 48, 0
    ),
    MonsterCode.DERAMILE: Monster(
        MonsterCode.DERAMILE.value, 100, 100, 48, 28, 200, 500, True, 0, 96, 48, 64, 0
    ),
}
