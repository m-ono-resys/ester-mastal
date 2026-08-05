import pyxel


def init_audio():
    """コード上でレトロ効果音とファンファーレを自動生成"""
    # SE 0: 攻撃音（シュッと下降する音）
    pyxel.sounds[0].set("c3c2", "n", "7", "f", 4)

    # SE 1: 回復魔法音（ポピポピ音）
    pyxel.sounds[1].set("g3c4e4g4", "t", "6", "v", 8)

    # SE 2: ダメージ音（ドゴッという重低音）
    pyxel.sounds[2].set("f2c2", "p", "7", "f", 6)

    # SE 3: 勝利ファンファーレ（タタタターン！）
    pyxel.sounds[3].set("c3e3g3c4 c4c4 g3c4", "t", "6", "v", 12)


def play_se(sound_id: int):
    """チャンネル3を使って効果音を再生"""
    pyxel.play(3, sound_id)
