#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file = pd.read_csv('match_history.csv')
file.replace('win',1, inplace=True)
file.replace('lose',0, inplace=True)

X = file.iloc[:,:17]
X = pd.get_dummies(X)
y = np.array(file['result'])
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.3,random_state=42)
reg = LinearRegression().fit(x_train, y_train)
test_error = mean_squared_error(y_test, reg.predict(x_test))
train_error = mean_squared_error(y_train, reg.predict(x_train))
print("test MSE: ", test_error)
print("train MSE: ", train_error)

# %%
x_input=['Lucian','Trinity Force',60,2600,105,500,50,325,250,40,160,0,130,0,24,30,50]
x_sample=x_input[2:]
for column in X.columns[15:]:
    if x_input[0]==column.replace('Name_','') or x_input[1]==column.replace('Item_',''):
        x_sample.append(1)
    else:
        x_sample.append(0)
# %%
test1 = reg.predict(np.array(x_sample).reshape(1, -1))
print(test1)
# %%
from sklearn.externals import joblib
joblib.dump(reg, 'reg_model.pkl')
model = joblib.load('reg_model.pkl')

# %%
test2 = model.predict(np.array(x_sample).reshape(1, -1))
print(test2)

# %%
f = open('columns.txt','a')
for x in X.columns:
    f.write(x)
    f.write(', ')
f.close()
# %%


# %%
