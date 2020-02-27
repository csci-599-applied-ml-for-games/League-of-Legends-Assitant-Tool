__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/15/2020 6:22 PM'

import time
import random

import win32gui

from model.KeyBoardListener import KeyBoardCatcher
from model.LoLClientHeartBeat import ClientStatus
from model.InGameInfo import UserInGameInfo
from utils.CopyPasteUtil import pasteToSearchBox
from utils.PositionUtil import genRelativePos, getSearchBoxPoint
from view.NotificationWindow import NotificationWindow
from conf.Settings import BAN_AREA_YOU, BAN_AREA_ENEMY, BANNED_CHAMP_SIZE, TAB_PANEL, LOL_CLIENT_NAME, \
    SEARCH_BOX_POINT, YOUR_TEAM_AREA, ENEMY_TEAM_AREA
from model.ImgProcessor import ImgCatcherThread, ImgCropType

bp_session_thread_pool = []
in_game_thread_pool = []
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
                for thread1 in bp_session_thread_pool:
                    thread1.stop()
                for thread2 in in_game_thread_pool:
                    thread2.stop()
                bp_session_thread_pool.clear()
                # 重置所有游戏信息
                ImgCatcherThread.resetLocalList()
                UserInGameInfo.getInstance().resetAll()
        else:
            # 游戏阶段， BP， 选英雄， 游戏内
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
                bpSessionAnalysis(client)


            else:
                if len(bp_session_thread_pool) > 0:
                    for thread in bp_session_thread_pool:
                        thread.stop()
                    bp_session_thread_pool.clear()
                inGameAnalysis(client)


    else:
        NotificationWindow.warning('Warning',
                                   "Assistant has lost connection to LOL client",
                                   callback=None)


def inGameAnalysis(client_info):
    if len(in_game_thread_pool) == 0:
        NotificationWindow.suggest('Game Mode',
                                   "Ready to fright! \n"
                                   "Poro will continue to give you suggestions. \n help you to win this game",
                                   callback=None)

        enemy_team_catcher = ImgCatcherThread("ENEMY_TEAM_PROFILE_CATCHER", client_info, ImgCropType.ENEMY_TEAM_5_CHAMP,
                                              genRelativePos(client_info.getPosition(), ENEMY_TEAM_AREA,
                                                             client_info.getEnlargementFactor()))

        in_game_thread_pool.append(enemy_team_catcher)
        enemy_team_catcher.setDaemon(True)
        enemy_team_catcher.start()

        # tab_catcher = KeyBoardCatcher("TAB_IMG_CATCHER", client_info, TAB_PANEL)
        #
        # in_game_thread_pool.append(tab_catcher)
        # tab_catcher.setDaemon(True)
        # tab_catcher.start()
    if len(UserInGameInfo.getInstance().getEnemyTeamList()) == 5:
        NotificationWindow.detect('BP Champion Session',
                                  """Enemy team has choose these following champions:<html>
                                  <head><style>.info{{text-align:left;height:40px}}.info span{{display:inline-block;
                                  vertical-align:middle;padding:20px 0;}}.info img{{width:32px;
                                  height:auto;vertical-align:middle}}#class_icon{{width:15px}}#lane_icon{{width:15px;
                                  margin-left:5px}}</style></head><body>{}</body></html>""".format(
                                      UserInGameInfo.getInstance().getEnemyTeamListHTML()),
                                  callback=None)


def copyAndPaste():
    champ_name = UserInGameInfo.getInstance().getRecommendChampAutoCountList()
    enlargement_factor = UserInGameInfo.getInstance().getEnlargementFactor()
    lobby_client = win32gui.FindWindow(None, LOL_CLIENT_NAME)
    if lobby_client != 0:
        rect = win32gui.GetWindowRect(lobby_client)
        relative_point = getSearchBoxPoint(rect, SEARCH_BOX_POINT, enlargement_factor)
        if champ_name is not None:
            pasteToSearchBox(relative_point, champ_name)
        else:
            NotificationWindow.warning('BP Champion Session',
                                       "It seems like you don't have any one recommend champion..\n Good Luck then",
                                       callback=None)


# initialize an image catcher
# and use position data to crop imgs in every n sec.
def bpSessionAnalysis(client_info):
    if len(bp_session_thread_pool) == 0:
        ban_you_catcher = ImgCatcherThread("BAN_YOU_IMG_CATCHER", client_info, ImgCropType.BAN_5_CHAMP,
                                           genRelativePos(client_info.getPosition(), BAN_AREA_YOU,
                                                          client_info.getEnlargementFactor()))

        ban_enemy_catcher = ImgCatcherThread("BAN_ENEMY_IMG_CATCHER", client_info, ImgCropType.ENEMY_BAN_5_CHAMP,
                                             genRelativePos(client_info.getPosition(), BAN_AREA_ENEMY,
                                                            client_info.getEnlargementFactor()))

        bp_session_thread_pool.append(ban_you_catcher)
        bp_session_thread_pool.append(ban_enemy_catcher)
        ban_you_catcher.setDaemon(True)
        ban_enemy_catcher.setDaemon(True)
        ban_you_catcher.start()
        ban_enemy_catcher.start()

    if UserInGameInfo.getInstance().getBannedChampionsSize() >= BANNED_CHAMP_SIZE:
        NotificationWindow.detect('BP Champion Session',
                                  """You team has banned these following champions:<html>
                                  <head><style>.info{{text-align:left;height:40px}}.info span{{display:inline-block;
                                  vertical-align:middle;padding:20px 0;}}.info img{{width:32px;
                                  height:auto;vertical-align:middle}}#class_icon{{width:15px}}#lane_icon{{width:15px;
                                  margin-left:5px}}</style></head><body>{}</body></html>""".format(
                                      UserInGameInfo.getInstance().getBannedChampListHTML()),
                                  callback=None)

    if UserInGameInfo.getInstance().getEnemyBannedChampionsSize() >= BANNED_CHAMP_SIZE:
        UserInGameInfo.getInstance().setEnemyFlag(True)
        NotificationWindow.threat('BP Champion Session',
                                  """Enemy team has banned these following champions:<html>
                                  <head><style>.info{{text-align:left;height:40px}}.info span{{display:inline-block;
                                  vertical-align:middle;padding:20px 0;}}.info img{{width:32px;
                                  height:auto;vertical-align:middle}}#class_icon{{width:15px}}#lane_icon{{width:15px;
                                  margin-left:5px}}</style></head><body>{}</body></html>""".format(
                                      UserInGameInfo.getInstance().getEnemyBannedChampListHTML()),
                                  callback=None)

    # 在这里可以进行英雄推荐了
    if UserInGameInfo.getInstance().getEnemyBannedChampionsSize() >= BANNED_CHAMP_SIZE and \
            UserInGameInfo.getInstance().getBannedChampionsSize() >= BANNED_CHAMP_SIZE:
        print("UserPosition :", UserInGameInfo.getInstance().getPosition())
        UserInGameInfo.getInstance().initRecommendChampList()
        NotificationWindow.suggest('BP Champion Session',
                                   """Poro highly recommends you to choose champion:<html>
                                  <head><style>.info{{text-align:left;height:40px}}.info span{{display:inline-block;
                                  vertical-align:middle;padding:20px 0;}}.info img{{width:32px;
                                  height:auto;vertical-align:middle}}#class_icon{{width:15px}}#lane_icon{{width:15px;
                                  margin-left:5px}}</style></head><body>{}</body></html>""".format(
                                       UserInGameInfo.getInstance().getRecommendChampListHTML()),
                                   callback=copyAndPaste)
