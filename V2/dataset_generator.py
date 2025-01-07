import mine_field_generator
import mine_field_drawer
import pattern_finder
from pattern_finder import find_pattern

def create_dataset(num_mf=1000, pattern_size=20, do_test=True, do_train=True):
    train_dataset = []
    test_dataset = []

    for i in range(num_mf):
        mf = mine_field_generator.gen_mine_field()
        image = mine_field_drawer.to_image(mf)

        if do_train:
            for pattern in mf.patterns: 
                xy1 = (pattern.offset_x , pattern.offset_y )
                xy2 = (xy1[0] + pattern.pattern_size, xy1[1] + pattern.pattern_size)
                cropped_image = image.crop((xy1[0], xy1[1], xy2[0], xy2[1]))
                train_dataset.append((cropped_image, pattern.type))

        if do_test:
            for xy1 in pattern_finder.find_pattern(mf):
                xy2 = (xy1[0] + pattern_size, xy1[1] + pattern_size)
                pattern_image = image.crop((xy1[0], xy1[1], xy2[0], xy2[1]))
                test_dataset.append(pattern_image)

    return train_dataset, test_dataset

