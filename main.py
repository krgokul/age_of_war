from dataclasses import dataclass
from typing import List
from itertools import permutations

CLASS_ADVANTAGE = {
    "Militia": {"Spearmen", "LightCavalry"},
    "Spearmen": {"LightCavalry", "HeavyCavalry"},
    "LightCavalry": {"FootArcher", "CavalryArcher"},
    "HeavyCavalry": {"Militia", "FootArcher", "LightCavalry"},
    "CavalryArcher": {"Spearmen", "HeavyCavalry"},
    "FootArcher": {"Militia", "CavalryArcher"},
}


@dataclass
class Platoon:
    unit_class: str
    count: int

    @staticmethod
    def from_string(s: str) -> "Platoon":
        cls, count = s.split("#")
        return Platoon(cls, int(count))

    def to_string(self) -> str:
        return f"{self.unit_class}#{self.count}"


class BattlePlanner:
    def __init__(self, own_line: str, enemy_line: str):
        self.own_platoons = self._parse_line(own_line)
        self.enemy_platoons = self._parse_line(enemy_line)

    def _parse_line(self, line: str) -> List[Platoon]:
        return [Platoon.from_string(p.strip()) for p in line.strip().split(";")]

    def _has_advantage(self, attacker: str, defender: str) -> bool:
        return defender in CLASS_ADVANTAGE.get(attacker, set())

    def _battle_outcome(self, own: Platoon, enemy: Platoon) -> str:
        if self._has_advantage(own.unit_class, enemy.unit_class):
            own_eff = own.count * 2
            enemy_eff = enemy.count
        elif self._has_advantage(enemy.unit_class, own.unit_class):
            own_eff = own.count
            enemy_eff = enemy.count * 2
        else:
            own_eff = own.count
            enemy_eff = enemy.count

        if own_eff > enemy_eff:
            return "W"
        elif own_eff == enemy_eff:
            return "D"
        else:
            return "L"

    def find_best_arrangement(self) -> str:
        for perm in permutations(self.own_platoons):
            win_count = 0
            for own, enemy in zip(perm, self.enemy_platoons):
                result = self._battle_outcome(own, enemy)
                if result == "W":
                    win_count += 1
                    if win_count >= 3:
                        break  # Early exit

            if win_count >= 3:
                return ";".join(p.to_string() for p in perm)

        return "There is no chance of winning"


if __name__ == "__main__":
    own_input = (
        "Spearmen#10;Militia#30;FootArcher#20;LightCavalry#1000;HeavyCavalry#120"
    )
    enemy_input = (
        "Militia#10;Spearmen#10;FootArcher#1000;LightCavalry#120;CavalryArcher#100"
    )

    planner = BattlePlanner(own_input, enemy_input)
    result = planner.find_best_arrangement()
    print(result)
