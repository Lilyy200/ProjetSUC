from enum import Enum


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def distance(self, another):
        return ((self.x - another.x)**2 + (self.y - another.y)**2)**0.5

class MinePatternType(Enum):
    CIRCLE = 1
    SQUARE = 2
    TRIANGLE = 3
    CROSS = 4
    V_SHAPE = 5

class MinePattern:
    def __init__(self, type: MinePatternType, mine_coords: list[Point], pattern_size, offset_x, offset_y):
        self.type = type
        self.mine_coords = mine_coords
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.pattern_size = pattern_size

class MineField:
    def __init__(self, patterns: list[MinePattern], noise: list[Point], max_x, max_y, pattern_size):
        self.patterns = patterns
        self.noise = noise
        self.max_x = max_x
        self.max_y = max_y
        self.pattern_size = pattern_size

    def points(self):
        for pattern in self.patterns:
            for coord in pattern.mine_coords:
                yield coord

        for point in self.noise:
            yield point


