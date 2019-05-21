# -*- coding:utf-8 -*-

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt


df_test = pd.read_csv('C:/Users/Jagga/Documents/testset.csv',index_col=0)
df_rank = pd.read_csv('C:/Users/Jagga/Documents/rank2.csv',index_col=0)
al = df_rank.index.tolist()
df_test['stock'] = df_test['stock'].apply(str)
for i in range(len(df_test)):
    s = df_test.ix[i, ['stock']].tolist()[0]
    # print(type(s))
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
stock_l = []
for i in range(len(df_test)):
    flag = False
    names = df_test.ix[i,['author']].tolist()[0]
    for item in al:
        if item in names and df_test.ix[i,['type']].tolist()[0] in pos:
            flag = True
    if flag == True:
        stock = df_test.ix[i,['stock']].tolist()[0]
        date = df_test.ix[i,['date']].tolist()[0]
        hist = ts.get_hist_data(stock, start=date, ktype='M')
        hist = hist.sort_index()
        hist = hist['p_change']
        if len(hist) >= 7:
            money += hist[6]
            print('author:', names, 'stock:',stock,'date:',date,'{}month return:{}'.format(6,hist[6]))
            # stock_l.append(stock)
            # date_l.append(date)


        else:
            money += hist[len(hist)-1]
            print('author:', names, 'stock:', stock, 'date:', date, '{}month return:{}'.format(len(hist)-1, hist[len(hist)-1]))
print('',money*100)

# df = pd.read_csv('C:/Users/Jagga/Documents/cement_report_all.csv')
# for i in range(len(df)):
#     if df.ix[i,'stock_code'] == '600801.SH':
#         print('author:',df.ix[i,'author'],'company:',df.ix[i,'company'],'star:',df.ix[i,'company_star'])
#
# code = df['stock_code'].tolist()
# code = list(set(code))
# print(code)

# for i in range(len(code)):
#     date = '2018-03-19'
#     hist = ts.get_hist_data(code[i][:6],start=date,ktype='M')
#     hist = hist.sort_index()
#     hist.preprice = hist.close.shift(1)
#     hist.insert(1, 'preprice', hist.preprice)
#     hist['return'] = hist['p_change']/hist['preprice']
#     hist = hist['return']
#     hist = hist.cumsum()
#     print(hist)
#     p_hist = ts.get_hist_data('000001',start=date,ktype='M')
#     p_hist = p_hist.sort_index()
#     p_hist.preprice = p_hist.close.shift(1)
#     p_hist.insert(1, 'preprice', p_hist.preprice)
#     p_hist['return'] = p_hist['p_change']/p_hist['preprice']
#     p_hist = p_hist['return']
#     p_hist = p_hist.cumsum()
#
#     print(p_hist)
#     fig = plt.figure(figsize=(6,3))
#     plt.plot(hist.index, hist,color='red')
#     plt.plot(p_hist.index,  p_hist,color='blue')
#     print(code[i])
#     plt.title(code[i])
# plt.show()

d = pd.date_range(start='3/7/2017',end='9/2/2018')
dl = []
for item in d:
    dl.append(str(item)[:10])
df = pd.DataFrame(index=dl,columns=['return'])
df['return']=0
fig = plt.figure(figsize=(6,3))
hist = ts.get_hist_data('600449',start='2017-03-16',ktype='D')
# print(hist)
hist = hist.sort_index()
for date in hist.index:
    if date in df.index:
        df.ix[date,['return']] = float(hist.ix[date,['close']].tolist()[0])
        # print(hist.ix[date,['close']])
        # print(df.ix[date,['return']])
print(df)

def getHTMLText(url):
    try:
        # pxs={'http':'http://user:pass@10.10.10.1:1234',
        #      'https':'https://10.10.10.1:1234' }
        # r = requests.get(url,timeout=30,proxies=pxs)
        hd = {'user-agent': 'Chrome/10'}
        r = requests.get(url, headers=hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'

def get_info(url):
    demo = getHTMLText(url)
    soup = BeautifulSoup(demo, 'html.parser')
    # print(soup.find_all('script'))
    s = soup.find_all(string=re.compile('author'))
    if s == []:
        print('null value')
        return -1
    s = s[0]
    print(s)
    b= s.find('rr.firstInit({"data":[')
    st = b+len('rr.firstInit({"data":[')
    ed = s[st:].find(',"pages"')+st
    # print('st=',st)
    # print('ed=',ed)
    if s[st] != '{':
        print('location error')
    else:
        target = ''
        for i in range(st,ed-1):
            target = target + s[i]
    f = []
    t_list = target.split('},{')
    if len(t_list) == 1:
        print(t_list)
    else:
        for j in range(len(t_list)):
            if j == 0:
                t_list[j] = t_list[j] + '}'
            elif j == len(t_list)-1:
                t_list[j] = '{' + t_list[j]
            else:
                t_list[j] = '{' + t_list[j] + '}'
            print(t_list[j])
            f.append(json.loads(t_list[j]))
    return f


if __name__ == '__main__':

    keyword = pd.read_csv('C:/Users/Jagga/Documents/cementin.csv',encoding='gbk')['证券代码'].tolist()
    keyword = list(set(keyword))
    total_info = []
    print('len(keyword)=',len(keyword))
    for i in range(len(keyword)):
        url = 'http://data.eastmoney.com/report/' + keyword[i][:-3] + '.html'
        info_list = get_info(url)
        if info_list != -1:
            total_info.extend(info_list)
    print(len(total_info))
    # print(total_info)
    ti = []
    for i in range(len(total_info)):
        temp = {}
        temp['author'] = total_info[i]['author']
        temp['date'] = total_info[i]['datetime']
        temp['company'] = total_info[i]['insName']
        temp['company_star'] = total_info[i]['insStar']
        temp['stock_code'] = total_info[i]['secuFullCode']
        temp['stock_name'] = total_info[i]['secuName']
        temp['rate'] = total_info[i]['rate']
        temp['title'] = total_info[i]['title']
        temp['infoCode'] = total_info[i]['infoCode']
        ti.append(temp)


    fd = ti[0]
    print(fd)
    fd = pd.DataFrame(fd,index=[0])
    for i in range(1,len(ti)):
        sd = ti[i]
        sd = pd.DataFrame(sd,index=[i])
        fd = pd.concat([fd,sd])
    fd.to_csv('C:/Users/Jagga/Documents/cement_report_all.csv')



#####download pdf files######
# url = 'http://pdf.dfcfw.com/pdf/H3
# _AP201808131177497612_1.pdf'
# root = 'C://pics//'
# path = root + url.split('/')[-1]
# if not os.path.exists(path):
#     r = requests.get(url)
#     # r.encoding = 'gbk'
#     with open(path,'wb') as f:
#         f.write(r.content)
#         f.close()
# else:
#     print('already exists')







# print(soup.prettify())
# tag = soup.script
# print(tag.next_sibling.string)
# print(tag.string)
# print(tag.parent.name)
# print(tag.parent.parent.name)