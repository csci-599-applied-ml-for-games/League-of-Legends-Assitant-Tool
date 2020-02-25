#%%
import numpy as np
import pandas as pd
import csv
from scipy.stats import spearmanr
# %%
winRateIn = pd.read_csv('winRate.csv')
winRateIn = np.array(winRateIn)
# winRateIn[x][3] is champName
# winRateIn[x][4] is champAgainst
# winRateIn[x][5] is winRate
winRateOut = pd.read_csv('winRateIndex.csv')
winRateOut = winRateOut.iloc[0:145]
# %%
for name in winRateOut.columns:
    for x in range(len(winRateIn)):
        if name.strip() == winRateIn[x][0].strip():

            for i in range(len(winRateOut)):
                if winRateIn[x][4].strip() == winRateOut.iloc[i,0].strip():
                    winRateOut.loc[i,name] = winRateIn[x][5]
#%%
winRateOut_1 = np.array(winRateOut.iloc[:,1:])
winRateOut_1[np.isnan(winRateOut_1)]=50.00
#%%
winRateOut_2, pval = spearmanr(winRateOut_1) 
winRateOut_2
#%%
# winRateOut_2 = np.cov(winRateOut_1)

# %%
with open('winRateCorr_spearmanr.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow(winRateOut.columns)
    for i in range(len(winRateOut_2)):
        writer.writerow(winRateOut_2[i])
# %%
corr_matrix = pd.read_csv('winRateCorr_spearmanr.csv')
corr_matrix

# %%
