__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/8/2020 5:43 PM'

from conf.Settings import LOL_CLIENT_SIZE, IN_GAME_CLIENT_SIZE


def genRelativePos(client_pos, area_info, factor=1.0):
    assert len(client_pos) == 4, "client_pos has to be an array with 4 number"
    assert len(area_info) == 4, "client_pos has to be an array with 4 number"
    area_info = tuple([factor * x for x in area_info])
    return (client_pos[0] + area_info[0],
            client_pos[1] + area_info[1],
            client_pos[0] + area_info[2],
            client_pos[1] + area_info[3])


def getChampSearchBoxPoint(client_pos, search_box_point, factor=1.0):
    assert len(client_pos) == 4, "client_point has to be an array with 2 number"
    assert len(search_box_point) == 2, "search_box_point has to be an array with 2 number"
    search_box_point = tuple([factor * x for x in search_box_point])
    return (client_pos[0] + search_box_point[0],
            client_pos[1] + search_box_point[1])

def getGearSearchBoxPoint(client_pos, search_box_point, factor=1.0):
    assert len(client_pos) == 4, "client_point has to be an array with 2 number"
    assert len(search_box_point) == 2, "search_box_point has to be an array with 2 number"
    search_box_point = tuple([factor * x for x in search_box_point])
    return (client_pos[0] + search_box_point[0],
            client_pos[1] + search_box_point[1])


def getEnlargementFactor(position, status="BP"):
    enlargement_factor = None
    actual_client_size = (position[2] - position[0], position[3] - position[1])
    if status == "BP":
        enlargement_factor = \
            (list(float(actual / default) for default, actual in zip(LOL_CLIENT_SIZE, actual_client_size)))[0]
    else:
        enlargement_factor = \
            (list(float(actual / default) for default, actual in zip(IN_GAME_CLIENT_SIZE, actual_client_size)))[0]
    return enlargement_factor
