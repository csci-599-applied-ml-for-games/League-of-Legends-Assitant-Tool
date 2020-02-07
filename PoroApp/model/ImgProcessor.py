__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/5/2020 10:11 PM'


class ImgCpaturer():
    client_position = None

    def receivePosition(self, client_position):
        assert len(client_position) == 4, "the position need to have 4 number, like(x1, y1, x2, y2)"
        self.client_position = client_position
        print("new position", client_position)
        # cropImgByRect(client_position)
