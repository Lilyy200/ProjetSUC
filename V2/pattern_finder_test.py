import pattern_finder as pf
import mine_field as mf
import mine_field_generator as mfg
import mine_field_drawer as mfd

from PIL import ImageDraw

p_size = 20
field = mfg.gen_mine_field(pattern_count=5, pattern_size=p_size)
image = mfd.to_image(field).convert('RGB')
draw = ImageDraw.Draw(image)

for pattern in field.patterns:
    xy1 = (pattern.offset_x - 1, pattern.offset_y - 1)
    xy2 = (xy1[0] + pattern.pattern_size + 2, xy1[1] + pattern.pattern_size + 2)
    draw.rectangle(xy=(xy1, xy2), outline='green')

image2 = image.convert('RGB')
draw2 = ImageDraw.Draw(image2)

for xy1 in pf.find_pattern(field):
    xy1 = (xy1[0] - 1, xy1[1] - 1)
    xy2 = (xy1[0] + p_size + 2, xy1[1] + p_size + 2)
    draw.rectangle(xy=(xy1, xy2), outline='red')

for xy1, xy2 in pf.find_pattern(field, resize=False):
    xy1 = (xy1[0] - 1, xy1[1] - 1)
    xy2 = (xy2[0] + 1, xy2[1] + 1)
    draw2.rectangle(xy=(xy1, xy2), outline='red')

image.save('V2/test_result/pattern_finder_test.png')
image2.save('V2/test_result/pattern_finder_test_before_resize.png')