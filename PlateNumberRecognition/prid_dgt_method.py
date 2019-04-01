import tensorflow as tf
import os
import config
import numpy as np
import cv2


def prid_digit(img):
    NUM_CLASSES = config.DIGITS_NUM_CLASSES
    SAVER_DIR = config.DIGITS_SAVER_DIR
    saver = tf.train.import_meta_graph(os.path.join(SAVER_DIR, 'model.ckpt.meta'))
    HEIGHT = config.HEIGHT
    WIDTH = config.WIDTH
    CHANNEL_NUM = config.CHANNEL_NUM
    LETTERS_DIGITS = config.LETTERS_DIGITS
    license_digit = ''
    x = tf.placeholder(tf.float32, shape=[None, HEIGHT, WIDTH, CHANNEL_NUM])
    with tf.Session() as sess:
        model_file = tf.train.latest_checkpoint(SAVER_DIR)
        saver.restore(sess, model_file)
        conv1_w = sess.graph.get_tensor_by_name('layer1-conv1/weight:0')
        conv1_b = sess.graph.get_tensor_by_name('layer1-conv1/bias:0')

        conv1 = tf.nn.conv2d(x, conv1_w, strides=[1, 1, 1, 1], padding='SAME')
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_b))
        pool1 = tf.nn.max_pool(relu1, [1, 2, 2, 1], [1, 2, 2, 1], padding='SAME')

        # 第二个卷积层
        conv2_w = sess.graph.get_tensor_by_name('layer3-conv2/weight:0')
        conv2_b = sess.graph.get_tensor_by_name('layer3-conv2/bias:0')
        conv2 = tf.nn.conv2d(pool1, conv2_w, strides=[1, 1, 1, 1], padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_b))
        pool2 = tf.nn.max_pool(relu2, [1, 1, 1, 1], [1, 1, 1, 1], padding='SAME')

        # 全连接层
        fc1_w = sess.graph.get_tensor_by_name('layer5-fc1/weight:0')
        fc1_b = sess.graph.get_tensor_by_name('layer5-fc1/bias:0')
        pool_shape = pool2.get_shape().as_list()
        nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]

        reshaped = tf.reshape(pool2, [-1, nodes])
        fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_w) + fc1_b)

        fc2_w = sess.graph.get_tensor_by_name('layer6-fc2/weight:0')
        fc2_b = sess.graph.get_tensor_by_name('layer6-fc2/bias:0')

        result = tf.nn.softmax(tf.matmul(fc1, fc2_w) + fc2_b)
        img_grp_data=np.zeros((6,HEIGHT,WIDTH))
        for i in range(0,6):
            _, img_b = cv2.threshold(img[i], 190, 255, cv2.THRESH_BINARY_INV)
            img_grp_data[i]=img_b

        img_data = np.reshape(img_grp_data, [6, HEIGHT, WIDTH, CHANNEL_NUM])
        result = sess.run(result, feed_dict={x: np.array(img_data)})

        for i in range(6):
            max = 0
            max_index = 0
            for j in range(NUM_CLASSES):
                if result[i][j] > max:
                    max = result[i][j]
                    max_index = j
            license_digit += LETTERS_DIGITS[max_index]
    return license_digit
