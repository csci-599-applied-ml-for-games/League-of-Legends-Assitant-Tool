__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/8/2020 5:43 PM'


def genRelativePos(client_pos, area_info, factor=1.0):
    assert len(client_pos) == 4, "client_pos has to be an array with 4 number"
    assert len(area_info) == 4, "client_pos has to be an array with 4 number"
    area_info = tuple([factor * x for x in area_info])
    return (client_pos[0] + area_info[0],
            client_pos[1] + area_info[1],
            client_pos[0] + area_info[2],
            client_pos[1] + area_info[3])
