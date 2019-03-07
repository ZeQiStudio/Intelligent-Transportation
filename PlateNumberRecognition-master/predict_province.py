import tensorflow as tf
import os
import config
from PIL import Image
import numpy as np

NUM_CLASSES=config.PROVINCE_NUM_CLASSES
SAVER_DIR=config.PROVINCE_SAVER_DIR
saver=tf.train.import_meta_graph(os.path.join(SAVER_DIR,'model.ckpt.meta'))
HEIGHT=config.HEIGHT
WIDTH=config.WIDTH
CHANNEL_NUM=config.CHANNEL_NUM
x=tf.placeholder(tf.float32,shape=[None,HEIGHT,WIDTH,CHANNEL_NUM])
SIZE=config.SIZE
PROVINCES=config.PROVINCES
nProvinceIndex = 0

with tf.Session() as sess:
    model_file=tf.train.latest_checkpoint(SAVER_DIR)
    saver.restore(sess, model_file)
    conv1_w=sess.graph.get_tensor_by_name('layer1-conv1/weight:0')
    conv1_b=sess.graph.get_tensor_by_name('layer1-conv1/bias:0')

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

    fc2_w=sess.graph.get_tensor_by_name('layer6-fc2/weight:0')
    fc2_b=sess.graph.get_tensor_by_name('layer6-fc2/bias:0')

    result=tf.nn.softmax(tf.matmul(fc1, fc2_w) + fc2_b)

    img_data = np.zeros((5,HEIGHT,WIDTH))
    path = "tf_car_license_dataset/test_images/1510076213_454_1.bmp" 
    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    for h in range(0, height):
        for w in range(0, width):
            if img.getpixel((w, h)) < 190:
                img_data[0][h][w] = 1
            else:
                img_data[0][h][w] = 0

    img_data=np.reshape(img_data,[5,HEIGHT,WIDTH,CHANNEL_NUM])
    result = sess.run(result, feed_dict={x: np.array(img_data)})

    max1 = 0
    max2 = 0
    max3 = 0
    max1_index = 0
    max2_index = 0
    max3_index = 0

    for j in range(NUM_CLASSES):
        if result[0][j] > max1:
            max1 = result[0][j]
            max1_index = j
            continue
        if (result[0][j] > max2) and (result[0][j] <= max1):
            max2 = result[0][j]
            max2_index = j
            continue
        if (result[0][j] > max3) and (result[0][j] <= max2):
            max3 = result[0][j]
            max3_index = j
            continue
    nProvinceIndex = max1_index
    print ("概率：  [%s %0.2f%%]    [%s %0.2f%%]    [%s %0.2f%%]" % (PROVINCES[max1_index],max1*100, PROVINCES[max2_index],max2*100, PROVINCES[max3_index],max3*100))
            
    print ("省份简称是: %s" % PROVINCES[nProvinceIndex])

