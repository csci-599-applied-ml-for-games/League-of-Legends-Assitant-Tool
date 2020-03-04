__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/16/2020 2:23 PM'

import threading
import tensorflow as tf
import numpy as np
from tensorflow import keras

from conf.ProfileModelLabel import LABEL_NAME, BANNED_LABEL_NAME
from conf.Settings import IN_GAME_PROFILE_RECOGNITION_CHECK_POINT_PATH, BANNED_CHAMP_RECOGNITION_CHECK_POINT_PATH


class ProfileModel(object):
    _instance_lock = threading.Lock()

    _height = 60
    _width = 60
    _channels = 3
    _batch_size = 128
    _num_classes = 149

    def __init__(self):
        self._reload_model_schema()
        self.model.load_weights(IN_GAME_PROFILE_RECOGNITION_CHECK_POINT_PATH)

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
        img_arr = np.array(image.convert('RGB'))
        image = tf.convert_to_tensor(img_arr)
        image = tf.image.resize(image, [self._width, self._height])
        image = tf.cast(image, tf.float32) / 255.0  # 归一化到[0,1]范围
        image = np.expand_dims(image, axis=0)
        predict_result = self.model.predict(image)
        return LABEL_NAME[np.argmax(predict_result, axis=1)[0]]

    def predictImgs(self, images):
        results = []
        for img in images:
            img_arr = np.array(img.convert('RGB'))
            image = tf.convert_to_tensor(img_arr)
            image = tf.image.resize(image, [self._width, self._height])
            image = tf.cast(image, tf.float32) / 255.0  # 归一化到[0,1]范围
            image = np.expand_dims(image, axis=0)
            predict_result = self.model.predict(image)
            results.append(LABEL_NAME[np.argmax(predict_result, axis=1)[0]])

        return results

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(ProfileModel, "_instance"):
            with ProfileModel._instance_lock:  # 为了保证线程安全在内部加锁
                if not hasattr(ProfileModel, "_instance"):
                    ProfileModel._instance = ProfileModel(*args, **kwargs)
        return ProfileModel._instance


class BanedChampRecognitionModel(object):
    _instance_lock = threading.Lock()

    _height = 32
    _width = 32
    _channels = 3
    _batch_size = 128
    _num_classes = 151

    def __init__(self):
        self._reload_model_schema()
        self.model.load_weights(BANNED_CHAMP_RECOGNITION_CHECK_POINT_PATH)

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
        img_arr = np.array(image.convert('RGB'))
        image = tf.convert_to_tensor(img_arr)
        image = tf.image.resize(image, [self._width, self._height])
        image = tf.cast(image, tf.float32) / 255.0  # 归一化到[0,1]范围
        image = np.expand_dims(image, axis=0)
        predict_result = self.model.predict(image)
        return BANNED_LABEL_NAME[np.argmax(predict_result, axis=1)[0]]

    def predictImgs(self, images):
        results = []
        for img in images:
            img_arr = np.array(img.convert('RGB'))
            image = tf.convert_to_tensor(img_arr)
            image = tf.image.resize(image, [self._width, self._height])
            image = tf.cast(image, tf.float32) / 255.0  # 归一化到[0,1]范围
            image = np.expand_dims(image, axis=0)
            predict_result = self.model.predict(image)
            results.append(BANNED_LABEL_NAME[np.argmax(predict_result, axis=1)[0]])

        return results

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(BanedChampRecognitionModel, "_instance"):
            with BanedChampRecognitionModel._instance_lock:  # 为了保证线程安全在内部加锁
                if not hasattr(BanedChampRecognitionModel, "_instance"):
                    BanedChampRecognitionModel._instance = BanedChampRecognitionModel(*args, **kwargs)
        return BanedChampRecognitionModel._instance
