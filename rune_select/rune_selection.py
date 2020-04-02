#%%
import pandas as pd
import numpy as np

# %%
data = pd.read_csv('output_comma.csv')
champ_stats = pd.read_csv('champion.csv')
# %%
def runeSelect(enemy_champion: list, my_champion: str, position: str) -> list:
    ap=0
    for champ in enemy_champion:
        for i in range(len(champ_stats)):
            if champ_stats[i][0] == champ and champ_stats[i][1]==position:
                ap += champ_stats[i][-1]
    winrate = 0
    res = []
    if position == 'Support' or position == 'Bottom':
        if ap >= 2:
            for i in range(len(data)):
                if data[i][0] == my_champion and data[i][10] == 'Magic Resist' and data[i][-1]>winrate:
                     res.append(data[i][1:11])
                     winrate = data[i][-1]
        else:
            for i in range(len(data)):
                if data[i][0] == my_champion and data[i][10] != 'Magic Resist' and data[i][-1]>winrate:
                     res.append(data[i][1:11])
                     winrate = data[i][-1]