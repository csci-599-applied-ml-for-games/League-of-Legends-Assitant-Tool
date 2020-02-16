__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/15/2020 6:22 PM'

from model.LoLClientHeartBeat import ClientStatus
from model.InGameInfo import UserInGameInfo
from utils.PositionUtil import genRelativePos
from view.NotificationWindow import NotificationWindow
from conf.Settings import BAN_AREA_YOU, BAN_AREA_ENEMY, POSITION_AREA
from model.ImgProcessor import ImgCatcherThread, ImgCropType

thread_pool = []


def statusChange(client):
    if client.hasAlive():
        if not client.isGameMode():
            # 非游戏和 房间阶段
            NotificationWindow.info('Info',
                                    "LOL Client Status: Your are in <u><b>{}</b></u> Panel".format(
                                        client.getStatus()["name"]),
                                    callback=None)
        else:
            # detect user's position
            if client.getStatusIndex() == ClientStatus.AssignPosition:
                NotificationWindow.suggest('Entering Game Mode...',
                                           "You are assigned in {} position.".format(
                                               UserInGameInfo.getInstance().getPosition()),
                                           callback=None)

            # picking champions
            elif client.getStatusIndex() == ClientStatus.ChooseChampion:
                NotificationWindow.suggest('BP Champion Session',
                                           "Poro recommends these following champions for you",
                                           callback=None)

                # TODO 都是为了测试， 正式时候可以删除
                if not UserInGameInfo.getInstance().hasPositionInfo():
                    print("Since we join the custom room, so we assigned a TOP position to you")
                    UserInGameInfo.getInstance().setPosition("TOP")
                # 这里开启一个线程 去捕捉 图片 预测 不需要跟pyqt挂钩
                goCaptureAndAnalysis(client)


            else:
                # InGame
                # TODO
                NotificationWindow.suggest('Game Mode',
                                           "Ready to fright! \n"
                                           "Poro will continue to give you suggestions",
                                           callback=None)
                # goCaptureAndAnalysis(client)


    else:
        NotificationWindow.warning('Warning',
                                   "Assistant has lost connection to LOL client",
                                   callback=None)


# initialize an image catcher
# and use position data to crop imgs in every n sec.
def goCaptureAndAnalysis(client_info):
    ImgCropType.init()
    print("User position: ", UserInGameInfo.getInstance().getPosition())
    if client_info.getStatusIndex() == ClientStatus.ChooseChampion:
        ban_you_catcher = ImgCatcherThread("BAN_YOU_IMG_CATCHER", client_info, ImgCropType.BAN_5_CHAMP,
                                           genRelativePos(client_info.getPosition(), BAN_AREA_YOU,
                                                          client_info.getEnlargementFactor()))
        thread_pool.append(ban_you_catcher)

        ban_enemy_catcher = ImgCatcherThread("BAN_ENEMY_IMG_CATCHER", client_info, ImgCropType.BAN_5_CHAMP,
                                             genRelativePos(client_info.getPosition(), BAN_AREA_ENEMY,
                                                            client_info.getEnlargementFactor()))
        thread_pool.append(ban_enemy_catcher)

        ban_you_catcher.start()
        ban_enemy_catcher.start()
    else:
        # when you got here, it means you are in the game mode
        print("go_capture -> ", client_info.getStatus())
    # capturer.receivePosition(client_info.getPosition())
