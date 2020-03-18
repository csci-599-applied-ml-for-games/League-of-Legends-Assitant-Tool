#%%
import pandas as pd
import numpy as np
import math
# %%
input_opgg = pd.read_csv('Core Build data - OPGG/General.csv')
input_opgg_jg = pd.read_csv('Core Build data - OPGG/Jungle.csv')
input_opgg_sup = pd.read_csv('Core Build data - OPGG/Support.csv')
input_basic = pd.read_csv('basic_stat.csv')
input_basic

#%%
def winRatePred(champion_name:str, myBuild:list, enemy_build:list) -> float:
    CD, health, mr, mana, health_regen, ap, ms, attack_speed, ad, life_steal, ar, crit, ar_penetration, mr_penetration, heal_resist = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    res = 0
    for enemy_item in enemy_build:
        enemy_item = enemy_item.replace('1','').replace("'",'')
    model= joblib.load('reg_model.pkl')
    X_columns = pd.read_csv('columns.txt').columns

    for item in enemy_build:
        for i in range(len(input_basic)):
            if input_basic.iloc[i,0].replace(' ','').strip()==item.replace(' ','').strip():
                CD += input_basic.iloc[i,1]
                health += input_basic.iloc[i,2]
                mr += input_basic.iloc[i,3]
                mana += input_basic.iloc[i,4]
                health_regen += input_basic.iloc[i,5]
                ap += input_basic.iloc[i,6]
                ms += input_basic.iloc[i,7]
                attack_speed += input_basic.iloc[i,8]
                ad += input_basic.iloc[i,9]
                life_steal += input_basic.iloc[i,10]
                ar += input_basic.iloc[i,11]
                crit += input_basic.iloc[i,12]
                ar_penetration += input_basic.iloc[i,13]
                mr_penetration += input_basic.iloc[i,14]
                heal_resist += input_basic.iloc[i,15]
    numerical_enemy_build = [CD, health, mr, mana, health_regen, ap, ms, attack_speed, ad, life_steal, ar, crit, ar_penetration, mr_penetration, heal_resist]
    
    for item in myBuild:
        X = [champion_name]
        X.append(item)
        for item in numerical_enemy_build:
            X.append(item)
        x_sample=X[2:]
        for column in X_columns[15:]:
            if X[0]==column.replace('Name_','') or X[1]==column.replace('Item_',''):
                x_sample.append(1)
            else:
                x_sample.append(0)
        res_temp = model.predict(np.array(x_sample).reshape(1, -1))
    res += res_temp
    
    return res

#%%
def itemSuggestion(position:str, champion_name:str, enemy_build:list) -> list:
    if position.strip()=='Support':
        input_file = input_opgg_sup
    elif position.strip()=='Jungle':
        input_file = input_opgg_jg
    else:
        input_file = input_opgg
    
    res_list = []
    temp=0
    for i in range(len(input_file)):
        if champion_name.strip() == input_file.iloc[i,0].strip():
            X = input_file.iloc[i,0:4]
            # winRate = winRatePred(champion_name, list(X), enemy_build)
            winRate = float(input_file.iloc[i,6])
            if winRate > temp:
                temp = winRate
                del res_list[:]
                for k in range(1,5):     
                    res_list.append(input_file.iloc[i,k])
    
    if math.isnan(res_list[3]):
        del res_list[3]       
    
    return res_list

# %%
test2 = winRatePred('Riven', ['Black Cleaver', "Youmuu's Ghostblade", "Death's Dance"], ['Black Cleaver',"Death's Dance","Boots of speed"])
print(test2)

# %%


# %%
