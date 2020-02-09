__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/5/2020 10:11 PM'

import threading


class ImgCatcherThread(threading.Thread):
    def __init__(self, name, client_info, crop_position):
        threading.Thread.__init__(self)
        self.name = name
        self.client_info = client_info
        self.crop_position = crop_position

    def run(self):
        for i in range(3):
            print("Starting " + self.name)

    client_position = None

    def receivePosition(self, client_position):
        assert len(client_position) == 4, "the position need to have 4 number, like(x1, y1, x2, y2)"
        self.client_position = client_position
        print("new position", client_position)
        # cropImgByRect(client_position)
