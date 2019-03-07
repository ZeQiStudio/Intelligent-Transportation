import os
import numpy as np
import config
from PIL import Image

#SIZE = config.SIZE
WIDTH = config.WIDTH
HEIGHT = config.HEIGHT


def cul_file_sum(path, NUM_CLASSES):
    count = 0
    for i in range(0, NUM_CLASSES):
        dir = os.path.join(path, str(i))
        for rt, dirs, files in os.walk(dir):
            for filename in files:
                count += 1
    images = np.zeros((count, HEIGHT, WIDTH))
    labels = np.zeros((count, NUM_CLASSES))
    return count, images, labels


def gener_img_lbls(path, images, labels, NUM_CLASSES):
    index = 0
    for i in range(0, NUM_CLASSES):
        dir = os.path.join(path, str(i))
        for rt, dirs, files in os.walk(dir):
            for filename in files:
                filename = dir + '/' + filename
                img = Image.open(filename)
                width = img.size[0]
                height = img.size[1]
                for h in range(0, height):
                    for w in range(0, width):
                        if img.getpixel((w, h)) > 230:
                            # images[index][w + h * width] = 0
                            images[index][h][w] = 0
                        else:
                            # images[index][w + h * width] = 1
                            images[index][h][w] = 1
                labels[index][i] = 1
                index += 1
    images = images.reshape((-1, HEIGHT, WIDTH, 1))
    return images, labels
