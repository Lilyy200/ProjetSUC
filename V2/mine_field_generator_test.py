import mine_field_generator
import mine_field_drawer

for i in range(5):
    mf = mine_field_generator.gen_mine_field()
    image = mine_field_drawer.to_image(mf)
    image.save(f'V2/test_result/mine_field_generator_test_{i}.png')