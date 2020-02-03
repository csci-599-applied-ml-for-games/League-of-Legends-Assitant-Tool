#%%
import numpy as np
import pandas as pd
import csv
def selectBestAlternativeChampion(input_champ: str) -> str:
    input_file1 = pd.read_csv('winRateCorr_spearmanr.csv')
    input_file2 = pd.read_csv('champStatsCorr.csv')
    for i in range(len(input_file2)):
        if input_file2.iloc[i,0].strip() == input_champ:
            champCorr = input_file2.iloc[i,1:]
            rank1 = [index for index,value in sorted(list(enumerate(champCorr)),key=lambda x:x[1])]
            rank1 = rank1[::-1]
            names1 = []
            for k in range(0,30):
                champ_name1 = input_file2.columns[rank1[k]+1].replace('.','')
                champ_name2 = champ_name1.replace('1','')
                champ_name3 = champ_name2.replace('2','')
                champ_name4 = champ_name3.replace('3','')
                champ_name5 = champ_name4.replace('4','')
                champ_name = champ_name5.replace('?',' ')
                names1.append(champ_name)
    
    for i in range(len(input_file1)):
        if input_file1.iloc[i,0].strip() == input_champ:
            winRateCorr = input_file1.iloc[i,1:]
            rank2 = [index for index,value in sorted(list(enumerate(winRateCorr)),key=lambda x:x[1])]
            rank2 = rank2[::-1]
            names2 = []
            for k in range(0,30):
                names2.append(input_file1.columns[rank2[k]+1])
    
    names = set(names2).intersection(set(names1))
    names = list(names)[::-1]
    return names

# %%
test = selectBestAlternativeChampion(input_champ='Ahri')
print(test)

# %%
