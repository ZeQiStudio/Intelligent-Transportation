import os
import time
import inference
import tensorflow as tf
import pic_reader
import config
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

SIZE = config.SIZE
WIDTH = config.WIDTH
HEIGHT = config.HEIGHT
NUM_CLASSES = config.PROVINCE_NUM_CLASSES
iterations = config.iterations
batch_size = config.batch_size
LEARNING_RATE_BASE = config.LEARNING_RATE_BASE
LEARNING_RATE_DECAY = config.LEARNING_RATE_DECAY
REGULARIZATION_RATE = config.REGULARIZATION_RATE
MOVING_AVERAGE_DECAY = config.MOVING_AVERAGE_DECAY

SAVER_DIR = config.PROVINCE_SAVER_DIR
time_begin = time.time()

# 定义输入节点，对应于图片像素值矩阵集合和图片标签(即所代表的数字)
x = tf.placeholder(tf.float32, shape=[None, HEIGHT, WIDTH, 1])
y_ = tf.placeholder(tf.float32, shape=[None, NUM_CLASSES])

x_image = tf.reshape(x, [-1, WIDTH, HEIGHT, 1])

input_dir = './tf_car_license_dataset/train_images/training-set/chinese-characters/'
input_sum, input_images, input_labels = pic_reader.cul_file_sum(input_dir,NUM_CLASSES)
input_images, input_labels = pic_reader.gener_img_lbls(input_dir, input_images, input_labels,NUM_CLASSES)

valid_dir = './tf_car_license_dataset/train_images/validation-set/chinese-characters/'
valid_sum, valid_images, valid_labels = pic_reader.cul_file_sum(valid_dir,NUM_CLASSES)
valid_images, valid_labels = pic_reader.gener_img_lbls(valid_dir, valid_images, valid_labels,NUM_CLASSES)

time_elapsed = time.time() - time_begin
print("读取图片文件耗费时间：%d秒" % time_elapsed)

logits = inference.inference(x_image, True, None, NUM_CLASSES)
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_, logits=logits))
global_step = tf.Variable(0, trainable=False)

learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, input_sum / batch_size, LEARNING_RATE_DECAY)
train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    tf.global_variables_initializer().run()

    time_begin = time.time()

    print("一共读取了 %s 个训练图像， %s 个标签" % (input_sum, input_sum))

    # 设置每次训练op的输入个数和迭代次数，这里为了支持任意图片总数，定义了一个余数remainder，譬如，如果每次训练op的输入个数为60，图片总数为150张，则前面两次各输入60张，最后一次输入30张（余数30）

    batches_count = int(input_sum / batch_size)
    remainder = input_sum % batch_size
    print("训练数据集分成 %s 批, 前面每批 %s 个数据，最后一批 %s 个数据" % (batches_count + 1, batch_size, remainder))

    # 执行训练迭代
    for it in range(1000):
        for n in range(batches_count):
            train_step.run(feed_dict={x: input_images[n * batch_size:(n + 1) * batch_size],
                                      y_: input_labels[n * batch_size:(n + 1) * batch_size]})
        if remainder > 0:
            start_index = batches_count * batch_size;
            train_step.run(
                feed_dict={x: input_images[start_index:input_sum - 1], y_: input_labels[start_index:input_sum - 1]})

        # 每完成五次迭代，判断准确度是否已达到100%，达到则退出迭代循环
        iterate_accuracy = 0
        if it % 5 == 0:
            iterate_accuracy = accuracy.eval(feed_dict={x: valid_images, y_: valid_labels})
            print('第 %d 次训练迭代: 准确率 %0.5f%%' % (it, iterate_accuracy * 100))
            if iterate_accuracy >= 0.9999 or it >= iterations:
                break;

    print('完成训练!')
    time_elapsed = time.time() - time_begin
    print("训练耗费时间：%d秒" % time_elapsed)
    time_begin = time.time()

    # 保存训练结果
    if not os.path.exists(SAVER_DIR):
        print('不存在训练数据保存目录，现在创建保存目录')
        os.makedirs(SAVER_DIR)
    # 初始化saver
    saver = tf.train.Saver()
    saver_path = saver.save(sess, "%smodel.ckpt" % (SAVER_DIR))
