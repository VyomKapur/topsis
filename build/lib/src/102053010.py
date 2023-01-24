import pandas as pd
import sys
import numpy as np 


if len(sys.argv) != 5:
    raise Exception('Incorrect number of inputs!')
try:
    data = pd.read_csv(sys.argv[1])
except:
    raise Exception('File not found/ Openable!')

if data.shape[1] < 3:
    raise Exception('File must have more than 3 columns')

data.drop(columns=data.columns[0], inplace=True)
weights = sys.argv[2].split(',')
weights = [int(i) for i in weights]
impacts = sys.argv[3].split(',')
for i in impacts:
    if i not in ['+','-']:
        raise Exception('Invalid impacts, only add + or - seperated by commas')

if len(impacts) != len(weights) or len(impacts) != data.shape[1]:
    raise Exception('Non matching weights, impacts or columns in the data file!')
df = pd.read_csv(sys.argv[1])
result_file_addr = sys.argv[4]

for i in range(data.shape[1]):
    total_sq_sum = 0 
    for j in range(data.shape[0]):
        total_sq_sum += pow(data.iloc[j,i],2)
    total_sq_sum = pow(total_sq_sum,0.5)
    data.iloc[:,i] = data.iloc[:,i].apply(lambda x: x*weights[i]/total_sq_sum)

ideal_best = []
ideal_worst = []

for i in range(len(impacts)):
    if impacts[i] == "+":
        ideal_best.append(data.iloc[:,i].max())
        ideal_worst.append(data.iloc[:,i].min())
    else:
        ideal_best.append(data.iloc[:,i].min())
        ideal_worst.append(data.iloc[:,i].max())

s_pos = []
s_neg = []

for i in range(data.shape[0]):
    pos_sum = 0
    neg_sum = 0
    for j in range(len(ideal_best)):
        pos_sum += pow(data.iloc[i,j]-ideal_best[j],2)
        neg_sum += pow(data.iloc[i,j] - ideal_worst[j],2)
    s_pos.append(pow(pos_sum,0.5))
    s_neg.append(pow(neg_sum,0.5))

p = []
for i in range(len(s_pos)):
    p.append(s_neg[i]/(s_neg[i]+s_pos[i]))


df['Topsis Score'] = p
df['Rank'] = df['Topsis Score'].rank(ascending=False)

df.to_csv(result_file_addr, index=False)
