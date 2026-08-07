from ester_mastal.models.spell import Spell, SpellCode, SpellType

SPELL_MASTER: dict[SpellCode, Spell] = {
    SpellCode.IMARU: Spell("イマル", SpellType.HEAL, 2, 20, "HPを 20 かいふくする"),
    SpellCode.IRAMEI: Spell("イラメイ", SpellType.ATTACK, 3, 20, "モンスターに 20 ダメージ"),
    SpellCode.AIMETO: Spell("アイメト", SpellType.HEAL, 5, 40, "HPを 40 かいふくする"),
    SpellCode.MASARA: Spell("マサラ", SpellType.DEFENCE_BUFF, 2, 20, "まもりが 20 あがる"),
}