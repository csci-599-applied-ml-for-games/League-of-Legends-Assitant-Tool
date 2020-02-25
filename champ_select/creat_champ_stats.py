#%%
import numpy as np
import pandas as pd
import csv
from sklearn.metrics.pairwise import cosine_similarity
# %%
file = pd.read_csv('champion.csv')
file
# %%
data_input = np.array(file.iloc[:,1:])
data_input
# %%
data_output = (cosine_similarity(data_input)-0.9)*10
data_output
# %%
with open('champStatsCorr.csv','w') as output:
    writer = csv.writer(output)

    for i in range(len(data_output)):
        writer.writerow(data_output[i])

# %%
