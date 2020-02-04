import numpy as np
import pandas as pd
import csv
# filter method
def selectBestAlternativeChampion(input_champ: str) -> list:
    input_file1 = pd.read_csv('winRateCorr_spearmanr.csv')
    input_file2 = pd.read_csv('champStatsCorr.csv')
    names1 = []
    names2 = []
    for i in range(len(input_file2)):
        champ_name1 = input_file2.iloc[i,0].replace('.','')
        champ_name2 = champ_name1.replace('1','')
        champ_name3 = champ_name2.replace('2','')
        champ_name4 = champ_name3.replace('3','')
        champ_name5 = champ_name4.replace('4','')
        champ_name = champ_name5.replace('?',' ')

        if champ_name.strip() == input_champ.strip():
            champCorr = input_file2.iloc[i,1:]
            rank1 = [index for index,value in sorted(list(enumerate(champCorr)),key=lambda x:x[1])]
            rank1 = rank1[::-1]
            
            for k in range(0,30):
                champ_name1k = input_file2.columns[rank1[k]+1].replace('.','')
                champ_name2k = champ_name1k.replace('1','')
                champ_name3k = champ_name2k.replace('2','')
                champ_name4k = champ_name3k.replace('3','')
                champ_name5k = champ_name4k.replace('4','')
                champ_namek = champ_name5k.replace('?',' ')               
                names1.append(champ_namek)
    
    for i in range(len(input_file1)):
        if input_file1.iloc[i,0].strip() == input_champ:
            winRateCorr = input_file1.iloc[i,1:]
            rank2 = [index for index,value in sorted(list(enumerate(winRateCorr)),key=lambda x:x[1])]
            rank2 = rank2[::-1]
            
            for k in range(0,30):
                names2.append(input_file1.columns[rank2[k]+1])
    
    names = set(names2).intersection(set(names1))
    names = list(names)[::-1][:5]
    return names

# selection method
def basedOnBans(bansByThem:list, position:str, bansInAll:list)->list:
    input_file = pd.read_csv('champion.csv')
    names = []
    for i in range(len(input_file)):
        champ_name = input_file.iloc[i,0].replace('\xa0',' ')
        names.append((champ_name.strip(),input_file.iloc[i,1]))

    possiblePick = []
    for ban in bansByThem:
        temp = selectBestAlternativeChampion(ban)
        possiblePick.extend(temp)

    for champ in possiblePick:
        if champ in bansInAll:
            possiblePick.remove(champ)
    
    result = []
    for champ in possiblePick:
        for name in names:
            if champ == name[0] and position == name[1]:
                result.append(champ)
    result = set(result)
    return result   

# %%
test = basedOnBans(bansByThem=["Rengar","Master Yi","Nocturne","Vel'Koz","Sett"],
                    position="Top",
                    bansInAll=["Rengar","Master Yi","Nocturne","Vel'Koz","Sett",
                    "Sona","Sett","Taric","Yasuo","Dr. Mundo"])
print(test)
# %%
