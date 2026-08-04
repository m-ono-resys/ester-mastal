from ester_mastal.models.battle import BattleEngine
from ester_mastal.models.monster import Monster
from ester_mastal.models.player import Player


def print_logs(logs):
    for log in logs:
        print(f" > {log}")


def main():
    # 1. プレイヤーとモンスターの生成
    hero = Player(
        name="ゆうしゃ", max_hp=20, hp=20, max_mp=0, mp=0, attack=10, defense=8
    )
    slime = Monster(
        name="スライム", max_hp=8, hp=8, attack=7, defense=3, exp_yield=12, gold_yield=5
    )

    print("=== 戦闘テスト開始 ===")
    battle = BattleEngine(hero, slime)

    # 最初に出てくるメッセージ
    print(f"{slime.name} が あらわれた！")

    # 簡易ターンループ（CLIで対話的に入力）
    while not battle.is_finished:
        print(f"\n[{hero.name}] HP:{hero.hp}/{hero.max_hp} MP:{hero.mp}/{hero.max_mp}")
        print(f"[{slime.name}] HP:{slime.hp}/{slime.max_hp}")
        print("1: たたかう | 2: じゅもん | 3: にげる")

        choice = input("コマンドを入力してください > ")

        if choice == "1":
            logs = battle.player_attack()
            print_logs(logs)
        elif choice == "2":
            if not hero.spells:
                print(" > じゅもんを おぼえていない！")
                continue
            logs = battle.player_cast_spell(hero.spells[0])
            print_logs(logs)
        elif choice == "3":
            logs, success = battle.player_escape()
            print_logs(logs)
            if success:
                break
        else:
            continue

        # モンスターの反撃（敵が生きていて戦闘が終わっていない場合）
        if not battle.is_finished:
            m_logs = battle.monster_turn()
            print_logs(m_logs)

    print("\n=== 戦闘終了 ===")
    print(f"結果: レベル={hero.level}, 経験値={hero.exp}, 所持金={hero.gold}")


if __name__ == "__main__":
    main()
