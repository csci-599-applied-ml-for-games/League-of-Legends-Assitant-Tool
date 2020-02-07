__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/6/2020 5:52 PM'

import random
import string


def genRandomStr(string_length=10):
    letters_and_num = string.hexdigits
    return ''.join(random.choice(letters_and_num) for i in range(string_length))

