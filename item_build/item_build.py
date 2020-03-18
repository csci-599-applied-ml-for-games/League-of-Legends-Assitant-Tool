#%%
import pandas as pd
import numpy as np
import math
from sklearn.externals import joblib
# %%
input_opgg = pd.read_csv('Core Build data - OPGG/General.csv')
input_opgg_jg = pd.read_csv('Core Build data - OPGG/Jungle.csv')
input_opgg_sup = pd.read_csv('Core Build data - OPGG/Support.csv')
input_basic = pd.read_csv('basic_stat.csv')

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
        x_sample=numerical_enemy_build[:15]
        for column in X_columns[15:]:
            if champion_name==column.replace('Name_',''):
                x_sample.append(1)
            elif item.replace(' ','').replace("'",'')==column.replace(' ','').replace('Item_',''):
                x_sample.append(1)
            else:
                x_sample.append(0)

        x_input=np.array(x_sample).reshape(1, -1)
        res_temp = model.predict(x_input)
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
            X = input_file.iloc[i,1:4]
            winRate = winRatePred(champion_name, list(X), enemy_build)
            
            if winRate > temp:
                temp = winRate
                del res_list[:]
                for k in range(1,5):     
                    res_list.append(input_file.iloc[i,k])
    
    if math.isnan(res_list[3]):
        del res_list[3] 
    suggestion=[]      
    for item in res_list:
        if item[0]==' ':
            item = item[1:]
        new_item=item.replace("'",'').lower().replace('1','')
        suggestion.append(new_item)
    return suggestion
# %%
test = itemSuggestion('Top', 'Riven', ['Black Cleaver', "Youmuu's Ghostblade", "Death's Dance","Amplifying Tome","Athenes Unholy Grail","Bramble Vest"])
print(test)

# %%
test2 = winRatePred('Riven', ['Black Cleaver', "Youmuu's Ghostblade", "Death's Dance"], ['Black Cleaver',"Death's Dance","Boots of speed"])
print(test2)

# %%
# To match with image_name, suppose image_name == file
# Then we have to modify file as:
# file = file.replace('_item.png','').replace('_item1.png','').replace('.png','').replace('_',' ').replace("'",'').lower()