import tensorflow as tf
import config
CONV1_SIZE = config.CONV1_SIZE
CONV2_SIZE = config.CONV2_SIZE
CHANNEL_NUM = config.CHANNEL_NUM
CONV2_DEEP = config.CONV2_DEEP
CONV1_DEEP = config.CONV1_DEEP
FC1_SIZE = config.FC1_SIZE



def inference(input_tensor, train, regularizer,NUM_CLASSES):
    with tf.variable_scope('layer1-conv1'):
        conv1_weights = tf.get_variable('weight', [CONV1_SIZE, CONV1_SIZE, CHANNEL_NUM, CONV1_DEEP],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1_bias = tf.get_variable('bias', [CONV1_DEEP], initializer=tf.constant_initializer(0.0))
        conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_bias))

    with tf.variable_scope('layer2-pool1'):
        pool1 = tf.nn.max_pool(relu1, [1, 2, 2, 1], [1, 2, 2, 1], padding='SAME')

    with tf.variable_scope('layer3-conv2'):
        conv2_weights = tf.get_variable('weight', [CONV2_SIZE, CONV2_SIZE, CONV1_DEEP, CONV2_DEEP],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv2_bias = tf.get_variable('bias', [CONV2_DEEP], initializer=tf.constant_initializer(0.0))
        conv2 = tf.nn.conv2d(pool1, conv2_weights, strides=[1, 1, 1, 1], padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_bias))

    with tf.variable_scope('layer4-pool2'):
        pool2 = tf.nn.max_pool(relu2, [1, 1, 1, 1], [1, 1, 1, 1], padding='SAME')

    pool_shape = pool2.get_shape().as_list()
    nodes = pool_shape[1] * pool_shape[2] * pool_shape[3]

    reshaped = tf.reshape(pool2, [-1, nodes])

    with tf.variable_scope('layer5-fc1'):
        fc1_weigths = tf.get_variable('weight', [nodes, FC1_SIZE],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        ## regularization
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc1_weigths))

        fc1_bias = tf.get_variable('bias', [FC1_SIZE], initializer=tf.constant_initializer(0.0))
        fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_weigths) + fc1_bias)
        if train:
            fc1 = tf.nn.dropout(fc1, 0.5)

    with tf.variable_scope('layer6-fc2'):
        fc2_weigths = tf.get_variable('weight', [FC1_SIZE, NUM_CLASSES],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        ## regularization
        if regularizer != None:
            tf.add_to_collection('losses', regularizer(fc2_weigths))

        fc2_bias = tf.get_variable('bias', [NUM_CLASSES], initializer=tf.constant_initializer(0.0))
        logit = tf.matmul(fc1, fc2_weigths) + fc2_bias

        return logit
