import mine_field as mf
import random

def _gen_pattern_cordinate(width, height, count, pattern_size) -> list[tuple[int, int]]:
    max_x = width - pattern_size
    max_y = height - pattern_size
    coords = []
    radius = pattern_size * 2  # Minimum distance between patterns

    while True:
        possible = True
        point = mf.Point(x=random.randint(0, max_x), y=random.randint(0, max_y))

        for cord in coords:
            if point.distance(cord) < radius:
                possible = False
                break

        if possible:
            coords.append(point)
            if len(coords) >= count:
                break

    return [(c.x, c.y) for c in coords]

def _gen_triangle(offset_x, offset_y, pattern_size) -> mf.MinePattern:
    mines = []
    orientation_x = random.choice((1, -1))
    orientation_y = random.choice((1, -1))
    
    for i in range(pattern_size // 3):
        for j in range(i + 1):
            mine_offset_x = random.randint(-1, 1) + i * 3
            mine_offset_x = mine_offset_x if orientation_x == 1 else pattern_size - mine_offset_x
            mine_offset_y = random.randint(-1, 1) + j * 3
            mine_offset_y = mine_offset_y if orientation_y == 1 else pattern_size - mine_offset_y
            mine_x = offset_x + mine_offset_x
            mine_y = offset_y + mine_offset_y
            mines.append(mf.Point(x=mine_x, y=mine_y))

    return mf.MinePattern(mf.MinePatternType.TRIANGLE, mines, pattern_size, offset_x, offset_y)

def _gen_square(offset_x, offset_y, pattern_size) -> mf.MinePattern:
    mines = []

    for i in range(0, pattern_size, 3):
        for j in range(0, pattern_size, 3):
            mine_offset_x = random.randint(-1, 1) + i
            mine_offset_y = random.randint(-1, 1) + j
            mine_x = offset_x + mine_offset_x
            mine_y = offset_y + mine_offset_y
            mines.append(mf.Point(x=mine_x, y=mine_y))

    return mf.MinePattern(mf.MinePatternType.SQUARE, mines, pattern_size, offset_x, offset_y)

def _gen_cross(offset_x, offset_y, pattern_size) -> mf.MinePattern:
    mines = []

    for i in range(pattern_size // 2):
        mine_offset_x1 = random.randint(-1, 1) + i * 2
        mine_offset_x2 = random.randint(-1, 1) + i * 2
        mine_offset_y1 = random.randint(-1, 1) + i * 2
        mine_offset_y2 = random.randint(-1, 1) + pattern_size - i * 2 - 1
        mine_x1 = offset_x + mine_offset_x1
        mine_x2 = offset_x + mine_offset_x2
        mine_y1 = offset_y + mine_offset_y1
        mine_y2 = offset_y + mine_offset_y2
        mines.append(mf.Point(x=mine_x1, y=mine_y1))
        mines.append(mf.Point(x=mine_x2, y=mine_y2))

    return mf.MinePattern(mf.MinePatternType.CROSS, mines, pattern_size, offset_x, offset_y)

def _gen_circle(offset_x, offset_y, pattern_size) -> mf.MinePattern:
    mines = []
    radius = pattern_size / 2

    for i in range(0, pattern_size, 3):
        sin = (i - radius) / radius
        cos = (1 - sin**2)**0.5 

        start = int(radius - radius * cos)
        stop = int(radius + radius * cos)

        for j in range(start, stop, 3):
            mine_offset_x = random.randint(-1, 1) + i
            mine_offset_y = random.randint(-1, 1) + j
            mine_x = offset_x + mine_offset_x
            mine_y = offset_y + mine_offset_y
            mines.append(mf.Point(x=mine_x, y=mine_y))

    return mf.MinePattern(mf.MinePatternType.CIRCLE, mines, pattern_size, offset_x, offset_y)

def _gen_v_shape(offset_x, offset_y, pattern_size) -> mf.MinePattern:
    mines = []

    for i in range(pattern_size // 2):
        mine_offset_x1 = random.randint(-1, 1) + i
        mine_offset_x2 = random.randint(-1, 1) + pattern_size - i
        mine_offset_y1 = random.randint(-1, 1) + i * 2
        mine_offset_y2 = random.randint(-1, 1) + i * 2
        mine_x1 = offset_x + mine_offset_x1
        mine_x2 = offset_x + mine_offset_x2
        mine_y1 = offset_y + mine_offset_y1
        mine_y2 = offset_y + mine_offset_y2
        mines.append(mf.Point(x=mine_x1, y=mine_y1))
        mines.append(mf.Point(x=mine_x2, y=mine_y2))

    return mf.MinePattern(mf.MinePatternType.V_SHAPE, mines, pattern_size, offset_x, offset_y)

def gen_mine_field(max_x = 128, max_y = 128, pattern_size = 20, pattern_count = 5) -> mf.MineField:
    patterns = []
    noise = []
    pattern_cords = _gen_pattern_cordinate(max_x, max_y, pattern_count, pattern_size)
    pattern_types = list(mf.MinePatternType)

    for offset_x, offset_y in pattern_cords:
        pattern_type = random.choice(pattern_types)

        if pattern_type == mf.MinePatternType.CIRCLE:
            patterns.append(_gen_circle(offset_x, offset_y, pattern_size))
        elif pattern_type == mf.MinePatternType.SQUARE:
            patterns.append(_gen_square(offset_x, offset_y, pattern_size))
        elif pattern_type == mf.MinePatternType.CROSS:
            patterns.append(_gen_cross(offset_x, offset_y, pattern_size))
        elif pattern_type == mf.MinePatternType.TRIANGLE:
            patterns.append(_gen_triangle(offset_x, offset_y, pattern_size))
        elif pattern_type == mf.MinePatternType.V_SHAPE:
            patterns.append(_gen_v_shape(offset_x, offset_y, pattern_size))
        else:
            raise Exception(f'Unknown pattern type {pattern_type}')

    noise_max = (max_x + max_y) // 2

    for _ in range(random.randint(noise_max // 2, noise_max)):
        noise_x = random.randint(0, max_x)
        noise_y = random.randint(0, max_y)
        noise.append(mf.Point(x=noise_x, y=noise_y))

    return mf.MineField(patterns, noise, max_x, max_y, pattern_size)
