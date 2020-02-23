__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/16/2020 10:30 AM'

import collections
import csv
import threading

from conf.Settings import CHAMPION_BASIC_CSV_PATH, CHAMPION_PROFILE_PATH

FILE_PATH = CHAMPION_BASIC_CSV_PATH


class ChampionBasicInfo(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.info = collections.defaultdict(dict)
        with open(FILE_PATH, encoding="utf8") as champion_info_file:
            data = csv.reader(champion_info_file, delimiter=',')
            for row in data:
                self.info[row[3]] = {
                    "en_name": row[3],
                    "en_title": row[4],
                    "img": CHAMPION_PROFILE_PATH + "/" + row[3] + ".jpg"
                }

    def toHtml(self, champ_name):
        return "<div class=\"info\"><img src=\"{}\">  Name: {}  Win Rate: {}<br/>" \
               "<span><img id=\"class_icon\" src=\"{}\">&nbsp;&nbsp;&nbsp;<img id=\"lane_icon\" src=\"{}\">" \
               "</span></div><br/>" \
            .format(self.info[champ_name]['img'],
                    self.info[champ_name]['en_name'],
                    "58.9%",
                    "resources/data/classes/Marksman.png",
                    "resources/data/lane/Top.png")

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(ChampionBasicInfo, "_instance"):
            with ChampionBasicInfo._instance_lock:
                if not hasattr(ChampionBasicInfo, "_instance"):
                    ChampionBasicInfo._instance = ChampionBasicInfo(*args, **kwargs)
        return ChampionBasicInfo._instance
