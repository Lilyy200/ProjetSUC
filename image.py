import random
from PIL import Image, ImageDraw

def gen_cords(width, height, count, pattern_size):
    max_x = width - pattern_size
    max_y = height - pattern_size
    coords = []
    radius = pattern_size * 2  # Minimum distance between patterns

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
        for i in range(5):  # Number of rows in the triangle
            for j in range(i + 1):
                offset_x = random.randint(-1, 1)  # Slight random offset for realism
                offset_y = random.randint(-1, 1)
                px = x + j * point_size * 2 + offset_x
                py = y + i * point_size * 2 + offset_y
                draw.ellipse((px, py, px + point_size, py + point_size), fill="black")

    elif pattern_type == 'square':
        for i in range(5):
            for j in range(5):
                offset_x = random.randint(-1, 1)
                offset_y = random.randint(-1, 1)
                px = x + i * point_size * 2 + offset_x
                py = y + j * point_size * 2 + offset_y
                draw.ellipse((px, py, px + point_size, py + point_size), fill="black")

    elif pattern_type == 'x':
        for i in range(5):
            offset_x1 = random.randint(-1, 1)
            offset_y1 = random.randint(-1, 1)
            offset_x2 = random.randint(-1, 1)
            offset_y2 = random.randint(-1, 1)
            # Diagonal \
            px1 = x + i * point_size * 2 + offset_x1
            py1 = y + i * point_size * 2 + offset_y1
            draw.ellipse((px1, py1, px1 + point_size, py1 + point_size), fill="black")
            # Diagonal /
            px2 = x + (4 - i) * point_size * 2 + offset_x2
            py2 = y + i * point_size * 2 + offset_y2
            draw.ellipse((px2, py2, px2 + point_size, py2 + point_size), fill="black")

def generate_random_image_with_patterns(width, height, num_patterns):
    # Create a white image
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    coords = gen_cords(width, height, num_patterns, 20)
    
    point_size = 3  # Size of each dot
    patterns = ['triangle', 'square', 'x']
    
    # Add patterns
    for x, y in coords:
        pattern_type = random.choice(patterns)
        draw_pattern(draw, pattern_type, x, y, point_size)
    
    # Add random noise (background dots)
    for _ in range(random.randint(50, 100)):  # Add 50-100 random dots
        nx = random.randint(0, width - point_size)
        ny = random.randint(0, height - point_size)
        draw.ellipse((nx, ny, nx + point_size, ny + point_size), fill="black")
    
    # Display and save the image
    image.show()
    image.save("realistic_mines.png")

# Generate the image
generate_random_image_with_patterns(width=128, height=128, num_patterns=5)
