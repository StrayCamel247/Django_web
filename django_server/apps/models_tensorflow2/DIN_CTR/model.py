#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : Deep interest network for click-through rate prediction
# __date__: 2020/09/21 14
from apps.data.handler import CHECKPOINT_PATH, MODELSLOG_PATH
from apps.models_tensorflow2.DIN_CTR.handler import get_building_dataset
import tensorflow as tf
import numpy as np
import datetime
import os
import pickle
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from apps.data.handler import TMP_PATH


def input_data(dataset, max_sl):
    user = np.array(dataset[:, 0], dtype='int32')
    item = np.array(dataset[:, 1], dtype='int32')
    hist = dataset[:, 2]
    # https://tensorflow.google.cn/api_docs/python/tf/keras/preprocessing/sequence/pad_sequences?hl=zh-cn
    hist_matrix = tf.keras.preprocessing.sequence.pad_sequences(hist, maxlen=max_sl, padding='post')

    sl = np.array(dataset[:, 3], dtype='int32')
    y = np.array(dataset[:, 4], dtype='float32')
    return user, item, hist_matrix, sl, y


def main(params=None):
    hidden_unit = 64
    batch_size = 32
    learning_rate = 1
    epochs = 5
    train_set, test_set, cate_list, (user_count, item_count,
                                     cate_count, max_sl) = get_building_dataset(params)
    train_user, train_item, train_hist, train_sl, train_y = input_data(
        train_set, max_sl)
    # Tensorboard
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = os.path.join(MODELSLOG_PATH, current_time)
    tensorboard = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir,
        histogram_freq=1,
        write_graph=True,
        write_grads=False,
        write_images=True,
        embeddings_freq=0, embeddings_layer_names=None,
        embeddings_metadata=None, embeddings_data=None, update_freq=500
    )
    # model checkpoint
    check_path = os.path.join(
        CHECKPOINT_PATH, 'din_weights.epoch_{epoch:04d}.val_loss_{val_loss:.4f}.ckpt')
    checkpoint = tf.keras.callbacks.ModelCheckpoint(check_path, save_weights_only=True,verbose=1, period=1)

    model = DIN(user_count, item_count, cate_count, cate_list, hidden_unit)
    # 保存模型结构图片
    tf.keras.utils.plot_model(model, to_file='./structure', show_shapes=True)
    print('123')
    # model.summary()
    # optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, decay=0.1)
    # model.compile(loss=tf.keras.losses.binary_crossentropy,
    #               optimizer=optimizer, metrics=[tf.keras.metrics.AUC()])
    # model.fit(
    #     [train_user, train_item, train_hist, train_sl],
    #     train_y,
    #     epochs=epochs,
    #     batch_size=batch_size,
    #     validation_split=0.1,
    #     callbacks=[tensorboard, checkpoint]
    # )


class DataInput:
    def __init__(self, data, batch_size):

        self.batch_size = batch_size
        self.data = data
        self.epoch_size = len(self.data) // self.batch_size
        if self.epoch_size * self.batch_size < len(self.data):
            self.epoch_size += 1
        self.i = 0

    def __iter__(self):
        return self

    def next(self):

        if self.i == self.epoch_size:
            raise StopIteration

        ts = self.data[self.i * self.batch_size: min((self.i + 1) * self.batch_size,
                                                     len(self.data))]
        self.i += 1

        u, i, y, sl = [], [], [], []
        for t in ts:
            u.append(t[0])
            i.append(t[2])
            y.append(t[3])
            sl.append(len(t[1]))
        max_sl = max(sl)

        hist_i = np.zeros([len(ts), max_sl], np.int64)

        k = 0
        for t in ts:
            for l in range(len(t[1])):
                hist_i[k][l] = t[1][l]
            k += 1

        return self.i, (u, i, y, hist_i, sl)


class DataInputTest:
    def __init__(self, data, batch_size):

        self.batch_size = batch_size
        self.data = data
        self.epoch_size = len(self.data) // self.batch_size
        if self.epoch_size * self.batch_size < len(self.data):
            self.epoch_size += 1
        self.i = 0

    def __iter__(self):
        return self

    def next(self):

        if self.i == self.epoch_size:
            raise StopIteration

        ts = self.data[self.i * self.batch_size: min((self.i + 1) * self.batch_size,
                                                     len(self.data))]
        self.i += 1

        u, i, j, sl = [], [], [], []
        for t in ts:
            u.append(t[0])
            i.append(t[2][0])
            j.append(t[2][1])
            sl.append(len(t[1]))
        max_sl = max(sl)

        hist_i = np.zeros([len(ts), max_sl], np.int64)

        k = 0
        for t in ts:
            for l in range(len(t[1])):
                hist_i[k][l] = t[1][l]
            k += 1

        return self.i, (u, i, j, hist_i, sl)


class Dice(tf.keras.layers.Layer):
    """
    define layer:
        dense layer: DNN Layer
        dice: Data Adaptive Activation Function
    """

    def __init__(self):
        super(Dice, self).__init__()
        self.bn = tf.keras.layers.BatchNormalization(center=False, scale=False)
        self.alpha = self.add_weight(shape=(), dtype=tf.float32, name='alpha')

    def call(self, x):
        x_normed = self.bn(x)
        x_p = tf.sigmoid(x_normed)

        return self.alpha * (1.0 - x_p) * x + x_p * x


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class DIN(tf.keras.Model):
    def __init__(self, user_num:"用户数量", item_num:"物品数量", cate_num:"物品种类数量", cate_list:"物品种类列表", hidden_units:"隐藏层单元"):
        """
        《Deep interest network for click-through rate prediction》 模型构建
        """
        super(DIN, self).__init__()
        self.cate_list = tf.convert_to_tensor(cate_list, dtype=tf.int32)
        self.hidden_units = hidden_units
        # self.user_embed = tf.keras.layers.Embedding(
        #     input_dim=user_num, output_dim=hidden_units, embeddings_initializer='random_uniform',
        #     embeddings_regularizer=tf.keras.regularizers.l2(0.01), name='user_embed')
        self.item_embed = tf.keras.layers.Embedding(
            input_dim=item_num, output_dim=self.hidden_units, embeddings_initializer='random_uniform',
            embeddings_regularizer=tf.keras.regularizers.l2(0.01), name='item_embed')
        self.cate_embed = tf.keras.layers.Embedding(
            input_dim=cate_num, output_dim=self.hidden_units, embeddings_initializer='random_uniform',
            embeddings_regularizer=tf.keras.regularizers.l2(0.01), name='cate_embed'
        )
        self.dense = tf.keras.layers.Dense(self.hidden_units)
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.concat = tf.keras.layers.Concatenate(axis=-1)
        self.att_dense1 = tf.keras.layers.Dense(80, activation='sigmoid')
        self.att_dense2 = tf.keras.layers.Dense(40, activation='sigmoid')
        self.att_dense3 = tf.keras.layers.Dense(1)
        self.bn2 = tf.keras.layers.BatchNormalization()
        self.concat2 = tf.keras.layers.Concatenate(axis=-1)
        self.dense1 = tf.keras.layers.Dense(80, activation='sigmoid')
        self.activation1 = tf.keras.layers.PReLU()
        # self.activation1 = Dice()
        self.dense2 = tf.keras.layers.Dense(40, activation='sigmoid')
        self.activation2 = tf.keras.layers.PReLU()
        # self.activation2 = Dice()
        self.dense3 = tf.keras.layers.Dense(1, activation=None)

    def call(self, inputs):
        user, item, hist, sl = inputs[0], tf.squeeze(
            inputs[1], axis=1), inputs[2], tf.squeeze(inputs[3], axis=1)
        # user_embed = self.u_embed(user)
        item_embed = self.concat_embed(item)
        hist_embed = self.concat_embed(hist)
        # 经过attention的物品embedding
        hist_att_embed = self.attention(item_embed, hist_embed, sl)
        hist_att_embed = self.bn1(hist_att_embed)
        hist_att_embed = tf.reshape(
            hist_att_embed, [-1, self.hidden_units * 2])
        u_embed = self.dense(hist_att_embed)
        item_embed = tf.reshape(item_embed, [-1, item_embed.shape[-1]])
        # 联合用户行为embedding、候选物品embedding、【用户属性、上下文内容特征】
        embed = self.concat2([u_embed, item_embed])
        x = self.bn2(embed)
        x = self.dense1(x)
        x = self.activation1(x)
        x = self.dense2(x)
        x = self.activation2(x)
        x = self.dense3(x)
        outputs = tf.nn.sigmoid(x)
        return outputs

    def summary(self):
        user = tf.keras.Input(shape=(1,), dtype=tf.int32)
        item = tf.keras.Input(shape=(1,), dtype=tf.int32)
        sl = tf.keras.Input(shape=(1,), dtype=tf.int32)
        hist = tf.keras.Input(shape=(431,), dtype=tf.int32)
        tf.keras.Model(inputs=[user, item, hist, sl], outputs=self.call(
            [user, item, hist, sl])).summary()

    def concat_embed(self, item):
        """
        拼接物品embedding和物品种类embedding
        :param item: 物品id
        :return: 拼接后的embedding
        """
        # cate = tf.transpose(tf.gather_nd(self.cate_list, [item]))
        cate = tf.gather(self.cate_list, item)
        cate = tf.squeeze(cate, axis=1) if cate.shape[-1] == 1 else cate
        item_embed = self.item_embed(item)
        item_cate_embed = self.cate_embed(cate)
        embed = self.concat([item_embed, item_cate_embed])
        return embed

    def attention(self, queries:"item embedding", keys:"hist embedding", keys_length:"the number of hist_embed"):
        # 候选物品的隐藏向量维度，hidden_unit * 2
        queries_hidden_units = queries.shape[-1]
        # 每个历史记录的物品embed都需要与候选物品的embed拼接，故候选物品embed重复keys.shape[1]次
        # keys.shape[1]为最大的序列长度，即431，为了方便矩阵计算
        # [None, 431 * hidden_unit * 2]
        queries = tf.tile(queries, [1, keys.shape[1]])
        # 重塑候选物品embed的shape
        # [None, 431, hidden_unit * 2]
        queries = tf.reshape(
            queries, [-1, keys.shape[1], queries_hidden_units])
        # 拼接候选物品embed与hist物品embed
        # [None, 431, hidden * 2 * 4]
        embed = tf.concat(
            [queries, keys, queries - keys, queries * keys], axis=-1)
        # 全连接, 得到权重W
        d_layer_1 = self.att_dense1(embed)
        d_layer_2 = self.att_dense2(d_layer_1)
        # [None, 431, 1]
        d_layer_3 = self.att_dense3(d_layer_2)
        # 重塑输出权重类型, 每个hist物品embed有对应权重值
        # [None, 1, 431]
        outputs = tf.reshape(d_layer_3, [-1, 1, keys.shape[1]])

        # Mask
        # 此处将为历史记录的物品embed令为True
        # [None, 431]
        key_masks = tf.sequence_mask(keys_length, keys.shape[1])
        # 增添维度
        # [None, 1, 431]
        key_masks = tf.expand_dims(key_masks, 1)
        # 填充矩阵
        paddings = tf.ones_like(outputs) * (-2 ** 32 + 1)
        # 构造输出矩阵，其实就是为了实现【sum pooling】。True即为原outputs的值，False为上述填充值，为很小的值，softmax后接近0
        # [None, 1, 431] ----> 每个历史浏览物品的权重
        outputs = tf.where(key_masks, outputs, paddings)
        # Scale，keys.shape[-1]为hist_embed的隐藏单元数
        outputs = outputs / (keys.shape[-1] ** 0.5)
        # Activation，归一化
        outputs = tf.nn.softmax(outputs)
        # 对hist_embed进行加权
        # [None, 1, 431] * [None, 431, hidden_unit * 2] = [None, 1, hidden_unit * 2]
        outputs = tf.matmul(outputs, keys)
        return outputs
