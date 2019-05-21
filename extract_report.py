import requests
import pandas as pd
import tushare as ts
import re

def get_html_text(url):
    hd = {'user-agent': 'Chrome/10'}
    r = requests.get(url,headers=hd)
    r.encoding = r.apparent_encoding
    try:
        r.raise_for_status()
        return r.text
    except: # 网页请求错误
        return -1

def process_text(url, stock):
    text = get_html_text(url)
    if text == -1:
        return pd.DataFrame()
    text = text[8:-3]
    # print(text)
    t_list = text.split('},{')
    f = {}
    type_l = []
    company_l = []
    date_l = []
    title_l = []
    url_l = []
    stock_l =[]
    author_l=[]
    if len(t_list) == 1:
        return pd.DataFrame()
    else:
        for j in range(len(t_list)):
            pattern = ">[\u4e00-\u9fa5]+<"
            regex = re.compile(pattern)
            name = regex.findall(t_list[j])
            names = [i[1:-1] for i in name]
            name = ','.join(names)
            author_l.append(name)
            if j == 0:
                t_list[j] = t_list[j] + '}'
            elif j == len(t_list) - 1:
                t_list[j] = '{' + t_list[j]
            else:
                t_list[j] = '{' + t_list[j] + '}'
            ed = t_list[j].find(',more')
            t_list[j] = t_list[j][:ed] + '}'
            t_list[j] = t_list[j].replace(',', ',"')
            t_list[j] = t_list[j].replace('{', '{"')
            t_list[j] = t_list[j].replace(':', '":')
            d = eval(t_list[j])
            type_l.append(d['type'])
            company_l.append(d['jgname'])
            date_l.append(d['date'])
            # title_l.append(d['title'])
            url_l.append(d['url'])
            stock_l.append(stock)
    f['type'] = type_l
    f['company'] = company_l
    f['date'] = date_l
    # f['title'] = title_l
    f['url'] = url_l
    f['stock'] = stock_l
    f['author'] = author_l
    # print('author=',len(author_l))
    # print(stock,len(date_l))
    # print(url)
    df = pd.DataFrame.from_dict(f)
    # print(df)
    return df

def report_by_keyword(keyword):
    flag = False
    for key in keyword:
        i = 1
        url = 'http://yanbao.stock.hexun.com/Handle/Json_dzyb_list.aspx?code=' + key + '&page=' + str(i)
        df_0 = process_text(url, key)
        while True:
            i += 1
            url = 'http://yanbao.stock.hexun.com/Handle/Json_dzyb_list.aspx?code=' + key + '&page=' + str(i)
            df = process_text(url, key)
            if df.empty == True:
                break
            df_0 = pd.concat([df_0, df])
        if flag == False:
            df_t = df_0
            flag = True
        else:
            df_t = pd.concat([df_t, df_0])
    return df_t

def get_industy_code(industry):
    indus = ts.get_industry_classified()
    indus = indus[indus['c_name'] == industry]
    indus['code'] = indus['code'].apply(str)
    code = indus['code'].tolist()
    # print('code:',code)
    return code

if __name__ == '__main__':

    indus = '金融行业'
    keyword = get_industy_code(indus)
    df = report_by_keyword(keyword)
    df = df.dropna()
    df = df.sort_values(by='date')
    df.to_csv('C:/Users/Jaggar/Documents/industry_reports/finanace.csv')
    print(df)
    print(len(df))




