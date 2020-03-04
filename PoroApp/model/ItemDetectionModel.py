__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/28/2020 10:56 PM'

import threading
import tensorflow as tf
import numpy as np
from tensorflow import keras

from conf.ItemModelLabel import LABEL_NAME
from conf.Settings import ITEM_DETECTION_CHECK_POINT_PATH
from utils.ImgUtil import split2NPieces, cut3X2Boxes


class ItemModel(object):
    _instance_lock = threading.Lock()

    _height = 64
    _width = 64
    _channels = 3
    _batch_size = 128
    _num_classes = 170

    def __init__(self):
        self._reload_model_schema()
        self.model.load_weights(ITEM_DETECTION_CHECK_POINT_PATH)

    def _reload_model_schema(self):
        self.model = tf.keras.models.Sequential([
            keras.layers.Conv2D(filters=16, kernel_size=3, padding='same',
                                activation='selu', input_shape=[self._width, self._height, self._channels]),
            keras.layers.Conv2D(filters=16, kernel_size=3,
                                padding='same', activation='selu'),
            keras.layers.MaxPool2D(pool_size=2),

            keras.layers.Conv2D(filters=32, kernel_size=3,
                                padding='same', activation='selu'),
            keras.layers.Conv2D(filters=32, kernel_size=3,
                                padding='same', activation='selu'),
            keras.layers.MaxPool2D(pool_size=2),

            keras.layers.Conv2D(filters=64, kernel_size=3, padding='same',
                                activation='selu', input_shape=[self._width, self._height, self._channels]),
            keras.layers.Conv2D(filters=64, kernel_size=3,
                                padding='same', activation='selu'),
            keras.layers.MaxPool2D(pool_size=2),

            keras.layers.Flatten(),
            keras.layers.Dense(128, activation='selu'),
            keras.layers.AlphaDropout(rate=0.5),

            keras.layers.Dense(self._num_classes, activation='softmax')
        ])

        self.model.compile(loss="categorical_crossentropy",
                           optimizer="adam", metrics=['accuracy'])

        return self.model

    def getModel(self):
        return self.model

    def predictSingleImg(self, image):
        # convert PIL image to Tensor
        result = list()
        imgs = split2NPieces(image, pieces=6, interval=1, horizontal=True)
        for img in imgs:
            img_arr = np.array(img.convert('RGB'))
            image = tf.convert_to_tensor(img_arr)
            image = tf.image.resize(image, [self._width, self._height])
            image = tf.cast(image, tf.float32) / 255.0  # 归一化到[0,1]范围
            image = np.expand_dims(image, axis=0)
            predict_result = self.model.predict(image)
            result.append(LABEL_NAME[np.argmax(predict_result, axis=1)[0]])
        return result

    def predictImgs(self, images):
        results = []
        for img in images:
            results.append(self.predictSingleImg(img))
        return results

    def predict3X2Img(self, image, interval=5, save_file=False):
        result = list()
        imgs = cut3X2Boxes(image, interval=interval, save_file=save_file)
        for img in imgs:
            img_arr = np.array(img.convert('RGB'))
            image = tf.convert_to_tensor(img_arr)
            image = tf.image.resize(image, [self._width, self._height])
            image = tf.cast(image, tf.float32) / 255.0  # 归一化到[0,1]范围
            image = np.expand_dims(image, axis=0)
            predict_result = self.model.predict(image)
            result.append(LABEL_NAME[np.argmax(predict_result, axis=1)[0]])
        return result

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(ItemModel, "_instance"):
            with ItemModel._instance_lock:
                if not hasattr(ItemModel, "_instance"):
                    ItemModel._instance = ItemModel(*args, **kwargs)
        return ItemModel._instance
