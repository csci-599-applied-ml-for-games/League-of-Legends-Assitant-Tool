__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '3/4/2020 10:45 AM'

import collections
import csv
import threading

from conf.Settings import GEAR_BASIC_CSV_PATH, GEAR_PROFILE_PATH

FILE_PATH = GEAR_BASIC_CSV_PATH


def gen_multi_lanes(lanes):
    imgs_html = ""
    for lane in lanes:
        if lane is not None and lane is not "":
            imgs_html += "<img id=\"lane_icon\" src=\"resources/data/gears/{}.png\">".format(lane)

    return imgs_html


class GearsBasicInfo(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.info = collections.defaultdict(dict)
        with open(FILE_PATH, encoding="utf8") as champion_info_file:
            data = csv.reader(champion_info_file, delimiter=',')
            for row in data:
                self.info[row[0]] = {
                    "en_name": row[0],
                    "img": GEAR_PROFILE_PATH + "/" + row[0] + "_item.png",
                }

    def toHtml(self, gear_name):
        return "<div class=\"gears\"><img src=\"{}\"> {} </div>" \
            .format(self.info[gear_name]['img'],
                    self.info[gear_name]['en_name'])

    def toImgHtml(self, gear_name_list):
        gears_str = ""
        for gear in gear_name_list:
            gears_str += "<img src=\"resources/data/gears/{}.png\">&nbsp;&nbsp;".format(gear)
        return gears_str

    @classmethod
    def getInstance(cls, *args, **kwargs):
        if not hasattr(GearsBasicInfo, "_instance"):
            with GearsBasicInfo._instance_lock:
                if not hasattr(GearsBasicInfo, "_instance"):
                    GearsBasicInfo._instance = GearsBasicInfo(*args, **kwargs)
        return GearsBasicInfo._instance
