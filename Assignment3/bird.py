import os
import random
import shutil
import h5py
import numpy as np
from PIL import Image
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

tf.compat.v1.set_random_seed(2019)
asian_brown_flycatcher_url = './IEMS5780_2022Spring_Assignment3_BirdDataset/Asian Brown Flycatcher/'
blue_rock_thrush_url = './IEMS5780_2022Spring_Assignment3_BirdDataset/Blue Rock Thrush/'
brown_shrike= './IEMS5780_2022Spring_Assignment3_BirdDataset/Brown Shrike/'
grey_faced_buzzard_url = './IEMS5780_2022Spring_Assignment3_BirdDataset/Grey-faced Buzzard/'

id = 0

def filter_gray_image(url):
    global id
    clear_img_list = []
    for fpath, _, fs in os.walk(url):
        for f in fs:
            item = os.path.join(fpath, f)
            img = Image.open(item)
            # Judge whether the image is grayscale image or bird image
            # gray scale image only 1 channel, bird image RGB three channels.
            layers = len(img.split())
            if layers != 1: clear_img_list.append(item)
    random.shuffle(clear_img_list)
    training_set = clear_img_list[:40]
    val_set = clear_img_list[40:50]
    test_set = clear_img_list[50:60]

    # Report id of select images
    training_set_id = [ _ for _ in range(id, id+40)]
    id = id + 40
    val_set_id = [ _ for _ in range(id, id+10)]
    id = id + 10
    test_set_id = [ _ for _ in range(id, id+10)]
    id = id + 10

    return training_set, val_set, test_set, training_set_id, val_set_id, test_set_id


def img_preprocessing():
    bird_type = ["Asian Brown Flycatcher", "Blue Rock Thrush", "Brown Shrike", "Grey-faced Buzzard"]
    bird_img_url = [asian_brown_flycatcher_url, blue_rock_thrush_url, brown_shrike, grey_faced_buzzard_url]
    if not os.path.exists('train'):os.makedirs('train')
    if not os.path.exists('val'):os.makedirs('val')
    if not os.path.exists('test'):os.makedirs('test')

    for _ in bird_type:
        if not os.path.exists('train/'+_): os.makedirs('train/'+_)
        if not os.path.exists('val/'+_): os.makedirs('val/'+_)
        if not os.path.exists('test/'+_): os.makedirs('test/'+_)

    for i in range(4):
        training_set, val_set, test_set, training_set_id, val_set_id, test_set_id = filter_gray_image(bird_img_url[i])
        print("Training set id of {} is: {}".format(bird_img_url[i][:-3], training_set_id))
        print("Validation set id of {} is: {}".format(bird_img_url[i][:-3], val_set_id))
        print("Test set id of {} is: {}".format(bird_img_url[i][:-3], test_set_id))
        for img_src in training_set: shutil.copy(img_src, 'train/'+bird_type[i])
        for img_src in val_set:shutil.copy(img_src, 'val/'+bird_type[i])
        for img_src in test_set:shutil.copy(img_src, 'test/'+bird_type[i])


def process_img_data():
    batch_size = 5
    train_dir = "train/"
    val_dir = "val/"
    test_dir = "test/"

    train_datagen = ImageDataGenerator(rescale=1.0 / 255.)
    val_datagen = ImageDataGenerator(rescale=1.0 / 255.)
    test_datagen = ImageDataGenerator(rescale=1.0 / 255.)

    train_generator = train_datagen.flow_from_directory(train_dir,
                                                        batch_size=batch_size,
                                                        class_mode='categorical',
                                                        target_size=(180, 180))
    validation_generator = val_datagen.flow_from_directory(val_dir,
                                                            batch_size=batch_size,
                                                            class_mode='categorical',
                                                            target_size=(180, 180))

    test_generator = test_datagen.flow_from_directory(test_dir,
                                                      batch_size=batch_size,
                                                      class_mode='categorical',
                                                      target_size=(180,180))

    return train_generator, validation_generator, test_generator

def cnn_model():

    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(16, (3, 3), activation="relu", input_shape=(180, 180, 3)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(550, activation="relu"),  # Adding the Hidden layer
        tf.keras.layers.Dropout(0.1, seed=2019),
        tf.keras.layers.Dense(400, activation="relu"),
        tf.keras.layers.Dropout(0.1, seed=2019),
        tf.keras.layers.Dense(300, activation="relu"),
        tf.keras.layers.Dropout(0.2, seed=2019),
        tf.keras.layers.Dense(200, activation="relu"),
        tf.keras.layers.Dropout(0.2, seed=2019),
        tf.keras.layers.Dense(4, activation="softmax")  # Adding the Output Layer
    ])
    model.summary()
    return model


if __name__ == '__main__':
    img_preprocessing()
    # 1 epoch = BatchSize * iteration
    bs = 10
    model = cnn_model()
    adam = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
    train_generator, validation_generator, test_generator = process_img_data()
    history = model.fit(train_generator,
                        validation_data=validation_generator,
                        steps_per_epoch=200 // bs,
                        epochs=30,
                        validation_steps=100 // bs,
                        verbose=2)


    print("Evaluate on test data")
    score = model.evaluate(test_generator, verbose=2)
    print("test loss, test acc:", score)

    model.save('bird_model.h5')





