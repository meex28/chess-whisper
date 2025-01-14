from app.levels.level0 import level_zero
from app.levels.level1 import level_one
from app.levels.level2 import level_two
from app.levels.level3 import level_three
from app.levels.types import Level

all_levels: list[Level] = [
    level_zero,
    level_one,
    level_two,
    level_three
]

def find_next_level(current_level_id: str):
    for i, level in enumerate(all_levels):
        if level.id == current_level_id:
            if i < len(all_levels) - 1:
                return all_levels[i + 1]
            else:
                return None
    return None
