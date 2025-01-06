import os
from PIL import Image, ImageDraw
import pattern_finder as pf
import mine_field as mf
import mine_field_generator as mfg
import mine_field_drawer as mfd

# Parameters
p_size = 20
output_dir = "V2/test_result/"
training_dir = os.path.join(output_dir, "training")
testing_dir = os.path.join(output_dir, "testing")

# Create directories for training and testing
os.makedirs(training_dir, exist_ok=True)
os.makedirs(testing_dir, exist_ok=True)

# Generate minefield and image
field = mfg.gen_mine_field(pattern_count=6, pattern_size=p_size)
image = mfd.to_image(field)

# Extract green rectangles (patterns in the field)
for i, pattern in enumerate(field.patterns):
    xy1 = (pattern.offset_x, pattern.offset_y)
    xy2 = (xy1[0] + pattern.pattern_size, xy1[1] + pattern.pattern_size)
    cropped_image = image.crop((*xy1, *xy2))
    cropped_image.save(os.path.join(training_dir, f"green_{i}.png"))

# Extract red rectangles (patterns found by pattern finder)
for i, xy1 in enumerate(pf.find_pattern(field)):
    xy2 = (xy1[0] + p_size, xy1[1] + p_size)
    cropped_image = image.crop((*xy1, *xy2))
    cropped_image.save(os.path.join(testing_dir, f"red_{i}.png"))

print(f"Extracted rectangles saved to {output_dir}")
