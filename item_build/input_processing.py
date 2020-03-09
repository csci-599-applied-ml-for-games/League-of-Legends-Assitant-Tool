#%%
import pandas as pd
import numpy as np
import csv
import os
# traversal files
input_basic = pd.read_csv('basic_stat.csv')
output_file = open('numerical_2.csv','w')
writer = csv.writer(output_file)
for root,dirs,files in os.walk("item-build/export/after-se"):
    for file in files:
        print(root)
        file_name = os.path.join(root,file)
        input_file = pd.read_csv(file_name, engine="python")
# convert into numerical data
        for k in range(0, len(input_file), 5):
            enemy_builds = input_file.iloc[k:k+5,5]
            numerical_enemy_build = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            for enemy_build in enemy_builds:
                enemy_build = enemy_build.replace('1','').replace('[','').replace(']','').replace('"','').replace("'",'').split(',')
                CD, health, mr, mana, health_regen, ap, ms, attack_speed, ad, life_steal, ar, crit, ar_penetration, mr_penetration, heal_resist = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                for item in enemy_build:
                    for i in range(len(input_basic)):
                        if item.replace('\xa0',' ').replace(' ','') == input_basic.iloc[i,0].replace(' ','').strip():
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
                numerical_enemy_build += np.array([CD, health, mr, mana, health_regen, ap, ms, attack_speed, ad, life_steal, ar, crit, ar_penetration, mr_penetration, heal_resist])
# write numerical.csv
            myBuild = input_file.iloc[k,4]
            myBuild = myBuild.replace('1','').replace('[','').replace(']','').replace('"','').replace("'",'').split(', ')
            for item in myBuild:
                if item != '':
                    row = [input_file.iloc[k,3]]
                    row.append(item)
                    for item1 in numerical_enemy_build:
                        row.append(item1)
                    row.append(input_file.iloc[k,2])
                    writer.writerow(row)

# %%
