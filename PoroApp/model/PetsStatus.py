__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/1/2020 5:07 PM'

import os


class PoroStatus():

    def __init__(self):
        self.pet_s_name = "Poro"
        self.dict_data = dict()

    def loadData(self, path):
        assert os.path.exists(path), "please specify your pet's imgs dir"

        for dir in os.listdir(path):
            img_path_list = os.listdir(path + "/" + dir)
            self.dict_data[dir] = [dir + "/" + img_name for img_name in img_path_list]

    def getRowData(self):
        return self.dict_data

    def getStatusName(self):
        return list(self.dict_data.keys())

    def getAllImgPaths(self):
        return list(self.dict_data.values())

    def getSomeImgPaths(self, key):
        return list(self.dict_data[key])
