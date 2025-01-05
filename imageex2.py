import random
from PIL import Image, ImageDraw
import numpy as np

def gen_cords(width, height, count, min_distance):
    """
    Generate non-overlapping coordinates for placing patterns or noise points.
    """
    coords = []
    while len(coords) < count:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # Ensure minimum distance between points
        if all(((x - cx)**2 + (y - cy)**2)**0.5 >= min_distance for cx, cy in coords):
            coords.append((x, y))
    return coords


def draw_pattern(draw, pattern_type, x, y, point_size=3):
    """
    Draw a specific pattern type (triangle, square, x) at a given location.
    """
    if pattern_type == 'triangle':
        for i in range(5):  # Triangle: rows of points
            for j in range(i + 1):
                px = x + j * point_size * 2
                py = y + i * point_size * 2
                draw.ellipse((px - 1, py - 1, px + 1, py + 1), fill="black")

    elif pattern_type == 'square':
        for i in range(5):  # Square: grid of points
            for j in range(5):
                px = x + i * point_size * 2
                py = y + j * point_size * 2
                draw.ellipse((px - 1, py - 1, px + 1, py + 1), fill="black")

    elif pattern_type == 'x':
        for i in range(5):  # X: two diagonals
            px1 = x + i * point_size * 2
            py1 = y + i * point_size * 2
            draw.ellipse((px1 - 1, py1 - 1, px1 + 1, py1 + 1), fill="black")

            px2 = x + (4 - i) * point_size * 2
            py2 = y + i * point_size * 2
            draw.ellipse((px2 - 1, py2 - 1, px2 + 1, py2 + 1), fill="black")


def generate_image_with_bombs(width, height, num_patterns, num_noise_points):
    """
    Generate an image with patterns and random noise points (all points are 'bombs').
    - Patterns are placed at specific locations.
    - Noise points are scattered randomly.
    """
    # Create a blank white image
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    patterns = ['triangle', 'square', 'x']
    annotations = []

    # Generate and draw patterns
    pattern_coords = gen_cords(width, height, num_patterns, min_distance=20)
    for x, y in pattern_coords:
        pattern_type = random.choice(patterns)  # Randomly choose a pattern type
        draw_pattern(draw, pattern_type, x, y, point_size=3)
        annotations.append({"type": pattern_type, "coords": (x, y)})

    # Generate and draw random noise points
    noise_coords = gen_cords(width, height, num_noise_points, min_distance=5)
    for x, y in noise_coords:
        draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill="black")
        annotations.append({"type": "noise", "coords": (x, y)})

    return np.array(image), annotations


def create_bomb_dataset(num_images, width, height, num_patterns, num_noise_points):
    """
    Generate a dataset of images and annotations.
    - num_images: Number of images to generate.
    - num_patterns: Number of patterns in each image.
    - num_noise_points: Number of random noise points in each image.
    """
    X = []
    y = []

    for _ in range(num_images):
        # Generate image and annotations
        img, annotations = generate_image_with_bombs(width, height, num_patterns, num_noise_points)
        X.append(img)

        # Convert annotations to a simplified format: [x1, y1, x2, y2, ...]
        bombs = [ann["coords"] for ann in annotations]
        y.append(bombs)

    return np.array(X), y
