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


def getSearchBoxPoint(client_pos, search_box_point, factor=1.0):
    assert len(client_pos) == 4, "client_point has to be an array with 2 number"
    assert len(search_box_point) == 2, "search_box_point has to be an array with 2 number"
    search_box_point = tuple([factor * x for x in search_box_point])
    return (client_pos[0] + search_box_point[0],
            client_pos[1] + search_box_point[1])
