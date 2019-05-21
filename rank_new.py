import pandas as pd
import tushare as ts
from datetime import timedelta
from dateutil.parser import parse


def deivide_set(df):
    # pd.set_option('display.max_rows', None)
    # print(df['stock'])
    # df['stock'] = df['stock'].apply(str)
    for i in range(len(df)):
        s = df.ix[i, ['stock']].tolist()[0]
        s = str(s)
        while len(s) < 6:
            s = '0' + s
        df.ix[i, ['stock']] = s

    #     # print(type(s))
    #     if len(s) == 3:
    #         x = '000' + s
    #         df.ix[i, ['stock']] = x
    #     if len(s) == 4:
    #         x = '00' + s
    #         df.ix[i, ['stock']] = x
    df_total = df.sort_values(by='date')
    df_1 = df_total.ix[df_total['date']>='2014-01-01']
    df_1 = df_1.ix[df_1['date']<='2016-12-31']
    df_2 = df_total.ix[df_total['date']>='2017-01-01']
    df_2 = df_2.ix[df_2['date']<='2018-12-31']
    df_1 = df_1.reset_index(drop=True)
    df_2 = df_2.reset_index(drop=True)
    df_1 = df_1.drop(columns=['Unnamed: 0'])
    df_2 = df_2.drop(columns=['Unnamed: 0'])
    # print(df_1['stock'])
    # print(df_2['stock'])
    return df_1,df_2

# AR计算： 个股累加受益-大盘累加受益
def count_AR(df):
    df['stock_change'] = None
    df['market_change'] = None
    sz = '399001'
    sh = '000001'
    # print(df)
    for i in range(len(df)):
        code = df.ix[i, ['stock']].tolist()[0]
        # code = str(code)
        agent = code[:3]
        date = df.ix[i, ['date']].tolist()[0]

        # compute market return
        if agent == '600':
            m_hist = ts.get_hist_data(sh, start=date, ktype='M')
        else:
            m_hist = ts.get_hist_data(sz, start=date, ktype='M')
        m_hist = m_hist.sort_index()
        m_hist.preprice = m_hist.close.shift(1)
        m_hist.insert(1, 'preprice', m_hist.preprice)
        m_hist['return'] = m_hist['p_change'] / m_hist['preprice']
        m_hist = m_hist['return'].cumsum()
        if len(m_hist) >= 7:
            df.ix[i, ['market_change']] = m_hist[6]
        else:
            continue

        # compute stock return

        hist = ts.get_hist_data(code, start=date, ktype='M')
        hist = hist.sort_index()
        hist.preprice = hist.close.shift(1)
        hist.insert(1, 'preprice', hist.preprice)
        hist['return'] = hist['p_change'] / hist['preprice']
        hist = hist['return'].cumsum()
        if len(hist) >= 7:
            df.ix[i, ['stock_change']] = hist[6]
        else:
            continue

    df['AR'] = df['stock_change'] - df['market_change']
    print(df)
    df.to_csv('C:/Users/Jaggar/Documents/industry_reports/financial_AR.csv') #节省调试时间
    return df

# 排序
def ranking():
    df = pd.read_csv('C:/Users/Jaggar/Documents/industry_reports/financial_AR.csv')
    a = df['author'].tolist()
    author = []
    for i in range(len(a)):
        b = str(a[i]).split(',')
        for j in range(len(b)):
            author.append(b[j])
    author = list(set(author))
    rank = pd.DataFrame(index=author, columns=['star','total'])
    rank['star'] = 0
    rank['total'] = 0
    neg = ['中性', '审慎推荐','谨慎增持', '谨慎推荐', '卖出','谨慎买入']
    pos = ['跑赢大市', '持有',  '买入', '增持', '推荐', '强烈推荐']
    for i in range(len(df)):
        print(df.ix[i,['author']].tolist()[0])
        name = str(df.ix[i, ['author']].tolist()[0]).split(',')
        for k in name:
            rank.ix[k,['total']] += 1
        if float(df.ix[i, ['AR']]) > 0 and (df.ix[i,['type']].tolist()[0] in pos):
            for j in name:
                rank.ix[j, ['star']] += 1
        elif float(df.ix[i, ['AR']]) < 0 and (df.ix[i,['type']].tolist()[0] in neg):
            for j in name:
                rank.ix[j, ['star']] += 1
        else:
            pass
    rank['score'] = rank['star']/rank['total']
    rank = rank.sort_values(by='score', axis=0, ascending=False)
    print('rank')
    print(rank)
    return rank

def test(df_test, df_rank):
    i = pick_without_break(df_test, df_rank)
    al = df_rank.index.tolist()
    al = al[:i]
    df_test['stock'] = df_test['stock'].apply(str)
    for i in range(len(df_test)):
        s = df_test.ix[i, ['stock']].tolist()[0]
        if len(s) == 3:
            x = '000' + s
            df_test.ix[i, ['stock']] = x
        if len(s) == 4:
            x = '00' + s
            df_test.ix[i, ['stock']] = x

    print(df_test)
    print(al)
    neg = ['中性', '审慎推荐', '谨慎增持', '谨慎推荐', '卖出', '谨慎买入']
    pos = ['跑赢大市', '持有', '买入', '增持', '推荐', '强烈推荐']
    money = 0
    for i in range(len(df_test)):
        flag = False
        names = df_test.ix[i, ['author']].tolist()[0]
        for item in al:
            if item in names and df_test.ix[i, ['type']].tolist()[0] in pos:
                flag = True
        # 后两年report的author在df_rank之中时，计算df_rank中author推荐的个股6个月收益之和
        if flag == True:
            stock = df_test.ix[i, ['stock']].tolist()[0]
            date = df_test.ix[i, ['date']].tolist()[0]
            hist = ts.get_hist_data(stock, start=date, ktype='M')
            hist = hist.sort_index()
            hist = hist['p_change']
            if len(hist) >= 7:
                money += hist[6]
                print('author:', names, 'stock:', stock, 'date:', date, '{}month return:{}'.format(6, hist[6]))
            else:
                money += hist[len(hist) - 1]
                print('author:', names, 'stock:', stock, 'date:', date,
                      '{}month return:{}'.format(len(hist) - 1, hist[len(hist) - 1]))
    print('return:', money * 100)
    return money

# 选择合适的author list 解决预测空窗期的问题
def pick_without_break(df_test, df_rank):
    author = df_rank.index.tolist()
    st_l = []
    j = 8
    timebreak = False
    while timebreak == False:
        al = author[:j]
        pos = ['跑赢大市', '持有', '买入', '增持', '推荐', '强烈推荐']
        for i in range(len(df_test)):
            flag = False
            names = str(df_test.ix[i, ['author']].tolist()[0])
            for item in al:
                if item in names and df_test.ix[i, ['type']].tolist()[0] in pos:
                    flag = True
            # 后两年report的author在df_rank之中时
            if flag == True:
                date = df_test.ix[i, ['date']].tolist()[0]
                st_l.append(date)
        st_l = sorted(st_l)
        pre_st = st_l[0]
        timebreak = True
        for st in st_l[1:]:
            pre_st = parse(pre_st)
            pre_ed = pre_st + timedelta(30*6)
            pre_ed = str(pre_ed)[:10]
            if pre_ed < st:      # 有空窗期
                timebreak = False
            pre_st = st
        ed = parse(st_l[-1]) + timedelta(30*6)
        ed = ed.strftime('%Y-%m-%d')
        if ed < '2018-12-31':
            timebreak = False
        j += 1
        print('i=',j)
    return j


if __name__ =='__main__':
    df = pd.read_csv('C:/Users/Jaggar/Documents/industry_reports/finanace.csv')
    # df = df.dropna()
    train_df, test_df = deivide_set(df)
    # count_AR(train_df) #数据已保存，节省调试时间
    rank_df = ranking()
    print(rank_df)
    # i = pick_without_break(train_df, rank_df)
    # print('i=',i)
    # money = test(test_df, rank_df)
    # rank_df.to_csv('C:/Users/Jagga/Documents/financial_rank.csv')
    pd.set_option('display.max_rows',None)
    # test_df.to_csv('C:/Users/Jagga/Documents/financial_test.csv')
