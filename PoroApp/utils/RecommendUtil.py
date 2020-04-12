__author__ = 'Alvin Zhou'
__email__ = 'xihaozho@usc.edu'
__date__ = '2/21/2020 3:48 PM'

import math

from sklearn.externals import joblib
import numpy as np
import pandas as pd
from warnings import simplefilter

# filter method
from view.NotificationWindow import NotificationWindow


def selectBestAlternativeChampion(input_champ: str) -> list:
    input_file1 = pd.read_csv('resources/data/winRateCorr_spearmanr.csv')
    input_file2 = pd.read_csv('resources/data/champStatsCorr.csv')
    names1 = []
    names2 = []
    for i in range(len(input_file2)):
        champ_name1 = input_file2.iloc[i, 0].replace('.', '')
        champ_name2 = champ_name1.replace('1', '')
        champ_name3 = champ_name2.replace('2', '')
        champ_name4 = champ_name3.replace('3', '')
        champ_name5 = champ_name4.replace('4', '')
        champ_name = champ_name5.replace('?', ' ')

        if champ_name.strip() == input_champ.strip():
            champCorr = input_file2.iloc[i, 1:]
            rank1 = [index for index, value in sorted(list(enumerate(champCorr)), key=lambda x: x[1])]
            rank1 = rank1[::-1]

            for k in range(0, 30):
                champ_name1k = input_file2.columns[rank1[k] + 1].replace('.', '')
                champ_name2k = champ_name1k.replace('1', '')
                champ_name3k = champ_name2k.replace('2', '')
                champ_name4k = champ_name3k.replace('3', '')
                champ_name5k = champ_name4k.replace('4', '')
                champ_namek = champ_name5k.replace('?', ' ')
                names1.append(champ_namek)

    for i in range(len(input_file1)):
        if input_file1.iloc[i, 0].strip() == input_champ:
            winRateCorr = input_file1.iloc[i, 1:]
            rank2 = [index for index, value in sorted(list(enumerate(winRateCorr)), key=lambda x: x[1])]
            rank2 = rank2[::-1]

            for k in range(0, 30):
                names2.append(input_file1.columns[rank2[k] + 1])

    names = set(names1).intersection(set(names2))
    names = list(names)[::-1]
    return names


# selection method
def gen_recommend_champs(bansByThem: list, position: str, bansInAll: list) -> list:
    input_file = pd.read_csv('resources/data/champion.csv')
    names = []
    for i in range(len(input_file)):
        champ_name = input_file.iloc[i, 0].replace('\xa0', ' ')
        names.append((champ_name.strip(), input_file.iloc[i, 1], input_file.iloc[i, 2]))

    possiblePick = []
    for ban in bansByThem:
        temp = selectBestAlternativeChampion(ban)
        possiblePick.extend(temp)

    for champ in possiblePick:
        if champ in bansInAll:
            possiblePick.remove(champ)

    result = {}
    for champ in possiblePick:
        for name in names:
            if champ == name[0] and position == name[1]:
                result[champ] = name[2]
    result = sorted(result.items(), key=lambda item: item[1])

    if len(result) < 1:
        NotificationWindow.detect('BP Champion Session',
                                  "Their Bans are not aiming on specific champions, \n"
                                  "pick your favorite one and beat them with your Mamba Mentality!",
                                  callback=None)
        return None
    else:
        return result[::-1][:3]


input_opgg = pd.read_csv('resources/data/items/General.csv')
input_opgg_jg = pd.read_csv('resources/data/items/Jungle.csv')
input_opgg_sup = pd.read_csv('resources/data/items/Support.csv')
input_basic = pd.read_csv('resources/data/items/basic_stat.csv')


# %%
def winRatePred(champion_name: str, myBuild: list, enemy_build: list) -> float:
    simplefilter(action='ignore', category=UserWarning)
    CD, health, mr, mana, health_regen, ap, ms, attack_speed, ad, life_steal, ar, crit, ar_penetration, mr_penetration, heal_resist = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    res = 0
    for enemy_item in enemy_build:
        enemy_item = enemy_item.replace('1', '').replace("'", '')
    model = joblib.load('resources/model/reg_model.pkl')
    X_columns = pd.read_csv('resources/data/items/columns.txt').columns

    for item in enemy_build:
        for i in range(len(input_basic)):
            if input_basic.iloc[i, 0].replace(' ', '').strip() == item.replace(' ', '').strip():
                CD += input_basic.iloc[i, 1]
                health += input_basic.iloc[i, 2]
                mr += input_basic.iloc[i, 3]
                mana += input_basic.iloc[i, 4]
                health_regen += input_basic.iloc[i, 5]
                ap += input_basic.iloc[i, 6]
                ms += input_basic.iloc[i, 7]
                attack_speed += input_basic.iloc[i, 8]
                ad += input_basic.iloc[i, 9]
                life_steal += input_basic.iloc[i, 10]
                ar += input_basic.iloc[i, 11]
                crit += input_basic.iloc[i, 12]
                ar_penetration += input_basic.iloc[i, 13]
                mr_penetration += input_basic.iloc[i, 14]
                heal_resist += input_basic.iloc[i, 15]
    numerical_enemy_build = [CD, health, mr, mana, health_regen, ap, ms, attack_speed, ad, life_steal, ar, crit,
                             ar_penetration, mr_penetration, heal_resist]

    for item in myBuild:
        x_sample = numerical_enemy_build[:15]
        for column in X_columns[15:]:
            if champion_name == column.replace('Name_', ''):
                x_sample.append(1)
            elif item.replace(' ', '').replace("'", '') == column.replace(' ', '').replace('Item_', ''):
                x_sample.append(1)
            else:
                x_sample.append(0)

        x_input = np.array(x_sample).reshape(1, -1)
        res_temp = model.predict(x_input)
        res += res_temp

    return res


# %%
def itemSuggestion(position: str, champion_name: str, enemy_build: list) -> list:
    if position.strip() == 'SUPPORT':
        input_file = input_opgg_sup
    elif position.strip() == 'JUNGLE':
        input_file = input_opgg_jg
    else:
        input_file = input_opgg

    res_list = []
    temp = 0
    for i in range(len(input_file)):
        if champion_name.replace(' ','').strip() == input_file.iloc[i, 0].strip():
            X = input_file.iloc[i, 1:4]
            winRate = winRatePred(champion_name, list(X), enemy_build)

            if winRate > temp:
                temp = winRate
                del res_list[:]
                for k in range(1, 5):
                    res_list.append(input_file.iloc[i, k])

    if math.isnan(res_list[3]):
        del res_list[3]
    suggestion = []
    for item in res_list:
        if item[0] == ' ':
            item = item[1:]
        new_item = item.replace('1', '').replace(' ', '_')
        suggestion.append(new_item)
    return suggestion

