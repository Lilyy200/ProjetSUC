import dataset_generator as db_gen
import numpy as np
import mine_field as mf
import mine_field_drawer as mfd
import pattern_finder as pf
from keras.src.models import Sequential
from keras.src.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.src.callbacks import EarlyStopping
from PIL import ImageDraw

def get_trained_model(nb_field=1000):
    train, _ = db_gen.create_dataset(num_mf=nb_field, do_test=False)

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(20, 20, 1)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(5, activation='softmax')  # Assuming 10 classes for classification
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    X_train = np.array([np.array(img[0]) == 0 for img in train], dtype=bool).astype(int)
    Y_train = np.array([img[1].value -1 for img in train])
    
    early_stopping = EarlyStopping(
        monitor='val_loss',   # Monitor validation loss (or 'val_accuracy')
        patience=3,           # Stop after 3 epochs of no improvement
        restore_best_weights=True,  # Restore model weights from the best epoch
        verbose=1             # Print a message when stopping
    )

    model.fit(X_train, Y_train, epochs=10, batch_size=32, validation_split=0.2,callbacks=[early_stopping])
    return model

def find_pattern(model, field: mf.MineField):
    image = mfd.to_image(field)
    scale = 4
    image_rgb = image.resize((field.max_x * scale, field.max_y * scale)).convert('RGB')
    draw = ImageDraw.Draw(image_rgb)
    p_size = field.pattern_size

    for pattern in field.patterns:
        xy1 = (pattern.offset_x - 1, pattern.offset_y - 1)
        xy2 = (xy1[0] + pattern.pattern_size + 2, xy1[1] + pattern.pattern_size + 2)
        draw.rectangle(xy=(tuple(v*scale for v in xy1), tuple(v*scale for v in xy2)), outline='green', width=scale)

    for xy1 in pf.find_pattern(field):
        xy1 = (xy1[0] - 1, xy1[1] - 1)
        xy2 = (xy1[0] + p_size + 2, xy1[1] + p_size + 2)
        pattern_img = image.crop((xy1[0] + 1, xy1[1] + 1, xy2[0] - 2, xy2[1] - 2))
        x = np.array(np.array([pattern_img]) == 0)
        y = model.predict(x)
        shape = mf.MinePatternType(np.argmax(y) + 1)
        draw.rectangle(xy=(tuple(v*scale for v in xy1), tuple(v*scale for v in xy2)), outline='red', width=scale)
        tx = (xy2[0] + 3) * scale
        ty = ((xy1[1] + xy2[1]) * scale) // 2
        draw.text(xy=(tx, ty), text=f'{shape.name} ({int(np.max(y) * 100)}%)',  fill='red')
        
    return image_rgb