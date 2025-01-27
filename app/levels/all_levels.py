from app.levels.level0 import level_zero
from app.levels.level1 import level_one
from app.levels.level10 import level_puzzle_1
from app.levels.level2 import level_two
from app.levels.level3 import level_three
from app.levels.level4 import level_four
from app.levels.level5 import level_five
from app.levels.level6 import level_six
from app.levels.level7 import level_seven
from app.levels.level8 import level_eight
from app.levels.level11 import level_puzzle_2
from app.levels.level9 import level_checks
from app.levels.types import Level

all_levels: list[Level] = [
    level_zero,
    level_one,
    level_two,
    level_three,
    level_four,
    level_five,
    level_six,
    level_seven,
    level_eight,
    level_checks,
    level_puzzle_1,
    level_puzzle_2,
]

def find_next_level(current_level_id: str):
    for i, level in enumerate(all_levels):
        if level.id == current_level_id:
            if i < len(all_levels) - 1:
                return all_levels[i + 1]
            else:
                return None
    return None
