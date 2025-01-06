import pattern_finder as pf
import mine_field as mf
import mine_field_generator as mfg
import mine_field_drawer as mfd

from PIL import ImageDraw

field = mfg.gen_mine_field(pattern_count=6)
image = mfd.to_image(field)
labels = pf.find_pattern(field)
draw = ImageDraw.Draw(image)

for pattern in field.patterns:
    xy1 = (pattern.offset_x - 1, pattern.offset_y - 1)
    xy2 = (xy1[0] + pattern.pattern_size + 2, xy1[1] + pattern.pattern_size + 2)
    draw.rectangle(xy=(xy1, xy2), outline='green')

xys = [[(field.max_x, field.max_y),(0, 0)] for _ in range(max(labels) + 1)]

for label, point in zip(labels, field.points()):
    if label == -1:
        continue

    xy = xys[label]
    xy[0] = (min(point.x, xy[0][0]), min(point.y, xy[0][1]))
    xy[1] = (max(point.x, xy[1][0]), max(point.y, xy[1][1]))

for xy in xys:
    print(xy)
    draw.rectangle(xy=xy, outline='red')

image.save('V2/test_result/pattern_finder_test.png')
