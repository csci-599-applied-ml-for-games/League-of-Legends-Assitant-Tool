__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/16/2020 10:30 AM'

import collections
import csv
import threading

from conf.Settings import CHAMPION_BASIC_CSV_PATH, CHAMPION_PROFILE_PATH

FILE_PATH = CHAMPION_BASIC_CSV_PATH


def gen_multi_lanes(lanes):
    imgs_html = ""
    for lane in lanes:
        if lane is not None and lane is not "":
            imgs_html += "<img id=\"lane_icon\" src=\"resources/data/lane/{}.png\">".format(lane)

    return imgs_html


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
                    "img": CHAMPION_PROFILE_PATH + "/" + row[3] + ".jpg",
                    "class": row[5],
                    "POS": gen_multi_lanes(list([row[6], row[7], row[8]]))
                }

    def toHtml(self, champ_name, win_rate=None):
        return "<div class=\"info\"><img src=\"{}\"> {} {}<br/>" \
               "<span><img id=\"class_icon\" src=\"{}\">&nbsp;&nbsp;&nbsp;{}" \
               "</span></div><hr/>" \
            .format(self.info[champ_name]['img'],
                    self.info[champ_name]['en_name'],
                    "[Win Rate]: " + str(win_rate) if win_rate is not None else "- [" + self.info[champ_name][
                        'en_title'] + "]",
                    "resources/data/classes/{}.png".format(self.info[champ_name]['class']),
                    self.info[champ_name]['POS'])

    def toSimpleHtml(self, champ_name):
        return "<div class=\"info\"><img src=\"{}\"> {} - [{}] <span><img id=\"class_icon\" src=\"{}\"></div>" \
            .format(self.info[champ_name]['img'],
                    self.info[champ_name]['en_name'],
                    self.info[champ_name]['en_title'],
                    "resources/data/classes/{}.png".format(self.info[champ_name]['class']))

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(ChampionBasicInfo, "_instance"):
            with ChampionBasicInfo._instance_lock:
                if not hasattr(ChampionBasicInfo, "_instance"):
                    ChampionBasicInfo._instance = ChampionBasicInfo(*args, **kwargs)
        return ChampionBasicInfo._instance
