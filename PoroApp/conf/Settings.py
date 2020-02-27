__author__ = 'Aaron Yang'
__email__ = 'byang971@usc.edu'
__date__ = '2/2/2020 8:33 PM'

# Pet's Opacity
DEFAULT_OPACITY = 90
DEFAULT_DRAGGABLE = True
ASSETS_DIR = "resources/assets/"
# the interval(ms) between every frame of pet's emoji
TIME_INTERVAL = 800

# LOL client name in Task Manager
LOL_CLIENT_NAME = 'League of Legends'
LOL_IN_GAME_CLIENT_NAME = "League of Legends (TM) Client"
LOL_CLIENT_HEART_BEAT_RATE = 2
LOL_CLIENT_SIZE = (1280, 720)
IN_GAME_CLIENT_SIZE = (1920, 1080)

# Notification_Item Setting
LAST_TIME = 4000
POPUP_COUNTER = 0
POPUP_THRESHOLD = 3

# champions_profile_area
STATUS_AREA = (60, 15, 840, 53)
BP_AREA = (500, 5, 870, 40)
BAN_AREA_YOU = (15, 30, 205, 60)
BAN_AREA_ENEMY = (1075, 30, 1265, 60)
POSITION_AREA = (565, 500, 710, 542)
YOUR_TEAM_AREA = (18, 105, 78, 485)  # Test
# YOUR_TEAM_AREA = (56, 105, 116, 485) # Rank
ENEMY_TEAM_AREA = (1202, 105, 1262, 485)
# player's position set
POSITION_SET = ["TOP", "SUPPORT", "BOTTOM", "JUNGLE", "MID"]
SEARCH_BOX_POINT = (870, 105)

# ImgCatcher Rate
IMG_CATCHER_RATE = 3
BANNED_CHAMP_SIZE = 3

# KeyBoard Capture Rate
KEYBOARD_CATCHER_RATE = 1
TAB_PANEL = (380, 300, 1540, 690)

# Champion profile recognition model setting
CHECK_POINT_PATH = "resources/model/face_recognition_model.h5"

# Champion basic info csv
CHAMPION_BASIC_CSV_PATH = "resources/data/champ_basic.csv"
CHAMPION_PROFILE_PATH = "resources/data/profile"
