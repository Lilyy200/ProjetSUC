import random
from PIL import Image, ImageDraw
import numpy as np

def gen_cords(width, height, count, pattern_size):
    max_x = width - pattern_size
    max_y = height - pattern_size
    coords = []
    radius = pattern_size * 2

    while True:
        possible = True
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        for ox, oy in coords:
            if ((ox - x)**2 + (oy - y)**2)**0.5 < radius:
                possible = False
                break

        if possible:
            coords.append((x, y))
            if len(coords) >= count:
                break

    return coords

def draw_pattern(draw, pattern_type, x, y, point_size):
    if pattern_type == 'triangle':
        for i in range(5):
            for j in range(i + 1):
                px = x + j * point_size * 2
                py = y + i * point_size * 2
                draw.ellipse((px, py, px + point_size, py + point_size), fill="black")

    elif pattern_type == 'square':
        for i in range(5):
            for j in range(5):
                px = x + i * point_size * 2
                py = y + j * point_size * 2
                draw.ellipse((px, py, px + point_size, py + point_size), fill="black")

    elif pattern_type == 'x':
        for i in range(5):
            px1 = x + i * point_size * 2
            py1 = y + i * point_size * 2
            draw.ellipse((px1, py1, px1 + point_size, py1 + point_size), fill="black")
            px2 = x + (4 - i) * point_size * 2
            py2 = y + i * point_size * 2
            draw.ellipse((px2, py2, px2 + point_size, py2 + point_size), fill="black")


def generate_image_array(width, height, num_patterns):
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    coords = gen_cords(width, height, num_patterns, 20)
    point_size = 3
    patterns = ['triangle', 'square', 'x']
    
    # Store pattern types in the image
    used_patterns = []

    # Assign a random pattern type to each coordinate
    for x, y in coords:
        pattern_type = random.choice(patterns)  # Randomly select a pattern type
        used_patterns.append(pattern_type)
        draw_pattern(draw, pattern_type, x, y, point_size)

    # Add noise
    for _ in range(random.randint(50, 100)):
        nx = random.randint(0, width - point_size)
        ny = random.randint(0, height - point_size)
        draw.ellipse((nx, ny, nx + point_size, ny + point_size), fill="black")

    print("Returning patterns:", used_patterns)  # Debugging statement

    # Return the image as a NumPy array and the list of patterns in the image
    return np.array(image), used_patterns




