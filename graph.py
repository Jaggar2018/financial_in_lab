import pandas as pd
import numpy as np
import datetime


# process the rank
df = pd.read_csv('C:/Users/Jagga/Documents/financial_rank.csv')
df = df[df['score']!=0]
df = df[df['score']>0.8]
df = df[df['total']!=1]
df = df[df['total']!=2]
df = df[df['Unnamed: 0']!='黎']
df = df[df['Unnamed: 0']!='聪']
df = df[df['Unnamed: 0']!='李']
df = df[df['Unnamed: 0']!='张']
# df['weight'] = df['score']
max_min_scaler = lambda x: (x - np.min(x)) / (np.max(x) - np.min(x))
df['total_normal']=df[['total']].apply(max_min_scaler)
df['weight'] = 0.4*df['total_normal']+df['score']
df = df.sort_values(by='weight',ascending=False)
df = df.reset_index(drop=True)
df.rename(columns={'Unnamed: 0':'author','score':'accuracy','weight':'score'}, inplace = True)
pd.set_option('display.max_rows',None)
print(df)
df.to_csv('C:/Users/Jagga/Documents/rank_f.csv')
al = df['author'].tolist()


df_test = pd.read_csv('C:/Users/Jagga/Documents/financial_test.csv',index_col=0)
df_test['stock'] = df_test['stock'].apply(str)
for i in range(len(df_test)):
    s = df_test.ix[i, ['stock']].tolist()[0]
    while len(s) < 6:
        s = '0'+str(s)
    df_test.ix[i, ['stock']] = str(s)
print(df_test)
sl = []
dl = []
pos = ['跑赢大市', '持有', '买入', '增持', '推荐', '强烈推荐']
for i in range(len(df_test)):
    names = str(df_test.ix[i, ['author']].tolist()[0]).split(',')
    for name in names:
        if name in al and df_test.ix[i,['type']].tolist()[0] in pos:
            print(name)
            sl.append(df_test.ix[i,['stock']].tolist()[0])
            dl.append(df_test.ix[i,['date']].tolist()[0])
print(sl)
print(len(sl))
print(dl)
print(len(dl))
sl = []
for d in dl:
    sl.append(datetime.datetime(int(d)) + datetime.timedelta(weeks=24))
print(sl)