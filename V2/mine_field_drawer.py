import mine_field as mf
from PIL import Image, ImageDraw

def to_image(mf: mf.MineField) -> Image:
    image = Image.new("RGB", (mf.max_x, mf.max_y), "white")
    draw = ImageDraw.Draw(image)

    for point in mf.points():
        x = point.x
        y = point.y
        draw.ellipse((x, y, x + 2, y + 2), fill="black")

    return image.convert("L")
