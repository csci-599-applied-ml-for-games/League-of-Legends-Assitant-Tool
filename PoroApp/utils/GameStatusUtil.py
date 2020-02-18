__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/15/2020 6:22 PM'

import time
import random

from model.LoLClientHeartBeat import ClientStatus
from model.InGameInfo import UserInGameInfo
from utils.PositionUtil import genRelativePos
from view.NotificationWindow import NotificationWindow
from conf.Settings import BAN_AREA_YOU, BAN_AREA_ENEMY, BANNED_CHAMP_SIZE, POPUP_COUNTER
from model.ImgProcessor import ImgCatcherThread, ImgCropType

thread_pool = []
ImgCropType.init()


def statusChange(client):
    global POPUP_COUNTER
    if client.hasAlive():
        if not client.isGameMode():
            # 非游戏和 房间阶段
            NotificationWindow.info('Info',
                                    "LOL Client Status: Your are in <u><b>{}</b></u> Panel".format(
                                        client.getStatus()["name"]),
                                    callback=None)
            # TODO  暂时防误杀
            if client.getStatus()["name"] != "InRoom":
                for item in thread_pool:
                    item.stop()
        else:
            # detect user's position
            if client.getStatusIndex() == ClientStatus.AssignPosition:
                NotificationWindow.detect('Entering Game Mode...',
                                          "You are assigned in <u><b>{}</b></u> position.".format(
                                              UserInGameInfo.getInstance().getPosition()),
                                          callback=None)

            # picking champions
            elif client.getStatusIndex() == ClientStatus.ChooseChampion:
                if random.randint(0, 1) == 1:
                    NotificationWindow.detect('BP Champion Session',
                                              "You have entered Champion BP Session.",
                                              callback=None)

                # TODO 都是为了测试， 正式时候可以删除
                if not UserInGameInfo.getInstance().hasPositionInfo():
                    print("Since we join the custom room, so we assigned a TOP position to you")
                    UserInGameInfo.getInstance() \
                        .setPosition("TOP", msg="Since we join the custom room, so we assigned a TOP position to you")
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
    if client_info.getStatusIndex() == ClientStatus.ChooseChampion:
        ban_you_catcher = None
        ban_enemy_catcher = None
        if len(thread_pool) == 0:
            ban_you_catcher = ImgCatcherThread("BAN_YOU_IMG_CATCHER", client_info, ImgCropType.BAN_5_CHAMP,
                                               genRelativePos(client_info.getPosition(), BAN_AREA_YOU,
                                                              client_info.getEnlargementFactor()))

            ban_enemy_catcher = ImgCatcherThread("BAN_ENEMY_IMG_CATCHER", client_info, ImgCropType.ENEMY_5_CHAMP,
                                                 genRelativePos(client_info.getPosition(), BAN_AREA_ENEMY,
                                                                client_info.getEnlargementFactor()))

            thread_pool.append(ban_you_catcher)
            thread_pool.append(ban_enemy_catcher)
            ban_you_catcher.setDaemon(True)
            ban_enemy_catcher.setDaemon(True)
            ban_you_catcher.start()
            ban_enemy_catcher.start()

        if random.randint(0, 1) == 1 \
                and UserInGameInfo.getInstance().getBannedChampionsSize() >= BANNED_CHAMP_SIZE:
            NotificationWindow.detect('BP Champion Session',
                                      "You team has banned these following champions: \n"
                                      "{}".format(UserInGameInfo.getInstance().getBannedChampList()),
                                      callback=None)

        if UserInGameInfo.getInstance().getEnemyBannedChampionsSize() >= BANNED_CHAMP_SIZE:
            UserInGameInfo.getInstance().setEnemyFlag(True)
            NotificationWindow.threat('BP Champion Session',
                                      "Enemy team has banned these following champions: \n"
                                      "{}".format(UserInGameInfo.getInstance().getEnemyBannedChampList()),
                                      callback=None)

        # 在这里可以进行英雄推荐了
        if UserInGameInfo.getInstance().getEnemyBannedChampionsSize() >= BANNED_CHAMP_SIZE and \
                UserInGameInfo.getInstance().getBannedChampionsSize() >= BANNED_CHAMP_SIZE:
            print("UserPosition :", UserInGameInfo.getInstance().getPosition())
            NotificationWindow.suggest('BP Champion Session',
                                       "Poro highly recommends you to choose champion: \n"
                                       " <u><b> {} </b></u> to win this game. ".format("Drius"),
                                       callback=None)


    else:
        # when you got here, it means you are in the game mode
        print("go_capture -> ", client_info.getStatus())
        # capturer.receivePosition(client_info.getPosition())
