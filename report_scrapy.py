import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import os
import demjson


file_path = 'C:/Users/Jagga/Documents/cement_report_all.csv'

a = pd.read_csv(file_path)
search_list = []
date = a['date'].tolist()
infoCode = a['infoCode'].tolist()
title = a['title'].tolist()


url = 'http://yanbao.stock.hexun.com/Handle/Json_dzyb_list.aspx?code=000877&page=1'
hd = {'user-agent': 'Chrome/10'}
r = requests.get(url, headers=hd)
r.encoding = r.apparent_encoding
# try:
r.raise_for_status()
t = r.text
t = t[8:-3]
# print(t)
f = []
t_list = t.split('},{')
if len(t_list) == 1:
    print(t_list)
else:
    for j in range(len(t_list)):
        if j == 0:
            t_list[j] = t_list[j] + '}'
        elif j == len(t_list) - 1:
            t_list[j] = '{' + t_list[j]
        else:
            t_list[j] = '{' + t_list[j] + '}'
        ed = t_list[j].find(',more')
        t_list[j]=t_list[j][:ed]+'}'
        t_list[j] = t_list[j].replace(',', ',"')
        t_list[j]=t_list[j].replace('{','{"')
        t_list[j] = t_list[j].replace(':','":')

        print(t_list[j])
        x=eval(t_list[j])

        print(x['title'])
print(f)
# soup = BeautifulSoup(t, 'html.parser')
# print(soup.a.string)
# for item in soup.children:
#     l = item.string
#     print(l[:80])

# for item in soup.children:
#     print(item)
# except:  # 无当前page
#     print(-1)

# json.loads(t_list[j])
# for i in range(len(date)):
#     temp = date[i][0:4]+date[i][5:7]+date[i][8:10]
#     date[i] = temp
#
# if len(date)!=len(infoCode) or len(date) != len(title):
#     print('error1')
#
# for i in range(len(date)):
#     hd = {'user-agent':'Chrome/10'}
#     r = requests.get('http://data.eastmoney.com/report/'+date[i]+'/'+infoCode[i]+'.html', headers=hd)
#     r.raise_for_status()
#     r.encoding = r.apparent_encoding
#     print(r.text)
#     bf = BeautifulSoup(r.text,'html.parser')
#     report = bf.find_all('div',class_="newsContent")[0].text
#     path = 'C:/Users/Jagga/Documents/report_text_n/'+str(i)+'.txt'
#     with open(path,'w',encoding='utf-8') as f:
#         f.write(report)
#     f.close()
    # ############download report pdf##############
    # bs = BeautifulSoup(r.text, 'html.parser')
    # a = bs.find_all('a', href=True)
    # pdf_url = 0
    # for item in a:
    #     link = item['href']
    #     pattern = 'http://pdf.dfcfw.com.*.pdf'
    #     x = re.findall(pattern, link)
    #     if x != []:
    #         pdf_url = x[0]
    #         break
    # if pdf_url == 0:
    #     print('no pdf')
    #     continue
    # root = 'C:/Users/Jagga/Documents/report_pdf/'
    # path = root +title[i]+'.pdf'
    # if not os.path.exists(path):
    #     r = requests.get(pdf_url)
    #     # r.encoding = 'gbk'
    #     with open(path,'wb') as f2:
    #         f2.write(r.content)
    #         f2.close()
    # else:
    #     print('already exists')
