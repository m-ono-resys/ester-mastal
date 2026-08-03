from ester_mastal.models.repository import GameRepository
from ester_mastal.models.battle import BattleEngine

def main():
    repo = GameRepository()

    # 1. JSONからプレイヤーとスライムを生成
    hero = repo.create_initial_player("ゆうしゃ")
    slime = repo.create_monster("entenstr")

    print(f"【初期状態】 {hero.name}: LV{hero.level} HP{hero.hp} ATK{hero.attack}")
    print(f"【出現敵】 {slime.name}: HP{slime.hp} ATK{slime.attack}")

    # 2. 戦闘テスト
    battle = BattleEngine(hero, slime)
    logs = battle.player_attack() # 一撃で倒せる想定で手動で経験値を加算してテスト
    for log in logs:
        print(" >", log)

    # 3. 大量経験値を得てレベルアップのテスト
    print("\n--- 経験値10を投与してレベルアップ判定 ---")
    hero.exp += 10
    lvl_logs = repo.check_level_up(hero)
    for log in lvl_logs:
        print(" >", log)

    print(f"【成長後】 {hero.name}: LV{hero.level} HP{hero.hp} MP{hero.mp}")

if __name__ == "__main__":
    main()