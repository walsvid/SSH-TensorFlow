import tensorflow as tf
from networks.network import Network


class Resnet101(Network):
    def __init__(self, is_train):
        super().__init__(is_train)
        self.inputs = []
        self.data = tf.placeholder(tf.float32, shape=[None, None, None, 3], name='data')
        self.im_info = tf.placeholder(tf.float32, shape=[None, 3], name='im_info')
        self.gt_boxes = tf.placeholder(tf.float32, shape=[None, 5], name='gt_boxes')
        # self.gt_ishard = tf.placeholder(tf.int32, shape=[None], name='gt_ishard')
        # self.dontcare_areas = tf.placeholder(tf.float32, shape=[None, 4], name='dontcare_areas')

        self.n_classes = 21
        self.feat_stride = [16, ]
        self.anchor_scales = [8, 16, 32]

        self.keep_prob = tf.placeholder(tf.float32)
        self.layers = dict({'data': self.data, 'im_info': self.im_info, 'gt_boxes': self.gt_boxes})

    def setup(self):
        (self.feed('data')
         .conv(7, 7, 64, 2, 2, biased=False, relu=False, name='conv1')
         .batch_normalization(relu=True, name='bn_conv1', is_training=False)
         .max_pool(3, 3, 2, 2, padding='VALID', name='pool1')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res2a_branch1')
         .batch_normalization(name='bn2a_branch1', is_training=False, relu=False))

        (self.feed('pool1')
         .conv(1, 1, 64, 1, 1, biased=False, relu=False, name='res2a_branch2a')
         .batch_normalization(relu=True, name='bn2a_branch2a', is_training=False)
         .conv(3, 3, 64, 1, 1, biased=False, relu=False, name='res2a_branch2b')
         .batch_normalization(relu=True, name='bn2a_branch2b', is_training=False)
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res2a_branch2c')
         .batch_normalization(name='bn2a_branch2c', is_training=False, relu=False))

        (self.feed('bn2a_branch1',
                   'bn2a_branch2c')
         .add(name='res2a')
         .relu(name='res2a_relu')
         .conv(1, 1, 64, 1, 1, biased=False, relu=False, name='res2b_branch2a')
         .batch_normalization(relu=True, name='bn2b_branch2a', is_training=False)
         .conv(3, 3, 64, 1, 1, biased=False, relu=False, name='res2b_branch2b')
         .batch_normalization(relu=True, name='bn2b_branch2b', is_training=False)
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res2b_branch2c')
         .batch_normalization(name='bn2b_branch2c', is_training=False, relu=False))

        (self.feed('res2a_relu',
                   'bn2b_branch2c')
         .add(name='res2b')
         .relu(name='res2b_relu')
         .conv(1, 1, 64, 1, 1, biased=False, relu=False, name='res2c_branch2a')
         .batch_normalization(relu=True, name='bn2c_branch2a', is_training=False)
         .conv(3, 3, 64, 1, 1, biased=False, relu=False, name='res2c_branch2b')
         .batch_normalization(relu=True, name='bn2c_branch2b', is_training=False)
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res2c_branch2c')
         .batch_normalization(name='bn2c_branch2c', is_training=False, relu=False))

        (self.feed('res2b_relu',
                   'bn2c_branch2c')
         .add(name='res2c')
         .relu(name='res2c_relu')
         .conv(1, 1, 512, 2, 2, biased=False, relu=False, name='res3a_branch1', padding='VALID')
         .batch_normalization(name='bn3a_branch1', is_training=False, relu=False))

        (self.feed('res2c_relu')
         .conv(1, 1, 128, 2, 2, biased=False, relu=False, name='res3a_branch2a', padding='VALID')
         .batch_normalization(relu=True, name='bn3a_branch2a', is_training=False)
         .conv(3, 3, 128, 1, 1, biased=False, relu=False, name='res3a_branch2b')
         .batch_normalization(relu=True, name='bn3a_branch2b', is_training=False)
         .conv(1, 1, 512, 1, 1, biased=False, relu=False, name='res3a_branch2c')
         .batch_normalization(name='bn3a_branch2c', is_training=False, relu=False))

        (self.feed('bn3a_branch1',
                   'bn3a_branch2c')
         .add(name='res3a')
         .relu(name='res3a_relu')
         .conv(1, 1, 128, 1, 1, biased=False, relu=False, name='res3b1_branch2a')
         .batch_normalization(relu=True, name='bn3b1_branch2a', is_training=False)
         .conv(3, 3, 128, 1, 1, biased=False, relu=False, name='res3b1_branch2b')
         .batch_normalization(relu=True, name='bn3b1_branch2b', is_training=False)
         .conv(1, 1, 512, 1, 1, biased=False, relu=False, name='res3b1_branch2c')
         .batch_normalization(name='bn3b1_branch2c', is_training=False, relu=False))

        (self.feed('res3a_relu',
                   'bn3b1_branch2c')
         .add(name='res3b1')
         .relu(name='res3b1_relu')
         .conv(1, 1, 128, 1, 1, biased=False, relu=False, name='res3b2_branch2a')
         .batch_normalization(relu=True, name='bn3b2_branch2a', is_training=False)
         .conv(3, 3, 128, 1, 1, biased=False, relu=False, name='res3b2_branch2b')
         .batch_normalization(relu=True, name='bn3b2_branch2b', is_training=False)
         .conv(1, 1, 512, 1, 1, biased=False, relu=False, name='res3b2_branch2c')
         .batch_normalization(name='bn3b2_branch2c', is_training=False, relu=False))

        (self.feed('res3b1_relu',
                   'bn3b2_branch2c')
         .add(name='res3b2')
         .relu(name='res3b2_relu')
         .conv(1, 1, 128, 1, 1, biased=False, relu=False, name='res3b3_branch2a')
         .batch_normalization(relu=True, name='bn3b3_branch2a', is_training=False)
         .conv(3, 3, 128, 1, 1, biased=False, relu=False, name='res3b3_branch2b')
         .batch_normalization(relu=True, name='bn3b3_branch2b', is_training=False)
         .conv(1, 1, 512, 1, 1, biased=False, relu=False, name='res3b3_branch2c')
         .batch_normalization(name='bn3b3_branch2c', is_training=False, relu=False))

        (self.feed('res3b2_relu',
                   'bn3b3_branch2c')
         .add(name='res3b3')
         .relu(name='res3b3_relu')
         .conv(1, 1, 1024, 2, 2, biased=False, relu=False, name='res4a_branch1', padding='VALID')
         .batch_normalization(name='bn4a_branch1', is_training=False, relu=False))

        (self.feed('res3b3_relu')
         .conv(1, 1, 256, 2, 2, biased=False, relu=False, name='res4a_branch2a', padding='VALID')
         .batch_normalization(relu=True, name='bn4a_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4a_branch2b')
         .batch_normalization(relu=True, name='bn4a_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4a_branch2c')
         .batch_normalization(name='bn4a_branch2c', is_training=False, relu=False))

        (self.feed('bn4a_branch1',
                   'bn4a_branch2c')
         .add(name='res4a')
         .relu(name='res4a_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b1_branch2a')
         .batch_normalization(relu=True, name='bn4b1_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b1_branch2b')
         .batch_normalization(relu=True, name='bn4b1_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b1_branch2c')
         .batch_normalization(name='bn4b1_branch2c', is_training=False, relu=False))

        (self.feed('res4a_relu',
                   'bn4b1_branch2c')
         .add(name='res4b1')
         .relu(name='res4b1_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b2_branch2a')
         .batch_normalization(relu=True, name='bn4b2_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b2_branch2b')
         .batch_normalization(relu=True, name='bn4b2_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b2_branch2c')
         .batch_normalization(name='bn4b2_branch2c', is_training=False, relu=False))

        (self.feed('res4b1_relu',
                   'bn4b2_branch2c')
         .add(name='res4b2')
         .relu(name='res4b2_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b3_branch2a')
         .batch_normalization(relu=True, name='bn4b3_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b3_branch2b')
         .batch_normalization(relu=True, name='bn4b3_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b3_branch2c')
         .batch_normalization(name='bn4b3_branch2c', is_training=False, relu=False))

        (self.feed('res4b2_relu',
                   'bn4b3_branch2c')
         .add(name='res4b3')
         .relu(name='res4b3_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b4_branch2a')
         .batch_normalization(relu=True, name='bn4b4_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b4_branch2b')
         .batch_normalization(relu=True, name='bn4b4_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b4_branch2c')
         .batch_normalization(name='bn4b4_branch2c', is_training=False, relu=False))

        (self.feed('res4b3_relu',
                   'bn4b4_branch2c')
         .add(name='res4b4')
         .relu(name='res4b4_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b5_branch2a')
         .batch_normalization(relu=True, name='bn4b5_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b5_branch2b')
         .batch_normalization(relu=True, name='bn4b5_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b5_branch2c')
         .batch_normalization(name='bn4b5_branch2c', is_training=False, relu=False))

        (self.feed('res4b4_relu',
                   'bn4b5_branch2c')
         .add(name='res4b5')
         .relu(name='res4b5_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b6_branch2a')
         .batch_normalization(relu=True, name='bn4b6_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b6_branch2b')
         .batch_normalization(relu=True, name='bn4b6_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b6_branch2c')
         .batch_normalization(name='bn4b6_branch2c', is_training=False, relu=False))

        (self.feed('res4b5_relu',
                   'bn4b6_branch2c')
         .add(name='res4b6')
         .relu(name='res4b6_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b7_branch2a')
         .batch_normalization(relu=True, name='bn4b7_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b7_branch2b')
         .batch_normalization(relu=True, name='bn4b7_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b7_branch2c')
         .batch_normalization(name='bn4b7_branch2c', is_training=False, relu=False))

        (self.feed('res4b6_relu',
                   'bn4b7_branch2c')
         .add(name='res4b7')
         .relu(name='res4b7_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b8_branch2a')
         .batch_normalization(relu=True, name='bn4b8_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b8_branch2b')
         .batch_normalization(relu=True, name='bn4b8_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b8_branch2c')
         .batch_normalization(name='bn4b8_branch2c', is_training=False, relu=False))

        (self.feed('res4b7_relu',
                   'bn4b8_branch2c')
         .add(name='res4b8')
         .relu(name='res4b8_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b9_branch2a')
         .batch_normalization(relu=True, name='bn4b9_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b9_branch2b')
         .batch_normalization(relu=True, name='bn4b9_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b9_branch2c')
         .batch_normalization(name='bn4b9_branch2c', is_training=False, relu=False))

        (self.feed('res4b8_relu',
                   'bn4b9_branch2c')
         .add(name='res4b9')
         .relu(name='res4b9_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b10_branch2a')
         .batch_normalization(relu=True, name='bn4b10_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b10_branch2b')
         .batch_normalization(relu=True, name='bn4b10_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b10_branch2c')
         .batch_normalization(name='bn4b10_branch2c', is_training=False, relu=False))

        (self.feed('res4b9_relu',
                   'bn4b10_branch2c')
         .add(name='res4b10')
         .relu(name='res4b10_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b11_branch2a')
         .batch_normalization(relu=True, name='bn4b11_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b11_branch2b')
         .batch_normalization(relu=True, name='bn4b11_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b11_branch2c')
         .batch_normalization(name='bn4b11_branch2c', is_training=False, relu=False))

        (self.feed('res4b10_relu',
                   'bn4b11_branch2c')
         .add(name='res4b11')
         .relu(name='res4b11_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b12_branch2a')
         .batch_normalization(relu=True, name='bn4b12_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b12_branch2b')
         .batch_normalization(relu=True, name='bn4b12_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b12_branch2c')
         .batch_normalization(name='bn4b12_branch2c', is_training=False, relu=False))

        (self.feed('res4b11_relu',
                   'bn4b12_branch2c')
         .add(name='res4b12')
         .relu(name='res4b12_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b13_branch2a')
         .batch_normalization(relu=True, name='bn4b13_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b13_branch2b')
         .batch_normalization(relu=True, name='bn4b13_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b13_branch2c')
         .batch_normalization(name='bn4b13_branch2c', is_training=False, relu=False))

        (self.feed('res4b12_relu',
                   'bn4b13_branch2c')
         .add(name='res4b13')
         .relu(name='res4b13_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b14_branch2a')
         .batch_normalization(relu=True, name='bn4b14_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b14_branch2b')
         .batch_normalization(relu=True, name='bn4b14_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b14_branch2c')
         .batch_normalization(name='bn4b14_branch2c', is_training=False, relu=False))

        (self.feed('res4b13_relu',
                   'bn4b14_branch2c')
         .add(name='res4b14')
         .relu(name='res4b14_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b15_branch2a')
         .batch_normalization(relu=True, name='bn4b15_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b15_branch2b')
         .batch_normalization(relu=True, name='bn4b15_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b15_branch2c')
         .batch_normalization(name='bn4b15_branch2c', is_training=False, relu=False))

        (self.feed('res4b14_relu',
                   'bn4b15_branch2c')
         .add(name='res4b15')
         .relu(name='res4b15_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b16_branch2a')
         .batch_normalization(relu=True, name='bn4b16_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b16_branch2b')
         .batch_normalization(relu=True, name='bn4b16_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b16_branch2c')
         .batch_normalization(name='bn4b16_branch2c', is_training=False, relu=False))

        (self.feed('res4b15_relu',
                   'bn4b16_branch2c')
         .add(name='res4b16')
         .relu(name='res4b16_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b17_branch2a')
         .batch_normalization(relu=True, name='bn4b17_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b17_branch2b')
         .batch_normalization(relu=True, name='bn4b17_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b17_branch2c')
         .batch_normalization(name='bn4b17_branch2c', is_training=False, relu=False))

        (self.feed('res4b16_relu',
                   'bn4b17_branch2c')
         .add(name='res4b17')
         .relu(name='res4b17_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b18_branch2a')
         .batch_normalization(relu=True, name='bn4b18_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b18_branch2b')
         .batch_normalization(relu=True, name='bn4b18_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b18_branch2c')
         .batch_normalization(name='bn4b18_branch2c', is_training=False, relu=False))

        (self.feed('res4b17_relu',
                   'bn4b18_branch2c')
         .add(name='res4b18')
         .relu(name='res4b18_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b19_branch2a')
         .batch_normalization(relu=True, name='bn4b19_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b19_branch2b')
         .batch_normalization(relu=True, name='bn4b19_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b19_branch2c')
         .batch_normalization(name='bn4b19_branch2c', is_training=False, relu=False))

        (self.feed('res4b18_relu',
                   'bn4b19_branch2c')
         .add(name='res4b19')
         .relu(name='res4b19_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b20_branch2a')
         .batch_normalization(relu=True, name='bn4b20_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b20_branch2b')
         .batch_normalization(relu=True, name='bn4b20_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b20_branch2c')
         .batch_normalization(name='bn4b20_branch2c', is_training=False, relu=False))

        (self.feed('res4b19_relu',
                   'bn4b20_branch2c')
         .add(name='res4b20')
         .relu(name='res4b20_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b21_branch2a')
         .batch_normalization(relu=True, name='bn4b21_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b21_branch2b')
         .batch_normalization(relu=True, name='bn4b21_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b21_branch2c')
         .batch_normalization(name='bn4b21_branch2c', is_training=False, relu=False))

        (self.feed('res4b20_relu',
                   'bn4b21_branch2c')
         .add(name='res4b21')
         .relu(name='res4b21_relu')
         .conv(1, 1, 256, 1, 1, biased=False, relu=False, name='res4b22_branch2a')
         .batch_normalization(relu=True, name='bn4b22_branch2a', is_training=False)
         .conv(3, 3, 256, 1, 1, biased=False, relu=False, name='res4b22_branch2b')
         .batch_normalization(relu=True, name='bn4b22_branch2b', is_training=False)
         .conv(1, 1, 1024, 1, 1, biased=False, relu=False, name='res4b22_branch2c')
         .batch_normalization(name='bn4b22_branch2c', is_training=False, relu=False))

        (self.feed('res4b21_relu',
                   'bn4b22_branch2c')
         .add(name='res4b22')
         .relu(name='res4b22_relu'))

        # ========= RPN ============
        (self.feed('res4b22_relu')
         .conv(3, 3, 512, 1, 1, name='rpn_conv/3x3')
         .conv(1, 1, len(self.anchor_scales) * 3 * 2, 1, 1, padding='VALID', relu=False, name='rpn_cls_score'))

        if self.is_train:
            (self.feed('rpn_cls_score', 'gt_boxes', 'im_info')
             .anchor_target_layer(self.feat_stride, self.anchor_scales, name='rpn-data'))
            # Loss of rpn_cls & rpn_boxes

        (self.feed('rpn_conv/3x3')
         .conv(1, 1, len(self.anchor_scales) * 3 * 4, 1, 1, padding='VALID', relu=False, name='rpn_bbox_pred'))

        # ========= RoI Proposal ============
        (self.feed('rpn_cls_score')
         .spatial_reshape_layer(2, name='rpn_cls_score_reshape')
         .spatial_softmax(name='rpn_cls_prob'))

        (self.feed('rpn_cls_prob')
         .spatial_reshape_layer(len(self.anchor_scales) * 3 * 2, name='rpn_cls_prob_reshape'))

        (self.feed('rpn_cls_prob_reshape', 'rpn_bbox_pred', 'im_info')
         .proposal_layer(self.feat_stride, self.anchor_scales, self.mode, name='rpn_rois'))

        if self.is_train:
            (self.feed('rpn_rois', 'gt_boxes')
             .proposal_target_layer(self.n_classes, name='roi-data'))

        feed_layer = 'roi-data' if self.is_train else 'rois'
        # ========= RCNN ============
        (self.feed('res4b22_relu', feed_layer)
         .roi_pool(7, 7, 1.0 / 16, name='res5a_branch2a_roipooling')
         .conv(1, 1, 512, 2, 2, biased=False, relu=False, name='res5a_branch2a', padding='VALID')
         .batch_normalization(relu=True, name='bn5a_branch2a', is_training=False)
         .conv(3, 3, 512, 1, 1, biased=False, relu=False, name='res5a_branch2b')
         .batch_normalization(relu=True, name='bn5a_branch2b', is_training=False)
         .conv(1, 1, 2048, 1, 1, biased=False, relu=False, name='res5a_branch2c')
         .batch_normalization(name='bn5a_branch2c', is_training=False, relu=False))

        (self.feed('res5a_branch2a_roipooling')
         .conv(1, 1, 2048, 2, 2, biased=False, relu=False, name='res5a_branch1', padding='VALID')
         .batch_normalization(name='bn5a_branch1', is_training=False, relu=False))

        (self.feed('bn5a_branch1',
                   'bn5a_branch2c')
         .add(name='res5a')
         .relu(name='res5a_relu')
         .conv(1, 1, 512, 1, 1, biased=False, relu=False, name='res5b_branch2a')
         .batch_normalization(relu=True, name='bn5b_branch2a', is_training=False)
         .conv(3, 3, 512, 1, 1, biased=False, relu=False, name='res5b_branch2b')
         .batch_normalization(relu=True, name='bn5b_branch2b', is_training=False)
         .conv(1, 1, 2048, 1, 1, biased=False, relu=False, name='res5b_branch2c')
         .batch_normalization(name='bn5b_branch2c', is_training=False, relu=False))

        (self.feed('res5a_relu',
                   'bn5b_branch2c')
         .add(name='res5b')
         .relu(name='res5b_relu')
         .conv(1, 1, 512, 1, 1, biased=False, relu=False, name='res5c_branch2a')
         .batch_normalization(relu=True, name='bn5c_branch2a', is_training=False)
         .conv(3, 3, 512, 1, 1, biased=False, relu=False, name='res5c_branch2b')
         .batch_normalization(relu=True, name='bn5c_branch2b', is_training=False)
         .conv(1, 1, 2048, 1, 1, biased=False, relu=False, name='res5c_branch2c')
         .batch_normalization(name='bn5c_branch2c', is_training=False, relu=False))

        (self.feed('res5b_relu',
                   'bn5c_branch2c')
         .add(name='res5c')
         .relu(name='res5c_relu')
         .avg_pool(4, 4, 1, 1, padding='VALID', name='pool5')
         .fc(self.n_classes, relu=False, name='cls_score')
         .softmax(name='cls_prob'))

        (self.feed('res5c_relu')
         .fc(self.n_classes * 4, relu=False, name='bbox_pred'))
        if self.is_train:
            self.bbox_normalization()

        return self